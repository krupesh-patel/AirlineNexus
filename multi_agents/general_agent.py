import os
import sys

from model.moonshot import get_model

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strands import tool, Agent


@tool
def generat_agent(query: str) -> str:
    """
    Process and respond to general queries.

    Args:
        query: general question or request

    Returns:
        A helpful response addressing the general query.
    """
    formatted_query = f"""Analyze and respond to this general query: {query}"""

    try:
        g_agent = Agent(
            model=get_model(),
            system_prompt="You are a general assistant. Provide clear and concise answers to user queries.",
            callback_handler=None,
            tools=[]
        )
        response = g_agent(formatted_query)
        return str(response)
    except Exception as e:
        return f"Error processing your policy related query: {str(e)}"
