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
        """Query customer data from Databricks for specific insights.
        
        Use this tool for questions about:
        - Customer segmentation with exact counts and percentages
        - Churn risk breakdown by segment with specific percentages
        - Customer lifetime value (LTV) by segment with exact values
        - Geographic distribution with specific numbers per region
        - Behavior patterns with quantified metrics
        
        Always provide exact numbers, percentages, and segment comparisons in your question.
        Specify which segments or regions to analyze and desired metrics.
        
        Args:
            question: A specific, detailed question about customer data
            
        Returns:
            Specific customer metrics and data from the warehouse
        """
        return ask_genie(space_id, question)

    return [customer_genie]
