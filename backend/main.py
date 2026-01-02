from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Dict, Any
import time
import logging

from config import settings
from models.query import QueryRequest, QueryResponse, IngestRequest, SourceDocument
from services.rag import RAGService
from agent import AgentRAGService
from utils.logging import app_logger

# Initialize FastAPI app
app = FastAPI(
    title="RAG Chatbot API",
    description="API for RAG-based documentation chatbot",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
rag_service = None
agent_service = None

@app.on_event("startup")
async def startup_event():
    global rag_service, agent_service
    try:
        app_logger.info("Initializing RAG service...")
        rag_service = RAGService()
        # Load the vector store if it exists
        await rag_service.load_vector_store()
        app_logger.info("RAG service initialized successfully")

        app_logger.info("Initializing Agent RAG service...")
        agent_service = AgentRAGService()
        # Load the vector store for the agent service as well
        await agent_service.load_vector_store()
        app_logger.info("Agent RAG service initialized successfully")
    except Exception as e:
        app_logger.error(f"Failed to initialize services: {str(e)}")
        raise


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint to verify the service is running.
    """
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "vector_store_loaded": rag_service is not None
    }


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Submit a natural language query to the RAG system and receive a response with citations.
    """
    if rag_service is None:
        raise HTTPException(status_code=500, detail="RAG service not initialized")

    try:
        start_time = time.time()
        result = await rag_service.query(request.query, top_k=request.top_k)
        query_time = time.time() - start_time

        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            query_time=query_time,
            session_id=request.session_id
        )
    except Exception as e:
        app_logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.post("/agent-query", response_model=QueryResponse)
async def agent_query_endpoint(request: QueryRequest):
    """
    Submit a natural language query to the Agent-enhanced RAG system for more sophisticated reasoning.
    """
    if agent_service is None:
        raise HTTPException(status_code=500, detail="Agent RAG service not initialized")

    try:
        start_time = time.time()
        response = await agent_service.query_with_agent(request)
        query_time = time.time() - start_time

        # Update query_time in response if needed
        response.query_time = query_time

        return response
    except Exception as e:
        app_logger.error(f"Agent query failed: {str(e)}")
        # Fallback to regular RAG if agent fails
        if rag_service:
            try:
                start_time = time.time()  # Reset start time for fallback
                result = await rag_service.query(request.query, top_k=request.top_k)
                query_time = time.time() - start_time

                # Convert the result to QueryResponse format
                sources = [
                    SourceDocument(
                        title=source["title"],
                        url=source["url"],
                        content=source["content"]
                    )
                    for source in result["sources"]
                ]

                return QueryResponse(
                    answer=result["answer"],
                    sources=sources,
                    query_time=query_time,
                    session_id=request.session_id
                )
            except Exception as fallback_error:
                app_logger.error(f"Fallback query also failed: {str(fallback_error)}")

        raise HTTPException(status_code=500, detail=f"Agent query failed: {str(e)}")


@app.post("/ingest")
async def ingest_endpoint(request: IngestRequest):
    """
    Trigger the ingestion process to update the vector store with new documentation content.
    """
    if rag_service is None:
        raise HTTPException(status_code=500, detail="RAG service not initialized")

    try:
        app_logger.info(f"Starting ingestion for sitemap: {request.sitemap_url}")
        await rag_service.ingest_sitemap(request.sitemap_url, force_rebuild=request.force_rebuild)

        return {
            "status": "completed",
            "message": "Ingestion process completed successfully",
            "sitemap_url": request.sitemap_url
        }
    except Exception as e:
        app_logger.error(f"Ingestion failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


# Error handling middleware
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    app_logger.error(f"Unhandled exception: {str(exc)}")
    return {"error": "Internal server error", "message": str(exc)}


# Serve frontend files
import os
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "src")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    # If frontend doesn't exist in expected location, create a simple fallback route
    @app.get("/")
    async def root():
        return {"message": "RAG Chatbot API is running. See /docs for API documentation."}
