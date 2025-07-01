from docx import Document
import fitz  # PyMuPDF
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class DocToVector:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docs')

    @staticmethod
    def read_docx(file_path):
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])

    @staticmethod
    def read_pdf(file_path):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    @staticmethod
    def load_documents(folder_path):
        documents = []
        for filename in os.listdir(folder_path):
            path = os.path.join(folder_path, filename)
            if filename.endswith(".docx"):
                documents.append(DocToVector.read_docx(path))
            elif filename.endswith(".pdf"):
                documents.append(DocToVector.read_pdf(path))
        return documents

    @staticmethod
    def chunk_text(text, chunk_size=500):
        words = text.split()
        return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    def generate_vector(self):
        documents = self.load_documents(self.folder_path)
        chunks = []
        for doc in documents:
            chunks.extend(self.chunk_text(doc))

        embeddings = self.model.encode(chunks)
        index = faiss.IndexFlatL2(embeddings[0].shape[0])
        index.add(np.array(embeddings))

        # Save to disk
        folder_path = os.path.join(os.path.dirname(__file__), 'embeddings')

        vector_file_path = os.path.join(folder_path, 'vector.index')
        faiss.write_index(index, vector_file_path)

        chunks_file_path = os.path.join(folder_path, 'data_chunks.txt')
        with open(chunks_file_path, "w") as f:
            for c in chunks:
                f.write(c + "\n")


if __name__ == '__main__':
    DocToVector().generate_vector()
