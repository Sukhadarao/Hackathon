"""
Quick Start Guide - SQL Query Generator Agent

This script demonstrates the basic usage of the SQL Query Generator.
"""

# Example 1: Simple query generation
print("=" * 70)
print("Example 1: Basic Query Generation")
print("=" * 70)

from my_agent import root_agent

query1 = "list all users"
result1 = root_agent.send_message(query1)
print(f"\nInput: {query1}")
print(f"Output: {result1}\n")

# Example 2: Filtered query
query2 = "show customers from USA"
result2 = root_agent.send_message(query2)
print(f"Input: {query2}")
print(f"Output: {result2}\n")

# Example 3: Specific columns
query3 = "get customer names and emails only"
result3 = root_agent.send_message(query3)
print(f"Input: {query3}")
print(f"Output: {result3}\n")

# Example 4: With conditions
query4 = "find customers with credit limit greater than 10000"
result4 = root_agent.send_message(query4)
print(f"Input: {query4}")
print(f"Output: {result4}\n")

print("=" * 70)
print("✅ Quick Start Complete!")
print("=" * 70)
print("\nNext steps:")
print("1. Try: python interactive_query_generator.py")
print("2. Or: python query_executor.py (to execute queries)")
print("3. Or: python test_agent.py (to run all tests)")
