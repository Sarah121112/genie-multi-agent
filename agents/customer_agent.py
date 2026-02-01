from pydantic import SecretStr
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent

from config import (
    CUSTOMER_SPACE_ID,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
    AZURE_API_VERSION,
)
from genie_client import ask_genie


def get_customer_tools():
    if not CUSTOMER_SPACE_ID:
        raise ValueError("CUSTOMER_SPACE_ID not configured")

    space_id = CUSTOMER_SPACE_ID

    @tool
    def customer_genie(question: str) -> str:
        """Query customer analytics from the Customer Genie space."""
        return ask_genie(space_id, question)

    return [customer_genie]


CUSTOMER_SYSTEM_PROMPT = """You are the Customer Agent.
You ONLY answer using the customer_genie tool and the customer_behavior table.

If a user asks for anything outside customer analytics, say:
"I can only answer customer questions."

When you need exact numbers, ALWAYS call customer_genie.
Return segmentation, churn, and LTV metrics clearly.
"""


def build_customer_agent():
    api_key = SecretStr(AZURE_OPENAI_API_KEY) if AZURE_OPENAI_API_KEY else None

    llm = AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        api_version=AZURE_API_VERSION,
        api_key=api_key,
        max_retries=3,
    )

    tools = get_customer_tools()

    return create_react_agent(
        llm,
        tools,
        prompt=CUSTOMER_SYSTEM_PROMPT,
    )
