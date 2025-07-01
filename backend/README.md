# AskMe Insurance Bot

Fast API application for Retrieval-Augmented Generation (RAG) chatbot trained on customer support documentation to assist users by answering queries and providing relevant support information.

### Project Setup

```
sudo apt-get update
sudo apt-get install python3-dev git
sudo apt-get install build-essential libssl-dev libffi-dev
sudo apt-get install libjpeg-dev libfreetype6-dev zlib1g-dev
sudo apt-get install redis
sudo apt-get install virtualenv
sudo apt-get install --upgrade pip

cd askme-insurance-bot
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Prerequisites

Before running the project, you need to generate the text chunks and their corresponding vectors. This is essential for enabling the RAG chatbot to function correctly. Follow the steps below:

1. **Create .env File**:\
   Create .env and add the below info
    ```bash
    ENVIRONMENT=local
    OPEN_API_KEY=
    ```

2. **Generate Document Vectors**:
   Ensure that all your document files are placed in the `docs` directory.\
   Run the following command to generate text chunks and vectors:

   ```bash
   python backend/helpers/load_vectors.py
   ```

   This command will create vector embeddings and serialize them into `vector.index` and `data_chunks.txt` in the `backend/apps/embeddings` directory.


### Run Fast API
```bash
 # Directly running the main file
 python run_fastapi.py 

 # Run Using command
 uvicorn run_fastapi:app --host 0.0.0.0 --port 9000
```
