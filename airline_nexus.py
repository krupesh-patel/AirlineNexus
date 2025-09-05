import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strands import Agent
from prompts.coordinator_prompt import COORDINATOR_SYSTEM_PROMPT
from multi_agents.flight_agent import flight_agent
from multi_agents.policy_agent import policy_agent
from multi_agents.support_agent import support_agent
from multi_agents.general_agent import generat_agent
from model.moonshot import get_model

airline_agent = Agent(
    model=get_model(),
    system_prompt=COORDINATOR_SYSTEM_PROMPT,
    callback_handler=None,
    tools=[flight_agent, policy_agent, support_agent, generat_agent]
)

if __name__ == "__main__":
    print("\n Airline Assistant Agent 📁\n")
    print("Type 'exit' to quit.")

    # Interactive loop
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == "exit":
                print("\nGoodbye! 👋")
                break

            response = airline_agent(
                user_input,
            )

            # Extract and print only the relevant content from the specialized agent's response
            content = str(response)
            print(content)

        except KeyboardInterrupt:
            print("\n\nExecution interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try asking a different question.")
