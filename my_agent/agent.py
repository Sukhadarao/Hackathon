# Google ADK imports
from google.adk.agents.llm_agent import Agent
from google.genai import types

# Database imports
import psycopg2
from typing import Dict, List, Optional, Any

# Database configuration
DB_CONFIG = {
    "host": "34.63.63.212",
    "database": "customer_inventory",
    "user": "app-user",
    "password": "Bhavya@12$",
    "port": 5432
}

# Database schema information
DATABASE_SCHEMA = """
Database: customer_inventory
Table: customers_billing

Columns:
- customer_id (VARCHAR): Unique identifier for customers (e.g., 'CUST019')
- customer_name (VARCHAR): Name of the customer
- credit_limit (NUMERIC): Credit limit for the customer
- customer_addr (TEXT): Customer address
- customer_email (VARCHAR): Customer email address
- billing_date (DATE): Billing date
- due_date (DATE): Payment due date
- billing_cycle (VARCHAR): Billing cycle period
- country (VARCHAR): Customer's country
"""

def get_table_schema():
    """Function to fetch current database schema dynamically"""
    conn = None
    cur = None
    schema_info = {}
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Get column information
        cur.execute("""
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns
            WHERE table_name = 'customers_billing'
            ORDER BY ordinal_position;
        """)
        
        columns = cur.fetchall()
        schema_info['table'] = 'customers_billing'
        schema_info['columns'] = [
            {
                'name': col[0], 
                'type': col[1],
                'max_length': col[2]
            } 
            for col in columns
        ]
        
        return schema_info
        
    except Exception as e:
        print(f"Error fetching schema: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# SQL Query Generator Agent with retry configuration
root_agent = Agent(
    model='gemini-2.5-flash',
    name='sql_query_generator',
    description='An intelligent SQL query generator that converts natural language to PostgreSQL queries.',
    instruction=f"""You are an expert PostgreSQL query generator. Your job is to convert user's natural language requests into valid PostgreSQL queries.

{DATABASE_SCHEMA}

RULES:
1. Generate ONLY the SQL query without any explanation unless asked
2. Use proper PostgreSQL syntax
3. Always use table name 'customers_billing'
4. For "list" or "show" requests, use SELECT statements
5. Use WHERE clauses for filtering (e.g., by country, customer_id)
6. Use LIMIT when appropriate for large result sets
7. Always use parameterized queries format with %s for values that should be parameterized
8. Return queries that are safe and read-only (SELECT only) unless specifically asked for INSERT/UPDATE/DELETE

EXAMPLES:
User: "list all users"
Response: SELECT * FROM customers_billing;

User: "show me customers from USA"
Response: SELECT * FROM customers_billing WHERE country = 'USA';

User: "get customer with ID CUST019"
Response: SELECT * FROM customers_billing WHERE customer_id = 'CUST019';

User: "show customer names and emails"
Response: SELECT customer_name, customer_email FROM customers_billing;

User: "find customers with credit limit over 5000"
Response: SELECT * FROM customers_billing WHERE credit_limit > 5000;

Now, generate SQL queries based on user input. Output ONLY the SQL query unless the user asks for explanation.
""",
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            # Retry configuration to handle quota limits (429 errors)
            retry_options=types.HttpRetryOptions(
                initial_delay=2,  # Start with 2 second delay
                attempts=3        # Retry up to 3 times
            )
        )
    )
)
