from google.adk.agents import LlmAgent
from agents.creation_agent import generate_customer_data
from agents import creation_agent
from agents import query_agent
from agents.query_agent import query_data

# --- Root Agent Definition ---
# This is the main agent that orchestrates tasks.
# root_agent = LlmAgent(
#     name='data_orchestrator_agent',
#     model='gemini-2.5-flash',
#     description='A helpful assistant for generating and querying customer data.',
#     instruction="""You are a powerful and autonomous data assistant. Your goal is to answer user questions about customer data, handling all necessary steps automatically.

# - If the user asks a question that requires data (e.g., "how many customers...", "what is the credit limit of..."), you MUST follow these steps in order:
#   1. Call the `generate_customer_data` tool to get the dataset.
#   2. Call the `query_data` tool, using the output from the first step as the `data` parameter and the user's original question as the `question` parameter.
#   3. Provide the final answer from the `query_data` tool to the user.

# - If the user simply asks to 'generate data', use only the `generate_customer_data` tool and show the result to the user.
# - If the user simply asks to get the customer data, use only the `query_data` tool and show the result to the user.
# - Do not ask for permission to generate data; do it automatically as part of the process to answer the question.
# """,
#     # The tools list contains the functions the agent can call.
#     tools=[
#         generate_customer_data,
#         query_data
#     ]
# )
root_agent = LlmAgent(
    name='data_orchestrator_agent',
    model='gemini-2.5-flash',
    description='A helpful assistant for querying customer data.',
    instruction = """
If the user asks to 'generate data', use only the `generate_customer_data` tool and show the result to the user.
If the user asks to 'get the customer data', use only the `query_data` tool and show the result to the user.
""",
tools = [generate_customer_data, query_data])