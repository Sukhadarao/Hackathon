from google.adk.agents import LlmAgent, Agent

# This is the core instruction for the agent.
# It uses placeholders {question} and {data} that can be filled in at runtime.
data = [
  {
    "CustomerID": "CUST001",
    "Customer Name": "John Miller",
    "credit_limit": 4500,
    "Customer_addr": "123 Maple Street, Denver, CO 80203",
    "customer_email": "john.miller@example.com",
    "Due_date": "2026-03-15",
    "Billing_date": "2026-01-30",
    "Billing_cycle": 45,
    "Country": "United States"
  },
  {
    "CustomerID": "CUST002",
    "Customer Name": "Sarah Johnson",
    "credit_limit": 12000,
    "Customer_addr": "456 Oak Avenue, Austin, TX 73301",
    "customer_email": "sarah.johnson@example.com",
    "Due_date": "2026-04-10",
    "Billing_date": "2026-02-24",
    "Billing_cycle": 45,
    "Country": "India"
  },
  {
    "CustomerID": "CUST003",
    "Customer Name": "Michael Brown",
    "credit_limit": 75000,
    "Customer_addr": "789 Pine Road, Seattle, WA 98101",
    "customer_email": "michael.brown@example.com",
    "Due_date": "2026-02-28",
    "Billing_date": "2026-01-13",
    "Billing_cycle": 45,
    "Country": "United Kingdom"
  }
]
from google.adk.agents import LlmAgent

_QUERY_AGENT_INSTRUCTION_TEMPLATE = """
You are an expert data analyst. Your task is to answer a question based on the provided JSON dataset.
Analyze the data carefully and provide a clear, concise answer.
If the answer cannot be found in the data, state that clearly. Do not make up information.

Data:
{data}

Question:
{question}
"""

def query_data(data: str, question: str) -> str:
    """
    Answers a question based on a given dataset in JSON format.

    Args:
        data: A string containing the JSON data to be queried.
        question: The question to ask about the data.

    Returns:
        The agent's answer.
    """
    # Format the prompt with the specific data and question for this query
    prompt = _QUERY_AGENT_INSTRUCTION_TEMPLATE.format(data=data, question=question)

query_agent = Agent(
    name="data_query_agent",
    model="gemini-1.5-flash",
    description="Answers questions based on a provided {data}.",
    instruction="You are a data analyst. You will be provided with a {data} and a question.",
)
# Expose the agent as the root_agent for this module if needed for standalone testing
root_agent = query_agent