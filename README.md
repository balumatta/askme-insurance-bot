# askme-insurance-bot
Retrieval-Augmented Generation (RAG) chatbot trained on customer support documentation to assist users by answering queries and providing relevant support information.

## Project Structure

This project consists of two main components:

1. **Backend**: The backend is built using FastAPI and handles the chatbot logic, document processing, and response generation. It is set up to read documents from the `/backend/docs` directory and generate responses based on the content found within those documents. For detailed setup and instructions, please refer to the README.md file located in the `backend` directory.

2. **Frontend**: The frontend is a Vue.js application that provides an interactive user interface for the chatbot. It allows users to input queries, which are then sent to the backend for processing. For instructions on setting up and running the frontend, please see the README.md file in the `frontend` directory.
