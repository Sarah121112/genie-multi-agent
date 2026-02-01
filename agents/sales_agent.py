from pydantic import SecretStr
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent

from config import (
    SALES_SPACE_ID,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
    AZURE_API_VERSION,
)
from genie_client import ask_genie


def get_sales_tools():
    if not SALES_SPACE_ID:
        raise ValueError("SALES_SPACE_ID not configured")

    space_id = SALES_SPACE_ID

    @tool
    def sales_genie(question: str) -> str:
        """Query sales and revenue data from the Sales Genie space."""
        return ask_genie(space_id, question)

    return [sales_genie]


SALES_SYSTEM_PROMPT = """You are the Sales Agent.
You ONLY answer using the sales_genie tool and the sales_transactions table.

If a user asks for anything outside sales analytics, say:
"I can only answer sales questions."

When you need exact numbers, ALWAYS call sales_genie.
Return clear metrics and simple breakdowns.
"""


def build_sales_agent():
    api_key = SecretStr(AZURE_OPENAI_API_KEY) if AZURE_OPENAI_API_KEY else None

    llm = AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        api_version=AZURE_API_VERSION,
        api_key=api_key,
        max_retries=3,
    )

    tools = get_sales_tools()

    return create_react_agent(
        llm,
        tools,
        prompt=SALES_SYSTEM_PROMPT,
    )
