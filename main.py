from utils.utils import make_data_set, read_pkl, save_pkl, make_recipes,filter_recipe
from utils.Recipe import Recipe, RecipesProject
from utils.build_chroma_db import build_chroma_db, requst_chroma_db
from utils.build_knowledge_graph import make_tags_list, lemmatize_tags, build_knowledge_graph\
    , lemmatize, lemmatize_sentance, make_one_word_tags_list, enreach_query_with_relative_tags, save_graph

import torch

MAIN_DIR = "/home/zaderu/Documents/MLHS/LLM Project/data/povar.ru/recipes/"
FILE_NAME = "/workspace/llm_project/data/povar_recipes_"
EMBEDDING_MODEL = "ai-forever/sbert_large_nlu_ru"

def load_pickle():
    
    povar_recipes = []
    for i in range(1, 4):
        _povar_recipes = read_pkl(FILE_NAME + str(i) + ".pickle")
        povar_recipes.extend(_povar_recipes)
    print(len(povar_recipes))

    return povar_recipes

def create_db(recipes_list):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    vector_store, tokenizer = build_chroma_db(
        recipes_list,
        embedding_model=EMBEDDING_MODEL, #"nomic-ai/nomic-embed-text-v1.5", #"IlyaGusev/saiga_yandexgpt_8b" 
        device=device,
    )
    return vector_store, tokenizer


def main():
    print("Downloading Recipes ... ")
    povar_recipes = load_pickle()
    print("Processing Recipes ... ")
    recipes_list = make_recipes(povar_recipes)
    recipes_list = filter_recipe(recipes_list, max_steps = 10, max_min=120, min_rating=4, min_votes=2)
    save_pkl(recipes_list, "./data/Recipe_final.pickle")
    print("Making Vectore Store ... ")
    vector_store, tokenizer = create_db(recipes_list)
    print("Making tags ... ")
    tags = make_tags_list(recipes_list)
    lemmatize_tags(tags)
    one_word_tags = make_one_word_tags_list(tags)

    print("Making Knowledge Graph ... ")
    Graph = build_knowledge_graph(recipes_list, tags)

 
    print("Making Project ... ")
    rp = RecipesProject(
        recipes=recipes_list,
        knowledgeGraph=Graph,
        tags=tags,
        vectorStore=vector_store,
        oneWordTags=one_word_tags
    )
    save_pkl(rp.recipes, "./data/rp_recipes.pickle")        
    save_pkl(rp.knowledgeGraph, "./data/rp_knowledgeGraph.pickle")        
    save_pkl(rp.tags, "./data/rp_tags.pickle")
    save_pkl(rp.oneWordTags, "./data/rp_oneWordTags.pickle")  
    print("done Making Project ... ")
    

if __name__ == "__main__":
    main()