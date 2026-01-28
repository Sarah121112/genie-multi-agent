"""Sales agent tools for querying sales and revenue data."""
from langchain_core.tools import tool
from config import SALES_SPACE_ID
from genie_client import ask_genie


def get_sales_tools():
    """Get sales-related tools for the agent."""
    
    if not SALES_SPACE_ID:
        raise ValueError("SALES_SPACE_ID not configured")
    
    space_id = SALES_SPACE_ID  # Capture for closure with confirmed type
    
    @tool
    def sales_genie(question: str) -> str:
        """Query sales and revenue data from Databricks.
        
        Use this tool for questions about:
        - Sales figures, revenue, and transactions
        - Product performance and categories
        - Regional sales breakdown
        - Sales trends and comparisons
        - Top/bottom performing products
        
        Args:
            question: A natural language question about sales data
            
        Returns:
            Answer from the sales data warehouse
        """
        return ask_genie(space_id, question)

    return [sales_genie]
