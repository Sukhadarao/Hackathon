"""
SQL Query Generator Agent Module

A natural language to SQL query generator using Google ADK.
"""

from .agent import root_agent, get_table_schema, DB_CONFIG

__version__ = "1.0.0"
__all__ = ['root_agent', 'get_table_schema', 'DB_CONFIG']
