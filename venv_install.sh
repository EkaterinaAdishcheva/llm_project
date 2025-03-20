python -m venv llm_venv
source llm_venv/bin/activate
pip install ipykernel
python -m ipykernel install --user --name=llm_venv --display-name "Python (llm_venv)"

mkdir /workspace/.ssh
echo "use dir /workspace/.ssh/id_rsa to create ssh-key"
ssh-keygen
cp /workspace/.ssh/* /root/.ssh/
chmod 400 /root/.ssh/id_rsa.pub
chmod 400 /root/.ssh/id_rsa


curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull mistral