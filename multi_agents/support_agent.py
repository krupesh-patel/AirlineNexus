import os
import sys
import uuid
from datetime import datetime

from model.moonshot import get_model

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strands import tool, Agent
from typing import Dict, Any


def _analyze_complexity(message) -> Dict[str, Any]:
    """Analyze if message needs support ticket"""
    message_lower = message.lower()

    support_keywords = ["refund", "complaint", "problem", "issue", "cancel", "help", "urgent", "medical"]
    needs_ticket = any(keyword in message_lower for keyword in support_keywords)

    return {
        "needs_ticket": needs_ticket,
        "priority": "HIGH" if "urgent" in message_lower else "MEDIUM"
    }

@tool
def create_support_ticket() -> str:
    """Create support ticket"""
    ticket_id = f"ANX-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    # In production, would save to database
    # For demo, just return ticket ID
    return ticket_id


@tool
def format_ticket_response(ticket_id, complexity) -> str:
    """Format ticket creation response"""
    content = f"""
Support ticket created successfully! We send a mail to your email address with the ticket details.

Ticket ID: {ticket_id}
Priority: {complexity["priority"]}

Our support team will contact you within:
- High priority: 2-4 hours
- Medium priority: 4-8 hours

Is there anything else I can help you with?
    """.strip()

    return content


@tool
def support_agent(query: str) -> str:
    """
    Process and respond to Support related queries.
    It will analyze the complexity of the query and decide whether to create a support ticket or provide a general response.

    Args:
        query: Support related question or request

    Returns:
        A helpful response addressing the Support query.
    """
    formatted_query = f"""Analyze and respond to this support related query: {query}"""

    try:
        complexity = _analyze_complexity(formatted_query)

        if complexity["needs_ticket"]:
            s_agent = Agent(
                model=get_model(),
                system_prompt="You are a specialized Customer Support Agent for AirlineNexus, an intelligent airline assistant system. Your role is to handle complex customer issues, create support tickets, and provide escalation management.",
                callback_handler=None,
                tools=[create_support_ticket, format_ticket_response]
            )

            response = s_agent(formatted_query)
            return str(response)
        else:
            return "Not required to create a support ticket. You can give a general response to the user."
    except Exception as e:
        return f"Error processing your policy related query: {str(e)}"
