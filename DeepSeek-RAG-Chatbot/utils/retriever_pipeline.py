#import streamlit as st
from utils.build_graph import retrieve_from_graph
from langchain_core.documents import Document
import requests

# 🚀 Query Expansion with HyDE
def expand_query(query,uri,model):
    try:
        response = requests.post(uri, json={
            "model": model,
            "prompt": f"Представь, что ты шеф-повар. Напиши подробный рецепт на основе запроса: : {query}",
            "stream": False
        }).json()
        return f"{query}\n{response.get('response', '')}"
    except Exception as e:
        # st.error(f"Query expansion failed: {str(e)}")
        print(f"Query expansion failed: {str(e)}")
        return query


# 🚀 Advanced Retrieval Pipeline
def retrieve_documents(query, uri, model, chat_history="", st=None):
    expanded_query = expand_query(f"{chat_history}\n{query}", uri, model) if st.session_state.enable_hyde else query
    print(f"\n\nQuery Expansion with HyDE: {expanded_query}")
    
    # 🔍 Retrieve documents using BM25 + FAISS
    docs = st.session_state.retrieval_pipeline["ensemble"].invoke(expanded_query)
    print(f"\n\nRetrieved documents using BM25 + FAISS: {docs}")

    # 🚀 GraphRAG Retrieval
    if st.session_state.enable_graph_rag:
        graph_results = retrieve_from_graph(query, st.session_state.retrieval_pipeline["knowledge_graph"])
        
        # Debugging output
        # st.write(f"🔍 GraphRAG Retrieved Nodes: {graph_results}")
        print(f"\n\n🔍 GraphRAG Retrieved Nodes: {graph_results}")

        # Ensure graph results are correctly formatted
        graph_docs = []
        for node in graph_results:
            graph_docs.append(Document(page_content=node))  # ✅ Fix: Correct Document initialization

        # If graph retrieval is successful, merge it with standard document retrieval
        if graph_docs:
            docs = graph_docs + docs  # Merge GraphRAG results with FAISS + BM25 results
    
    # 🚀 Neural Reranking (if enabled)
    if st.session_state.enable_reranking:
        pairs = [[query, doc.page_content] for doc in docs]  # ✅ Fix: Use `page_content`
        scores = st.session_state.retrieval_pipeline["reranker"].predict(pairs)
        print(f"\n\nNeural Reranking (if enabled): {scores}")

        # Sort documents based on reranking scores
        ranked_docs = [doc for _, doc in sorted(zip(scores, docs), reverse=True)]
    else:
        ranked_docs = docs

    return ranked_docs[:st.session_state.max_contexts]  # Return top results based on max_contexts


# 🚀 Advanced Retrieval Pipeline
def retrieve_documents_by_query(query, uri, model, chat_history="", st=None):
    # expanded_query = expand_query(f"{chat_history}\n{query}", uri, model) if st.session_state.enable_hyde else query
    # print(f"\n\nQuery Expansion with HyDE: {expanded_query}")
    
    # 🔍 Retrieve documents using BM25 + FAISS
    docs = st.session_state.retrieval_pipeline["ensemble"].invoke(query)
    print(f"\n\nRetrieved documents using BM25 + FAISS: {docs}")

    # 🚀 GraphRAG Retrieval
    if st.session_state.enable_graph_rag:
        graph_results = retrieve_from_graph(query, st.session_state.retrieval_pipeline["knowledge_graph"])
        
        # Debugging output
        # st.write(f"🔍 GraphRAG Retrieved Nodes: {graph_results}")
        print(f"\n\n🔍 GraphRAG Retrieved Nodes: {graph_results}")

        # Ensure graph results are correctly formatted
        graph_docs = []
        for node in graph_results:
            graph_docs.append(Document(page_content=node))  # ✅ Fix: Correct Document initialization

        # If graph retrieval is successful, merge it with standard document retrieval
        if graph_docs:
            docs = graph_docs + docs  # Merge GraphRAG results with FAISS + BM25 results
    
    # 🚀 Neural Reranking (if enabled)
    if st.session_state.enable_reranking:
        pairs = [[query, doc.page_content] for doc in docs]  # ✅ Fix: Use `page_content`
        scores = st.session_state.retrieval_pipeline["reranker"].predict(pairs)
        print(f"\n\nNeural Reranking (if enabled): {scores}")

        # Sort documents based on reranking scores
        ranked_docs = [doc for _, doc in sorted(zip(scores, docs), reverse=True)]
    else:
        ranked_docs = docs

    return ranked_docs[:st.session_state.max_contexts]  # Return top results based on max_contexts

