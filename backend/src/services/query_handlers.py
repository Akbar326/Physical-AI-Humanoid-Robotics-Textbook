"""
Query handlers for different types of queries in the RAG Agent API
"""

import logging
from typing import List
from ..models.search import RetrievedContext
from .openai_agent import openai_agent_service
from .query_analyzer import QueryType


logger = logging.getLogger(__name__)


class FactualQueryHandler:
    """
    Handler for factual queries that require specific information
    """

    def __init__(self):
        self.openai_service = openai_agent_service

    def format_factual_prompt(self, query: str, retrieved_contexts: List[RetrievedContext]) -> str:
        """
        Format a prompt specifically for factual queries
        """
        context_text = "\n\n".join([
            f"Source: {ctx.title}\nURL: {ctx.url}\nContent: {ctx.content}"
            for ctx in retrieved_contexts
        ])

        prompt = f"""
        You are an AI assistant that answers factual questions based on provided context from book content.
        Provide concise, specific answers to factual questions based on the following context.

        Context:
        {context_text}

        Query: {query}

        Instructions:
        - Answer the factual query based on the provided context
        - Provide specific facts, figures, definitions, or details requested
        - Include relevant citations to the sources used
        - If the context doesn't contain the specific information requested, say so clearly
        - Keep your response focused and factual
        - List specific items if asked to list

        Response:
        """
        return prompt

    def process_factual_query(self, query: str, retrieved_contexts: List[RetrievedContext], temperature: float = 0.1) -> str:
        """
        Process a factual query with specialized handling
        """
        logger.info(f"Processing factual query: {query[:50]}...")

        # Format the specialized prompt
        formatted_prompt = self.format_factual_prompt(query, retrieved_contexts)

        # Use the OpenAI service to generate response
        response = self.openai_service.generate_response_with_temperature(
            type('obj', (object,), {
                'query': query,
                'retrieved_chunks': retrieved_contexts,
                'formatted_prompt': formatted_prompt,
                'raw_response': None
            })(),
            temperature
        )

        logger.info(f"Factual query processed successfully")
        return response


class AnalyticalQueryHandler:
    """
    Handler for analytical queries that require analysis or explanation
    """

    def __init__(self):
        self.openai_service = openai_agent_service

    def format_analytical_prompt(self, query: str, retrieved_contexts: List[RetrievedContext]) -> str:
        """
        Format a prompt specifically for analytical queries
        """
        context_text = "\n\n".join([
            f"Source: {ctx.title}\nURL: {ctx.url}\nContent: {ctx.content}"
            for ctx in retrieved_contexts
        ])

        prompt = f"""
        You are an AI assistant that analyzes and explains concepts based on provided context from book content.
        Provide thorough analysis, explanations, and reasoning for analytical questions.

        Context:
        {context_text}

        Query: {query}

        Instructions:
        - Analyze and explain the concepts based on the provided context
        - Provide reasoning and connections between different ideas
        - Synthesize information from multiple sources if available
        - Include relevant citations to the sources used
        - If the context doesn't contain sufficient information for analysis, acknowledge this
        - Structure your response with clear explanations and logical flow

        Response:
        """
        return prompt

    def process_analytical_query(self, query: str, retrieved_contexts: List[RetrievedContext], temperature: float = 0.3) -> str:
        """
        Process an analytical query with specialized handling
        """
        logger.info(f"Processing analytical query: {query[:50]}...")

        # Format the specialized prompt
        formatted_prompt = self.format_analytical_prompt(query, retrieved_contexts)

        # Use the OpenAI service to generate response
        response = self.openai_service.generate_response_with_temperature(
            type('obj', (object,), {
                'query': query,
                'retrieved_chunks': retrieved_contexts,
                'formatted_prompt': formatted_prompt,
                'raw_response': None
            })(),
            temperature
        )

        logger.info(f"Analytical query processed successfully")
        return response


class ComparativeQueryHandler:
    """
    Handler for comparative queries that require comparison or contrast
    """

    def __init__(self):
        self.openai_service = openai_agent_service

    def format_comparative_prompt(self, query: str, retrieved_contexts: List[RetrievedContext]) -> str:
        """
        Format a prompt specifically for comparative queries
        """
        context_text = "\n\n".join([
            f"Source: {ctx.title}\nURL: {ctx.url}\nContent: {ctx.content}"
            for ctx in retrieved_contexts
        ])

        prompt = f"""
        You are an AI assistant that compares and contrasts concepts based on provided context from book content.
        Provide clear comparisons and contrasts between different concepts, approaches, or ideas.

        Context:
        {context_text}

        Query: {query}

        Instructions:
        - Compare and contrast the requested items based on the provided context
        - Highlight similarities and differences clearly
        - Organize the comparison in a structured way (e.g., point-by-point or by category)
        - Include relevant citations to the sources used
        - If the context doesn't contain sufficient information for comparison, acknowledge this
        - Focus on the specific aspects requested in the query

        Response:
        """
        return prompt

    def process_comparative_query(self, query: str, retrieved_contexts: List[RetrievedContext], temperature: float = 0.3) -> str:
        """
        Process a comparative query with specialized handling
        """
        logger.info(f"Processing comparative query: {query[:50]}...")

        # Format the specialized prompt
        formatted_prompt = self.format_comparative_prompt(query, retrieved_contexts)

        # Use the OpenAI service to generate response
        response = self.openai_service.generate_response_with_temperature(
            type('obj', (object,), {
                'query': query,
                'retrieved_chunks': retrieved_contexts,
                'formatted_prompt': formatted_prompt,
                'raw_response': None
            })(),
            temperature
        )

        logger.info(f"Comparative query processed successfully")
        return response


# Global instances for convenience
factual_query_handler = FactualQueryHandler()
analytical_query_handler = AnalyticalQueryHandler()
comparative_query_handler = ComparativeQueryHandler()