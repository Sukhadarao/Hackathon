"""
Offline SQL Query Generator (No API Required)
Works using pattern matching and rules - no Gemini API needed!
"""
import re
from typing import Optional

# Database schema
SCHEMA = {
    'table': 'customers_billing',
    'columns': {
        'customer_id': 'VARCHAR',
        'customer_name': 'VARCHAR',
        'credit_limit': 'NUMERIC',
        'customer_addr': 'TEXT',
        'customer_email': 'VARCHAR',
        'billing_date': 'DATE',
        'due_date': 'DATE',
        'billing_cycle': 'VARCHAR',
        'country': 'VARCHAR'
    }
}

class OfflineQueryGenerator:
    """Generate SQL queries from natural language without AI"""
    
    def __init__(self):
        self.table = SCHEMA['table']
        self.columns = list(SCHEMA['columns'].keys())
    
    def generate_query(self, user_input: str) -> str:
        """Main method to generate SQL query from natural language"""
        user_input = user_input.lower().strip()
        
        # Pattern 1: List all / Show all
        if re.search(r'\b(list|show|get|fetch|display)\s+(all|everything)\b', user_input):
            return self._list_all()
        
        # Pattern 2: Specific customer by ID
        customer_id_match = re.search(r'\bcust\w*\s*[:\-]?\s*(\w+)', user_input, re.IGNORECASE)
        if customer_id_match:
            cust_id = customer_id_match.group(1)
            return self._get_by_customer_id(cust_id)
        
        # Pattern 3: Filter by country
        country_match = re.search(r'\b(?:from|in|country)\s+(\w+)', user_input)
        if country_match:
            country = country_match.group(1).upper()
            return self._filter_by_country(country)
        
        # Pattern 4: Credit limit filters
        credit_match = re.search(r'credit.*?(\d+)', user_input)
        if credit_match:
            amount = credit_match.group(1)
            if any(word in user_input for word in ['greater', 'more', 'over', 'above', '>']):
                return self._credit_greater_than(amount)
            elif any(word in user_input for word in ['less', 'under', 'below', '<']):
                return self._credit_less_than(amount)
            elif any(word in user_input for word in ['equal', 'exactly', '=']):
                return self._credit_equals(amount)
        
        # Pattern 5: Specific columns requested
        requested_cols = self._extract_columns(user_input)
        if requested_cols:
            return self._select_specific_columns(requested_cols)
        
        # Pattern 6: Top N results
        limit_match = re.search(r'(?:top|first|limit)\s+(\d+)', user_input)
        if limit_match:
            limit = limit_match.group(1)
            return self._select_with_limit(limit)
        
        # Pattern 7: By email
        if 'email' in user_input and '@' in user_input:
            email_match = re.search(r'[\w\.-]+@[\w\.-]+', user_input)
            if email_match:
                return self._filter_by_email(email_match.group(0))
        
        # Pattern 8: Date filters
        if 'billing' in user_input and 'date' in user_input:
            year_match = re.search(r'\b(20\d{2})\b', user_input)
            if year_match:
                return self._filter_by_year(year_match.group(1), 'billing_date')
        
        # Default: list all if no pattern matches
        return self._list_all()
    
    def _list_all(self) -> str:
        """Generate query to list all records"""
        return f"SELECT * FROM {self.table};"
    
    def _get_by_customer_id(self, customer_id: str) -> str:
        """Get customer by ID"""
        return f"SELECT * FROM {self.table} WHERE customer_id = '{customer_id.upper()}';"
    
    def _filter_by_country(self, country: str) -> str:
        """Filter by country"""
        return f"SELECT * FROM {self.table} WHERE country = '{country}';"
    
    def _credit_greater_than(self, amount: str) -> str:
        """Filter credit limit greater than amount"""
        return f"SELECT * FROM {self.table} WHERE credit_limit > {amount};"
    
    def _credit_less_than(self, amount: str) -> str:
        """Filter credit limit less than amount"""
        return f"SELECT * FROM {self.table} WHERE credit_limit < {amount};"
    
    def _credit_equals(self, amount: str) -> str:
        """Filter credit limit equals amount"""
        return f"SELECT * FROM {self.table} WHERE credit_limit = {amount};"
    
    def _filter_by_email(self, email: str) -> str:
        """Filter by email"""
        return f"SELECT * FROM {self.table} WHERE customer_email = '{email}';"
    
    def _filter_by_year(self, year: str, column: str) -> str:
        """Filter by year for a date column"""
        return f"SELECT * FROM {self.table} WHERE EXTRACT(YEAR FROM {column}) = {year};"
    
    def _extract_columns(self, user_input: str) -> list:
        """Extract column names from user input"""
        found_cols = []
        
        # Map common phrases to column names
        column_aliases = {
            'name': 'customer_name',
            'names': 'customer_name',
            'email': 'customer_email',
            'emails': 'customer_email',
            'address': 'customer_addr',
            'addresses': 'customer_addr',
            'credit': 'credit_limit',
            'id': 'customer_id',
            'ids': 'customer_id',
            'billing': 'billing_date',
            'due': 'due_date',
            'cycle': 'billing_cycle',
            'country': 'country',
            'countries': 'country'
        }
        
        for alias, col in column_aliases.items():
            if alias in user_input:
                if col not in found_cols:
                    found_cols.append(col)
        
        return found_cols
    
    def _select_specific_columns(self, columns: list) -> str:
        """Select only specific columns"""
        cols_str = ', '.join(columns)
        return f"SELECT {cols_str} FROM {self.table};"
    
    def _select_with_limit(self, limit: str) -> str:
        """Select with LIMIT"""
        return f"SELECT * FROM {self.table} LIMIT {limit};"


def interactive_offline_mode():
    """Run the offline query generator interactively"""
    generator = OfflineQueryGenerator()
    
    print("=" * 70)
    print("  🔧 OFFLINE SQL Query Generator (No API Required)")
    print("=" * 70)
    print("\n📌 This works WITHOUT Gemini API - uses pattern matching!")
    print("\nDatabase: customer_inventory")
    print("Table: customers_billing")
    print("\nType your request in natural language, or 'quit' to exit.")
    print("=" * 70)
    
    # Example queries
    print("\n💡 Try these examples:")
    examples = [
        "list all users",
        "show customers from USA",
        "get customer CUST019",
        "show customer names and emails",
        "find customers with credit limit over 5000",
        "top 10 customers",
        "customers with credit limit equal to 5000"
    ]
    for ex in examples:
        print(f"  • {ex}")
    print()
    
    while True:
        print()
        user_input = input("💬 You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
            
        if not user_input:
            continue
        
        try:
            # Generate SQL query
            sql_query = generator.generate_query(user_input)
            
            print(f"\n🔍 Generated SQL Query:")
            print(f"{'─' * 70}")
            print(f"{sql_query}")
            print(f"{'─' * 70}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    interactive_offline_mode()
