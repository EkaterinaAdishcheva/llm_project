# LLM project

## Recipe Adviser

### Set the enviroment
```
python -m venv llm_venv
source llm_venv/bin/activate
pip install -r requerments.txt
python -m spacy download ru_core_news_sm
python -m spacy validate
```

### 2. Install local LLM Ollama + mistral
```
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull mistral
```

### 3. Create RAG
```
python main.py
```

### 3. Run LLM and make queries
chat.ipynb
