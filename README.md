# LLM project

## Step 1: Simple LLM w/o RAG

### 1. Enviroment
```
python -m venv llm_venv
source llm_venv/bin/activate
pip install ipykernel
python -m ipykernel install --user --name=llm_venv --display-name "Python (llm_venv)"
```
### 2. Install local LLM Ollama + mistral
```
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull mistral
```
### 3. Restart ollama
```
apt update
apt install -y lsof
lsof -i :11434
ollama serve &

kill -9 1317
```
