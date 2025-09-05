import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, List
from strands import Agent, tool
from utils.embeddings import embedding_service
from prompts.policy_prompt import POLICY_SYSTEM_PROMPT
from model.moonshot import get_model

from config.database import db_manager


def _search_policies(query) -> List[Dict]:
    """Search policies using vector search"""
    try:
        # Get vector client
        vector_client = db_manager.get_vector_client()

        # Generate embedding
        query_embedding = embedding_service.embed_text(query)

        # Perform search
        results = vector_client.query(query_vector=query_embedding, k=3)

        policies = []
        for result in results:
            if result.distance < 0.7:
                policies.append({
                    'title': result.metadata.get('title', ''),
                    'content': result.document,
                    'category': result.metadata.get('category', ''),
                    'similarity_score': result.distance
                })

        return policies

    except Exception as e:
        print(f"Vector search error: {e}")
        return []


@tool
def policy_agent(query: str) -> str:
    """
    Process and respond to Policy related queries.

    Args:
        query: Policy related question or request

    Returns:
        A helpful response addressing the Policy query.
    """
    formatted_query = f"""Analyze and respond to this policy related query: {query}
    Below are some relevant airline policies that might help you:\n
    """

    try:
        policies = _search_policies(query)

        if policies:
            p_agent = Agent(
                model=get_model(),
                system_prompt=POLICY_SYSTEM_PROMPT,
            )

            final_query = formatted_query + "\n".join(
                [f"- title: {p['title']}\ncontent: {p['content']}\ncategory: {p['category']}" for p in policies])

            agent_response = p_agent(final_query)
            text_response = str(agent_response)

            if len(text_response) > 0:
                return text_response

        else:
            return "I couldn't find any relevant policies related to your question. Could you please provide more details or rephrase your query?"

    except Exception as e:
        return f"Error processing your policy related query: {str(e)}"
