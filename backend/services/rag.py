import asyncio
import logging
from typing import List, Dict, Any, Tuple
from pathlib import Path
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import AsyncOpenAI
import pickle
import os

from ..models.document import Document
from ..models.query import SourceDocument
from ..config import settings
from ..utils.logging import app_logger
from ..utils.sitemap_parser import SitemapParser
from ..utils.content_extractor import ContentExtractor


class RAGService:
    """
    RAG (Retrieval Augmented Generation) service that handles:
    1. Sitemap ingestion and document processing
    2. Embedding generation and storage
    3. Query processing and response generation
    """

    def __init__(self):
        self.documents: List[Document] = []
        self.vector_index = None
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.vector_store_path = "vector_store.faiss"
        self.documents_path = "documents.pkl"

        # Validate required settings
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        if not settings.sitemap_url:
            raise ValueError("SITEMAP_URL environment variable is required")

    async def load_vector_store(self):
        """
        Load the pre-built vector store and documents from disk.
        """
        try:
            if os.path.exists(self.vector_store_path) and os.path.exists(self.documents_path):
                # Load FAISS index
                self.vector_index = faiss.read_index(self.vector_store_path)

                # Load documents
                with open(self.documents_path, 'rb') as f:
                    self.documents = pickle.load(f)

                app_logger.info(f"Loaded vector store with {len(self.documents)} documents")
            else:
                app_logger.info("No existing vector store found. Ready for ingestion.")
        except Exception as e:
            app_logger.error(f"Error loading vector store: {str(e)}")
            raise

    async def ingest_sitemap(self, sitemap_url: str, force_rebuild: bool = False):
        """
        Ingest content from a sitemap URL, generate embeddings, and build the vector store.
        """
        try:
            app_logger.info(f"Starting sitemap ingestion from: {sitemap_url}")

            # Parse sitemap and extract content
            sitemap_parser = SitemapParser(sitemap_url)
            urls = await sitemap_parser.get_urls()

            app_logger.info(f"Found {len(urls)} URLs to process")

            # Process each URL and extract content
            documents = []
            for i, url in enumerate(urls):
                app_logger.info(f"Processing {i+1}/{len(urls)}: {url}")

                title, content = await self._extract_content_from_url(url)
                if content:
                    # Split content into chunks
                    chunks = self._chunk_content(content, max_chunk_size=1000)

                    for j, chunk in enumerate(chunks):
                        doc = Document(
                            content=chunk,
                            source_url=url,
                            title=title
                        )
                        documents.append(doc)

                        app_logger.debug(f"Created chunk {j+1} for {url}")
                else:
                    app_logger.warning(f"Could not extract content from {url}")

            # Update documents list
            self.documents = documents
            app_logger.info(f"Created {len(documents)} document chunks")

            # Generate embeddings
            app_logger.info("Generating embeddings...")
            embeddings = []
            for i, doc in enumerate(documents):
                embedding = self.embedding_model.encode(doc.content)
                embeddings.append(embedding)

                if (i + 1) % 10 == 0:  # Log progress every 10 documents
                    app_logger.info(f"Generated embeddings for {i+1}/{len(documents)} documents")

            # Convert to numpy array
            embeddings_array = np.array(embeddings).astype('float32')

            # Build FAISS index
            dimension = embeddings_array.shape[1]
            self.vector_index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity

            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings_array)
            self.vector_index.add(embeddings_array)

            app_logger.info(f"Built FAISS index with {len(documents)} vectors")

            # Save vector store to disk
            faiss.write_index(self.vector_index, self.vector_store_path)

            # Save documents to disk
            with open(self.documents_path, 'wb') as f:
                pickle.dump(self.documents, f)

            app_logger.info("Vector store saved to disk")

        except Exception as e:
            app_logger.error(f"Error during sitemap ingestion: {str(e)}")
            raise

    async def _extract_content_from_url(self, url: str) -> Tuple[str, str]:
        """
        Extract title and content from a URL.
        """
        try:
            title, content = ContentExtractor.extract_content_from_url(url)
            return title, content

        except Exception as e:
            app_logger.error(f"Error extracting content from {url}: {str(e)}")
            return "", ""

    def _chunk_content(self, content: str, max_chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Split content into overlapping chunks.
        """
        if len(content) <= max_chunk_size:
            return [content]

        chunks = []
        start = 0

        while start < len(content):
            end = start + max_chunk_size
            chunk = content[start:end]
            chunks.append(chunk)

            # Move start forward by (chunk_size - overlap)
            start = end - overlap

            # Handle the case where the remaining content is less than chunk_size
            if len(content) - start <= overlap:
                break

        return chunks

    async def query(self, query_text: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Process a query against the vector store and generate a response.
        """
        if not self.vector_index or not self.documents:
            raise ValueError("Vector store not initialized. Run ingestion first.")

        try:
            # Generate embedding for the query
            query_embedding = self.embedding_model.encode([query_text]).astype('float32')
            faiss.normalize_L2(query_embedding)

            # Perform similarity search
            scores, indices = self.vector_index.search(query_embedding, top_k)

            # Get the relevant documents
            relevant_docs = []
            for idx in indices[0]:
                if idx < len(self.documents):
                    relevant_docs.append(self.documents[idx])

            # Prepare context for the LLM
            context = "\n\n".join([doc.content for doc in relevant_docs])

            # Generate response using OpenAI
            response = await self.openai_client.chat.completions.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided documentation context. If the answer is not in the context, say so."},
                    {"role": "user", "content": f"Context: {context}\n\nQuestion: {query_text}\n\nAnswer:"}
                ],
                max_tokens=500,
                temperature=0.3
            )

            answer = response.choices[0].message.content.strip()

            # Prepare sources
            sources = []
            for doc in relevant_docs:
                source = SourceDocument(
                    title=doc.title,
                    url=doc.source_url,
                    content=doc.content[:200] + "..." if len(doc.content) > 200 else doc.content
                )
                sources.append(source)

            return {
                "answer": answer,
                "sources": sources
            }

        except Exception as e:
            app_logger.error(f"Error processing query: {str(e)}")
            raise