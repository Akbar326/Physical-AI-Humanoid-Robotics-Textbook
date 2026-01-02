import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Any
from pathlib import Path

from ..models.document import Document
from ..utils.logging import app_logger


class VectorStore:
    """
    A wrapper class for FAISS vector store operations.
    """

    def __init__(self, index_path: str = "vector_store.faiss", documents_path: str = "documents.pkl"):
        self.index_path = index_path
        self.documents_path = documents_path
        self.index = None
        self.documents: List[Document] = []

    def create_index(self, dimension: int):
        """
        Create a new FAISS index with the specified dimension.
        """
        self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
        app_logger.info(f"Created FAISS index with dimension {dimension}")

    def add_embeddings(self, embeddings: np.ndarray, documents: List[Document]):
        """
        Add embeddings and corresponding documents to the index.
        """
        if self.index is None:
            raise ValueError("Index not created. Call create_index first.")

        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)

        # Store documents
        self.documents.extend(documents)

        app_logger.info(f"Added {len(documents)} embeddings to index")

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar vectors in the index.
        """
        if self.index is None:
            raise ValueError("Index not loaded.")

        # Normalize query embedding
        faiss.normalize_L2(query_embedding)

        # Perform search
        scores, indices = self.index.search(query_embedding, top_k)

        # Prepare results
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.documents):
                results.append({
                    "score": float(score),
                    "document": self.documents[idx],
                    "index": int(idx)
                })

        return results

    def save(self):
        """
        Save the index and documents to disk.
        """
        if self.index is None:
            raise ValueError("Index not created.")

        # Create directory if it doesn't exist
        Path(self.index_path).parent.mkdir(parents=True, exist_ok=True)

        # Save FAISS index
        faiss.write_index(self.index, self.index_path)

        # Save documents
        with open(self.documents_path, 'wb') as f:
            pickle.dump(self.documents, f)

        app_logger.info(f"Saved index to {self.index_path} and documents to {self.documents_path}")

    def load(self) -> bool:
        """
        Load the index and documents from disk.
        """
        try:
            if os.path.exists(self.index_path) and os.path.exists(self.documents_path):
                # Load FAISS index
                self.index = faiss.read_index(self.index_path)

                # Load documents
                with open(self.documents_path, 'rb') as f:
                    self.documents = pickle.load(f)

                app_logger.info(f"Loaded index from {self.index_path} with {len(self.documents)} documents")
                return True
            else:
                app_logger.info("No existing index found")
                return False
        except Exception as e:
            app_logger.error(f"Error loading index: {str(e)}")
            return False

    def reset(self):
        """
        Reset the index and clear documents.
        """
        self.index = None
        self.documents = []
        app_logger.info("Reset vector store")