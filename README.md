# LLM project

## Step 1: Simple LLM w/o RAG
1. Enviroment
```
python -m venv llm_venv
source llm_venv/bin/activate
pip install ipykernel
python -m ipykernel install --user --name=llm_venv --display-name "Python (llm_venv)"
```
2. Install local LLM Ollama + mistral
```
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
```

```
ollama pull mistral
ollama list
ollama run mistral
ollama ps
```
3. Run test
```
pip install openai fastapi uvicorn
pip install langchain ? transformers accelerate
pip install langchain_ollama
```



```
pip install faiss-cpu sentence-transformers transformers torch
pip install -U langchain langchain-community chromadb sentence-transformers llama-cpp-python numpy
pip install sentencepiece
pip3 install huggingface-hub
huggingface-cli download TheBloke/LLaMA-7b-GGUF llama-7b.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
pip install streamlit

Neoj4
O-jREKl7dDdF30QwMWCFVU30U0f5dtsOqn80QDjkWr4

```
Restart ollama
```
apt update
apt install -y lsof
lsof -i :11434
ollama serve &

kill -9 1317
```


```

pip install llama-cpp-python
```
