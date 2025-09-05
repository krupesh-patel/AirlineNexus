import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.client.streamable_http import streamablehttp_client
from strands import Agent, tool
from strands.tools.mcp.mcp_client import MCPClient
from prompts.flight_prompt import FLIGHT_SYSTEM_PROMPT
from model.moonshot import get_model


@tool
def flight_agent(query: str) -> str:
    """
    Process and respond to Flight related queries.

    Args:
        query: Flight related question or request

    Returns:
        A helpful response addressing the flight query.
    """
    formatted_query = f"Analyze and respond to this flight related query: {query}"

    try:
        streamable_http_mcp_client = MCPClient(lambda: streamablehttp_client(os.getenv('MCP_SERVER_URL')))
        # Create an agent with MCP tools
        with streamable_http_mcp_client:
            # Get the tools from the MCP server
            tools = streamable_http_mcp_client.list_tools_sync()

        f_agent = Agent(
            model=get_model(),
            system_prompt=FLIGHT_SYSTEM_PROMPT,
            tools=[] + tools,
        )
        agent_response = f_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response

        return "I apologize, but I couldn't properly analyze your flight related question. Could you please rephrase or provide more context?"
    except Exception as e:
        # Return specific error message for English queries
        return f"Error processing your English language query: {str(e)}"