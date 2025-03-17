from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer, AutoModel
import torch
from langchain.embeddings.base import Embeddings
import numpy as np
from langchain_core.documents import Document
from langchain_chroma import Chroma
import uuid

MAX_LENGTH = 512
MAX_N_CHUNKS = 40_000


def get_embedding(text, tokenizer, model, device):
    # Fonction pour générer les embeddings
    max_length = MAX_LENGTH
    tokens = tokenizer(
        text, 
        return_tensors="pt", 
        padding=False, 
        truncation=False
    )["input_ids"].squeeze()

    # Découper le texte en morceaux de 512 tokens
    chunks = [tokens[i:i + max_length] for i in range(0, len(tokens), max_length)]

    embeddings = []
    for chunk in chunks:
        inputs = {
            "input_ids": chunk.unsqueeze(0).to(device),
            "attention_mask": torch.ones_like(chunk).unsqueeze(0).to(device)
        }
        with torch.no_grad():
            outputs = model(**inputs)
        embeddings.append(outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy())

    # Combiner les embeddings (exemple : moyenne)
    combined_embedding = np.mean(embeddings, axis=0)
    return combined_embedding.tolist()

class CustomEmbeddings(Embeddings):
    # Wrapper pour Langchain
    def __init__(self, tokenizer, model, device):
        self.tokenizer = tokenizer
        self.model = model
        self.device = device
        
    def embed_documents(self, texts):
        return [get_embedding(text, self.tokenizer, self.model, self.device) for text in texts]
    
    def embed_query(self, query):
        return get_embedding(query, self.tokenizer, self.model, self.device)


def build_chroma_db(
        recipes_list,
        embedding_model="ai-forever/sbert_large_nlu_ru",
        device="cuda",
        persist_directory='./chroma_db',
        chunk_size=1000, chunk_overlap=200, length_function=len):
    
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=length_function
    )

    documents = [recipe.document for recipe in recipes_list]

    documents = text_splitter.split_documents(documents)

    print(f"{len(documents)} recipes are to be loaded to chroma db")
    if len(documents) > MAX_N_CHUNKS:
        print(f"Length {len(documents)} is exeeded max value {MAX_N_CHUNKS}")
        return None

    # Charge le modèle et le tokenizer
    tokenizer = AutoTokenizer.from_pretrained(embedding_model)
    model = AutoModel.from_pretrained(embedding_model).to(device)


    # Crée la fonction d'embedding
    embedding_function = CustomEmbeddings(tokenizer, model, device)

    # Initialise Chroma avec le wrapper

    vector_store = Chroma(persist_directory=persist_directory, embedding_function=embedding_function, )

    # Test d'ajout de documents

    uuids = [str(uuid.uuid4()) for _ in range(len(documents))]
    vector_store.add_documents(documents=documents, ids=uuids)
 #   print(f"Chroma DB is created. {len(vector_store)} documents are loaded.")
    
    return vector_store, tokenizer


def requst_chroma_db(vector_store, tokenizer, query, device, k=5):
    tokens = tokenizer(
        query,
        return_tensors="pt", 
        padding=True, 
        truncation=True, 
        max_length=MAX_LENGTH
    ).to(device)
    
    # Décoder les tokens tronqués en texte brut
    query = tokenizer.decode(tokens['input_ids'][0], skip_special_tokens=True)
    
    # Lancer la recherche de similarité avec le texte tronqué
    results = vector_store.similarity_search(
        query,
        k=k,
    )
    
    return results