"""
Hybrid Query Generator with Automatic Fallback
Uses AI agent when available, switches to offline mode on quota errors
"""
from my_agent.agent import root_agent, DB_CONFIG
from my_agent.offline_query_generator import OfflineQueryGenerator
import psycopg2
import sys

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None


class HybridQueryGenerator:
    """Query generator with automatic fallback to offline mode"""
    
    def __init__(self):
        self.offline_generator = OfflineQueryGenerator()
        self.use_offline = False
        self.offline_reason = None
    
    def generate_query(self, user_input: str) -> str:
        """Generate query using AI or offline mode"""
        
        if self.use_offline:
            print(f"ℹ️  Using offline mode: {self.offline_reason}")
            return self.offline_generator.generate_query(user_input)
        
        try:
            # Try AI agent first
            query = root_agent.send_message(user_input)
            return query
            
        except Exception as e:
            error_str = str(e)
            
            # Check if it's a quota error
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                print("\n⚠️  API Quota Exceeded - Switching to OFFLINE mode")
                print("📌 Offline mode uses pattern matching (no AI required)")
                self.use_offline = True
                self.offline_reason = "API quota exhausted"
                
                # Fallback to offline
                return self.offline_generator.generate_query(user_input)
            else:
                # Re-raise other errors
                raise


def execute_query(sql_query: str):
    """Execute SQL query and return results"""
    conn = None
    cur = None
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(sql_query)
        results = cur.fetchall()
        
        if cur.description:
            columns = [desc[0] for desc in cur.description]
            return columns, results
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


def interactive_hybrid_mode():
    """Interactive mode with automatic fallback"""
    generator = HybridQueryGenerator()
    
    print("=" * 70)
    print("  🤖 HYBRID SQL Query Generator")
    print("=" * 70)
    print("\n✨ Features:")
    print("  • Uses AI (Gemini) when quota available")
    print("  • Automatically switches to offline mode on quota errors")
    print("  • Can execute queries directly on database")
    print("\nDatabase: customer_inventory")
    print("Table: customers_billing")
    print("\nCommands:")
    print("  • Type your query in natural language")
    print("  • Type 'offline' to manually switch to offline mode")
    print("  • Type 'online' to try AI mode again")
    print("  • Type 'quit' to exit")
    print("=" * 70)
    
    while True:
        print("\n")
        user_input = input("💬 You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if user_input.lower() == 'offline':
            generator.use_offline = True
            generator.offline_reason = "Manual switch"
            print("✅ Switched to OFFLINE mode")
            continue
        
        if user_input.lower() == 'online':
            generator.use_offline = False
            print("✅ Switched to ONLINE mode (will try AI)")
            continue
            
        if not user_input:
            continue
        
        try:
            # Generate SQL query
            print("\n⚙️  Generating SQL query...")
            sql_query = generator.generate_query(user_input)
            
            print(f"\n🔍 Generated SQL Query:")
            print(f"{'─' * 70}")
            print(f"{sql_query}")
            print(f"{'─' * 70}")
            
            # Ask to execute
            execute = input("\n▶️  Execute this query? (y/n): ").strip().lower()
            
            if execute == 'y':
                print("\n⏳ Executing query...")
                columns, results = execute_query(sql_query)
                
                if columns and results:
                    print(f"\n✅ Query executed successfully! ({len(results)} rows)")
                    print("\n📊 Results:")
                    
                    if tabulate:
                        print(tabulate(results, headers=columns, tablefmt='grid'))
                    else:
                        print(" | ".join(columns))
                        print("-" * 70)
                        for row in results[:10]:  # Limit display to 10 rows
                            print(" | ".join(str(val) for val in row))
                        if len(results) > 10:
                            print(f"\n... ({len(results) - 10} more rows)")
                            
                elif columns and not results:
                    print("\n✅ Query executed successfully! (0 rows returned)")
                else:
                    print("\n❌ Query execution failed")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            continue
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    interactive_hybrid_mode()
