import os.path

from sentence_transformers import SentenceTransformer

from backend.apps.bot.prompts import GENERATE_ANSWER_PROMPT
from backend.apps.bot.serializer import AnswerResponseSerializer
from backend.helpers.llms.openai import OpenAILLM
from backend.main.settings import OPEN_API_KEY, EMBEDDING_MODEL, BASE_DIR
import faiss
import numpy as np


class BotController:
    def __init__(self):
        self.llm = OpenAILLM(OPEN_API_KEY, temperature=0.4)
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    async def generate_answer(self, data):
        """
        Asynchronously generate an answer for a given query by leveraging existing document embeddings and a language model.

        :param data: A dictionary containing the user's query under 'query'.
        :return: A generated answer based on the retrieved context from document embeddings.
        """
        # Define prompt and extract the user query
        prompt_str = GENERATE_ANSWER_PROMPT
        query = data['query']

        # Convert the query into a embedding vector using the sentence transformer model
        query_vec = self.model.encode([query])

        # Load the FAISS index which contains precomputed document vectors
        embeddings_folder_path = os.path.join(BASE_DIR, 'helpers', 'embeddings')
        vector_file_path = os.path.join(embeddings_folder_path, 'vector.index')
        index = faiss.read_index(vector_file_path)

        # Perform a nearest neighbors search on the index to find the top 5 closest document chunks
        matched_distance, matched_index = index.search(np.array(query_vec), k=15)

        # Load all the chunked text data from file
        chunks_file_path = os.path.join(embeddings_folder_path, 'data_chunks.txt')
        with open(chunks_file_path, "r", encoding="utf-8") as f:
            all_chunks = [line.strip() for line in f.readlines()]

        # Retrieve the most relevant chunks based on the indices returned by the FAISS search
        retrieved_chunks = [all_chunks[i] for i in matched_index[0] if i < len(all_chunks)]

        # Combine retrieved chunks into a single context string
        query_context = "\n\n".join(retrieved_chunks)

        # Prepare prompt arguments for generating an answer
        prompt_arguments = {
            'query': query,
            'context': query_context,
        }

        # Use the language model to generate a response using the prompt and context
        answer = await self.llm.get_response(
            prompt_str, prompt_arguments,
            parser_required=True,
            pydantic_object=AnswerResponseSerializer
        )

        return answer
