"""
Interactive SQL Query Generator CLI
"""
from my_agent.agent import root_agent

def main():
    """Interactive CLI for SQL query generation"""
    
    print("=" * 70)
    print("  🤖 SQL Query Generator - Interactive Mode")
    print("=" * 70)
    print("\nDatabase: customer_inventory")
    print("Table: customers_billing")
    print("\nAvailable columns:")
    print("  • customer_id, customer_name, credit_limit")
    print("  • customer_addr, customer_email")
    print("  • billing_date, due_date, billing_cycle, country")
    print("\nType your request in natural language, or 'quit' to exit.")
    print("=" * 70)
    
    while True:
        print("\n")
        user_input = input("💬 You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
            
        if not user_input:
            continue
        
        try:
            # Generate SQL query using the agent
            response = root_agent.send_message(user_input)
            
            print(f"\n🔍 Generated SQL Query:")
            print(f"{'─' * 70}")
            print(f"{response}")
            print(f"{'─' * 70}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
