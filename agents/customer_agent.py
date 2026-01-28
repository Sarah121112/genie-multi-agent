"""Customer agent tools for querying customer data."""
from langchain_core.tools import tool
from config import CUSTOMER_SPACE_ID
from genie_client import ask_genie


def get_customer_tools():
    """Get customer-related tools for the agent."""
    
    if not CUSTOMER_SPACE_ID:
        raise ValueError("CUSTOMER_SPACE_ID not configured")
    
    space_id = CUSTOMER_SPACE_ID  # Capture for closure with confirmed type
    
    @tool
    def customer_genie(question: str) -> str:
        """Query customer data from Databricks.
        
        Use this tool for questions about:
        - Customer segments and demographics
        - Churn risk and retention analysis
        - Customer lifetime value (LTV/CLV)
        - Customer geographic distribution
        - Customer behavior patterns
        
        Args:
            question: A natural language question about customer data
            
        Returns:
            Answer from the customer data warehouse
        """
        return ask_genie(space_id, question)

    return [customer_genie]
