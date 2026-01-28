"""Coordinator agent using LangChain with Azure OpenAI."""
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent  # type: ignore
from pydantic import SecretStr

from config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
    AZURE_API_VERSION,
    validate_config,
)
from agents.sales_agent import get_sales_tools
from agents.customer_agent import get_customer_tools


SYSTEM_PROMPT = """You are a helpful assistant that answers questions about sales and customer data.
You have access to two specialized tools:
1. sales_genie - for sales, revenue, products, and performance questions
2. customer_genie - for customer segments, churn, LTV, and demographics

Use these tools to fetch data, then provide clear and comprehensive answers.
If a question spans both domains, use both tools and combine the results."""


def build_coordinator():
    """Build a multi-agent coordinator using LangChain ReAct agent with Azure OpenAI.
    
    Returns:
        A compiled LangGraph state graph configured as a ReAct agent
        
    Raises:
        ValueError: If required environment variables are missing
    """
    # Validate configuration before building
    validate_config()
    
    # Convert API key to SecretStr for LangChain compatibility
    api_key = SecretStr(AZURE_OPENAI_API_KEY) if AZURE_OPENAI_API_KEY else None
    
    # Initialize Azure OpenAI LLM (gpt-5 only supports default temperature)
    llm = AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        api_version=AZURE_API_VERSION,
        api_key=api_key,
    )

    # Gather tools from agent modules
    tools = get_sales_tools() + get_customer_tools()

    # Create a ReAct agent with tools
    agent = create_react_agent(
        llm,
        tools,
        prompt=SYSTEM_PROMPT,
    )
    
    return agent
