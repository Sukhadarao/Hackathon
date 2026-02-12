"""
SQL Query Generator with Execution
This module generates and executes PostgreSQL queries from natural language input.
"""
from my_agent.agent import root_agent, DB_CONFIG
import psycopg2
try:
    from tabulate import tabulate
except ImportError:
    print("Warning: tabulate not installed. Install with: pip install tabulate")
    tabulate = None

def execute_query(sql_query):
    """Execute a SQL query and return results"""
    conn = None
    cur = None
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Execute the query
        cur.execute(sql_query)
        
        # Fetch results
        results = cur.fetchall()
        
        # Get column names
        if cur.description:
            columns = [desc[0] for desc in cur.description]
            return columns, results
        else:
            return None, None
            
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        return None, None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def generate_and_execute(user_input):
    """Generate SQL query from natural language and execute it"""
    
    print(f"\n💬 User Request: {user_input}")
    print("=" * 70)
    
    # Generate SQL query
    print("\n⚙️  Generating SQL query...")
    sql_query = root_agent.send_message(user_input)
    
    print(f"\n🔍 Generated SQL Query:")
    print(f"{'─' * 70}")
    print(sql_query)
    print(f"{'─' * 70}")
    
    # Ask for confirmation before executing
    confirm = input("\n▶️  Execute this query? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Query execution cancelled.")
        return
    
    # Execute the query
    print("\n⏳ Executing query...")
    columns, results = execute_query(sql_query)
    
    if columns and results:
        print(f"\n✅ Query executed successfully! ({len(results)} rows)")
        print("\n📊 Results:")
        
        # Use tabulate if available, otherwise simple formatting
        if tabulate:
            print(tabulate(results, headers=columns, tablefmt='grid'))
        else:
            # Simple fallback formatting
            print(" | ".join(columns))
            print("-" * 70)
            for row in results:
                print(" | ".join(str(val) for val in row))
    elif columns and not results:
        print("\n✅ Query executed successfully! (0 rows returned)")
    else:
        print("\n❌ No results or error occurred.")

def interactive_mode():
    """Interactive mode with query generation and execution"""
    
    print("=" * 70)
    print("  🤖 SQL Query Generator & Executor - Interactive Mode")
    print("=" * 70)
    print("\nDatabase: customer_inventory")
    print("Table: customers_billing")
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
            generate_and_execute(user_input)
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    # Example usage
    print("Choose mode:")
    print("1. Interactive mode (recommended)")
    print("2. Single query mode")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == '1':
        interactive_mode()
    else:
        user_query = input("\nEnter your request: ").strip()
        if user_query:
            generate_and_execute(user_query)
