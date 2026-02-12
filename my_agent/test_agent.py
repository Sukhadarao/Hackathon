"""
Test script for SQL Query Generator Agent
"""
from my_agent.agent import root_agent

def test_query_generation():
    """Test the agent with various natural language inputs"""
    
    test_queries = [
        "list all users",
        "show me customers from USA",
        "get customer with ID CUST019",
        "show customer names and emails",
        "find customers with credit limit over 5000",
        "show me top 10 customers",
        "list customers who have billing date in 2024",
        "get all customer emails from India"
    ]
    
    print("=" * 60)
    print("SQL Query Generator Agent - Test Results")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n📝 User Input: {query}")
        print("-" * 60)
        
        # Send the query to the agent
        response = root_agent.send_message(query)
        
        print(f"🔍 Generated SQL:")
        print(f"{response}")
        print("-" * 60)

if __name__ == "__main__":
    test_query_generation()
