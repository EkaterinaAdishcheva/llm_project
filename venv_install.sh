python -m venv llm_venv
source llm_venv/bin/activate
pip install ipykernel
python -m ipykernel install --user --name=llm_venv --display-name "Python (llm_venv)"
pip install -r requirements.txt

python -m spacy download ru_core_news_sm
python -m spacy validate

mkdir /workspace/.ssh
echo "use dir /workspace/.ssh/id_rsa to create ssh-key"
ssh-keygen
cp /workspace/.ssh/* /root/.ssh/
chmod 400 /root/.ssh/id_rsa.pub
chmod 400 /root/.ssh/id_rsa


curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull mistral


git config --global user.email "you@example.com"
git config --global user.name "Your Name"

apt update
apt install -y lsof
apt-get install unzip

lsof -i :11434


unzip ./data/povar_recipes_1.zip -d ./data
unzip ./data/povar_recipes_2.zip -d ./data
unzip ./data/povar_recipes_3.zip -d ./data