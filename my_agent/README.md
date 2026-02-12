# SQL Query Generator Agent

An intelligent agent that converts natural language to PostgreSQL queries using Google ADK and Gemini.

## Overview

This agent understands your database schema and generates accurate PostgreSQL queries based on natural language input.

**Database:** `customer_inventory`  
**Table:** `customers_billing`

### Columns
- `customer_id` - Unique customer identifier
- `customer_name` - Customer name
- `credit_limit` - Credit limit
- `customer_addr` - Customer address
- `customer_email` - Email address
- `billing_date` - Billing date
- `due_date` - Payment due date
- `billing_cycle` - Billing cycle
- `country` - Country

## Files

- **`agent.py`** - Main agent configuration with SQL query generation logic (requires API)
- **`fetch.py`** - Original sample code for database connection
- **`test_agent.py`** - Automated tests with predefined queries (requires API)
- **`interactive_query_generator.py`** - Interactive CLI for query generation only (requires API)
- **`query_executor.py`** - Full solution: generates and executes queries (requires API)
- **`offline_query_generator.py`** - ⭐ Pattern-based query generator (NO API required!)
- **`hybrid_query_generator.py`** - ⭐ Auto-fallback: AI when available, offline when quota exceeded

## Usage

### ⭐ RECOMMENDED: Hybrid Mode (Works Even Without API Quota)

```bash
python my_agent/hybrid_query_generator.py
```

**Features:**
- Tries AI (Gemini) first
- Automatically switches to offline mode if quota exceeded
- Generates and executes queries
- Best of both worlds!

**Example:**
```
💬 You: list customers with credit limit over 5000
⚙️  Generating SQL query...
⚠️  API Quota Exceeded - Switching to OFFLINE mode
🔍 Generated SQL Query:
SELECT * FROM customers_billing WHERE credit_limit > 5000;
```

### 🔧 Offline Mode Only (No API Required)

```bash
python my_agent/offline_query_generator.py
```

Perfect when:
- API quota is exhausted
- No internet connection
- Testing query patterns
- Learning SQL

### 1. Query Generation Only (Requires API)

```bash
python interactive_query_generator.py
```

**Example:**
```
💬 You: list all users
🔍 Generated SQL Query:
SELECT * FROM customers_billing;
```

### 2. Query Generation + Execution

```bash
python query_executor.py
```

This will:
1. Take your natural language input
2. Generate the SQL query
3. Ask for confirmation
4. Execute the query
5. Display results in a formatted table

### 3. Run Automated Tests

```bash
python test_agent.py
```

### 4. Use the Agent Programmatically

```python
from agent import root_agent

# Generate a query
user_request = "show customers from India"
sql_query = root_agent.send_message(user_request)
print(sql_query)
```

## Example Queries

| Natural Language Input | Generated SQL |
|------------------------|---------------|
| "list all users" | `SELECT * FROM customers_billing;` |
| "show me customers from USA" | `SELECT * FROM customers_billing WHERE country = 'USA';` |
| "get customer with ID CUST019" | `SELECT * FROM customers_billing WHERE customer_id = 'CUST019';` |
| "show customer names and emails" | `SELECT customer_name, customer_email FROM customers_billing;` |
| "find customers with credit limit over 5000" | `SELECT * FROM customers_billing WHERE credit_limit > 5000;` |
| "show top 10 customers" | `SELECT * FROM customers_billing LIMIT 10;` |

## Requirements

Install the required packages:

```bash
pip install google-adk psycopg2-binary tabulate
```

**Note:** `tabulate` is optional - the query executor will work without it using simple formatting.

## Verified Google ADK Imports

✅ **Working:**
- `from google.adk.agents.llm_agent import Agent`

The agent uses instruction-based configuration rather than function declarations.

## Database Configuration

Database credentials are stored in `agent.py`:

```python
DB_CONFIG = {
    "host": "34.63.63.212",
    "database": "customer_inventory",
    "user": "app-user",
    "password": "Bhavya@12$",
    "port": 5432
}
```

⚠️ **Security Note:** In production, use environment variables for credentials!

## Features

✅ Natural language to SQL conversion  
✅ Understands database schema  
✅ Generates safe, read-only queries by default  
✅ Interactive CLI mode  
✅ Query execution with confirmation  
✅ Formatted result display  
✅ Dynamic schema fetching

## Safety

- By default, only SELECT queries are generated
- Execution requires user confirmation
- Uses parameterized queries to prevent SQL injection
- Schema validation before query generation

## Extending the Agent

To add more tables or update schema:

1. Update `DATABASE_SCHEMA` in `agent.py`
2. Modify the `get_table_schema()` function to include new tables
3. Update the agent's instructions with new table information

## Tips

- Be specific with your requests for better results
- Mention column names when you need specific fields
- Use filtering keywords like "from", "where", "with"
- Ask for "top N" or "limit N" for large datasets

## Troubleshooting

**Connection Issues:**
- Verify database credentials in `agent.py`
- Check network access to the database host
- Ensure PostgreSQL port 5432 is accessible

**Query Generation Issues:**
- Make requests more specific
- Reference actual column names from the schema
- Check that table name is correct

## License

MIT
