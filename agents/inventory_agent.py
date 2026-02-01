from pydantic import SecretStr
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent

from config import (
    INVENTORY_SPACE_ID,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
    AZURE_API_VERSION,
)
from genie_client import ask_genie


def get_inventory_tools():
    if not INVENTORY_SPACE_ID:
        raise ValueError("INVENTORY_SPACE_ID not configured")

    space_id = INVENTORY_SPACE_ID

    @tool
    def inventory_genie(question: str) -> str:
        """Query inventory metrics from the Inventory Genie space."""
        return ask_genie(space_id, question)

    return [inventory_genie]


INVENTORY_SYSTEM_PROMPT = """You are the Inventory Agent.
You ONLY answer using the inventory_genie tool and the inventory table.

If a user asks for anything outside inventory analytics, say:
"I can only answer inventory questions."

When you need exact numbers, ALWAYS call inventory_genie.
Return stock levels, reorder risk, and summaries clearly.
"""


def build_inventory_agent():
    api_key = SecretStr(AZURE_OPENAI_API_KEY) if AZURE_OPENAI_API_KEY else None

    llm = AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        api_version=AZURE_API_VERSION,
        api_key=api_key,
        max_retries=3,
    )

    tools = get_inventory_tools()

    return create_react_agent(
        llm,
        tools,
        prompt=INVENTORY_SYSTEM_PROMPT,
    )
