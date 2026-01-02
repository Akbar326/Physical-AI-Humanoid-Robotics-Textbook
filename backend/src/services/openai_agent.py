"""
OpenAI agent service for the RAG Agent API
"""

import logging
import time
from typing import List, Optional
from openai import OpenAI
from config.settings import OPENAI_API_KEY
from ..models.agent import AgentContext
from ..models.search import RetrievedContext


logger = logging.getLogger(__name__)

# Initialize OpenAI client (will be set when API key is available)
client = None

def get_openai_client():
    """Get or create OpenAI client with API key"""
    global client
    if client is None:
        if OPENAI_API_KEY:
            client = OpenAI(api_key=OPENAI_API_KEY)
        else:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")
    return client


class OpenAIAgentService:
    """
    Service class for handling OpenAI agent interactions
    """

    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model

    def format_prompt(self, query: str, retrieved_contexts: List[RetrievedContext]) -> str:
        """
        Format the prompt with query and retrieved context
        """
        context_text = "\n\n".join([
            f"Source: {ctx.title}\nURL: {ctx.url}\nContent: {ctx.content}"
            for ctx in retrieved_contexts
        ])

        prompt = f"""
        You are an AI assistant that answers questions based on provided context from book content.
        Please provide accurate, helpful responses based on the following context.

        Context:
        {context_text}

        Query: {query}

        Instructions:
        - Answer the query based on the provided context
        - Include relevant citations to the sources used
        - If the context doesn't contain information to answer the query, say so
        - Keep your response concise but informative
        - If you reference specific content, mention the source title and URL

        Response:
        """
        return prompt

    def generate_response(self, agent_context: AgentContext) -> str:
        """
        Generate a response using the OpenAI agent with the provided context
        """
        try:
            # Format the prompt with query and retrieved contexts
            formatted_prompt = self.format_prompt(
                agent_context.query,
                agent_context.retrieved_chunks
            )

            # Update agent context with formatted prompt
            agent_context.formatted_prompt = formatted_prompt

            # Get OpenAI client and call API
            openai_client = get_openai_client()
            response = openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that answers questions based on provided context from book content. Always provide accurate responses grounded in the provided context."},
                    {"role": "user", "content": formatted_prompt}
                ],
                temperature=agent_context.query_request.temperature if hasattr(agent_context, 'query_request') and agent_context.query_request else 0.3
            )

            # Extract the response
            raw_response = response.choices[0].message.content
            agent_context.raw_response = raw_response

            logger.info(f"OpenAI agent generated response for query: {agent_context.query[:50]}...")
            return raw_response

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error generating response from OpenAI agent: {error_msg}")

            # Check for specific OpenAI error types and handle accordingly
            if "rate_limit" in error_msg.lower() or "quota" in error_msg.lower():
                logger.error("OpenAI API rate limit exceeded or quota exhausted")
                raise Exception(f"OpenAI API rate limit exceeded: {error_msg}")
            elif "authentication" in error_msg.lower() or "api key" in error_msg.lower():
                logger.error("OpenAI API authentication error")
                raise Exception(f"OpenAI API authentication failed: {error_msg}")
            elif "invalid_request_error" in error_msg.lower():
                logger.error("OpenAI API invalid request error")
                raise Exception(f"OpenAI API invalid request: {error_msg}")
            elif "server_error" in error_msg.lower() or "500" in error_msg:
                logger.error("OpenAI API server error")
                raise Exception(f"OpenAI API server error: {error_msg}")
            else:
                logger.error(f"Unexpected OpenAI API error: {error_msg}")
                raise e

    def validate_response_grounding(self, response: str, contexts: List[RetrievedContext]) -> bool:
        """
        Validate that the response is grounded in the provided context
        """
        # This is a basic validation - in a real implementation, you might use more sophisticated techniques
        response_lower = response.lower()
        context_found = any(
            any(keyword.lower() in response_lower
                for keyword in [ctx.title.lower(), ctx.content[:100].lower()]
                if len(ctx.content) > 0)
            for ctx in contexts
        )

        return context_found

    def process_query(self, query: str, retrieved_contexts: List[RetrievedContext], temperature: float = 0.3) -> str:
        """
        Process a query with retrieved contexts and return the agent's response
        """
        from ..models.query import QueryRequest

        # Create a temporary query request object to hold temperature
        temp_query_request = QueryRequest(
            query=query,
            temperature=temperature
        )

        agent_context = AgentContext(
            query=query,
            retrieved_chunks=retrieved_contexts
        )

        response = self.generate_response_with_temperature(agent_context, temperature)

        # Validate that the response is grounded in the context
        if not self.validate_response_grounding(response, retrieved_contexts):
            logger.warning("Response may not be fully grounded in provided context")

        return response

    def generate_response_with_temperature(self, agent_context: AgentContext, temperature: float = 0.3) -> str:
        """
        Generate a response using the OpenAI agent with the provided context and temperature
        """
        try:
            # Format the prompt with query and retrieved contexts
            formatted_prompt = self.format_prompt(
                agent_context.query,
                agent_context.retrieved_chunks
            )

            # Update agent context with formatted prompt
            agent_context.formatted_prompt = formatted_prompt

            # Get OpenAI client and call API with specified temperature
            openai_client = get_openai_client()
            response = openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that answers questions based on provided context from book content. Always provide accurate responses grounded in the provided context."},
                    {"role": "user", "content": formatted_prompt}
                ],
                temperature=temperature
            )

            # Extract the response
            raw_response = response.choices[0].message.content
            agent_context.raw_response = raw_response

            logger.info(f"OpenAI agent generated response for query: {agent_context.query[:50]}...")
            return raw_response

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error generating response from OpenAI agent: {error_msg}")

            # Check for specific OpenAI error types and handle accordingly
            if "rate_limit" in error_msg.lower() or "quota" in error_msg.lower():
                logger.error("OpenAI API rate limit exceeded or quota exhausted")
                raise Exception(f"OpenAI API rate limit exceeded: {error_msg}")
            elif "authentication" in error_msg.lower() or "api key" in error_msg.lower():
                logger.error("OpenAI API authentication error")
                raise Exception(f"OpenAI API authentication failed: {error_msg}")
            elif "invalid_request_error" in error_msg.lower():
                logger.error("OpenAI API invalid request error")
                raise Exception(f"OpenAI API invalid request: {error_msg}")
            elif "server_error" in error_msg.lower() or "500" in error_msg:
                logger.error("OpenAI API server error")
                raise Exception(f"OpenAI API server error: {error_msg}")
            else:
                logger.error(f"Unexpected OpenAI API error: {error_msg}")
                raise e


# Global instance for convenience
openai_agent_service = OpenAIAgentService()