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
        """Query sales and revenue data from Databricks for specific metrics.
        
        Use this tool for questions about:
        - Specific revenue figures by region, product, or category
        - Top/bottom N performing products with exact revenue numbers
        - Sales trends with period-over-period comparisons
        - Revenue breakdown by dimension (region, category, product)
        - Growth rates and percentage changes
        
        Always provide exact numbers and comparisons in your question.
        Include timeframe (e.g., "January 2026", "last quarter") and metric details.
        
        Args:
            question: A specific, detailed question about sales data
            
        Returns:
            Specific sales metrics and data from the warehouse
        """
        return ask_genie(space_id, question)

    return [sales_genie]
