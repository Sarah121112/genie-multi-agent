import sqlite3
from pydantic import SecretStr
from langchain_core.tools import tool
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver

from config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
    AZURE_API_VERSION,
    validate_config,
)

from agents.sales_agent import build_sales_agent
from agents.customer_agent import build_customer_agent
from agents.inventory_agent import build_inventory_agent


SYSTEM_PROMPT = """You are the Coordinator Agent responsible for answering business questions.

You can query:
- Sales data (revenue, growth, product performance)
- Customer data (segmentation, churn, lifetime value)
- Inventory data (stock, reorder risk)

You have access to three specialist agents:
- sales_agent: use for sales metrics and revenue questions
- customer_agent: use for customer segmentation/churn/LTV questions
- inventory_agent: use for stock levels and reorder risk questions

Use tools whenever exact data or metrics are required.
If a question combines domains, call multiple agents and synthesize.
If a question is outside these domains, say so clearly.
"""


def build_coordinator(db_path: str = "checkpoints.sqlite"):
    validate_config()

    api_key = SecretStr(AZURE_OPENAI_API_KEY) if AZURE_OPENAI_API_KEY else None

    llm = AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        api_version=AZURE_API_VERSION,
        api_key=api_key,
        max_retries=3,
    )

    sales_agent_graph = build_sales_agent()
    customer_agent_graph = build_customer_agent()
    inventory_agent_graph = build_inventory_agent()

    @tool
    def sales_agent(question: str) -> str:
        """Ask the Sales Agent to answer a sales analytics question."""
        result = sales_agent_graph.invoke({"messages": [("user", question)]})
        messages = result.get("messages", [])
        return messages[-1].content if messages else "(no response)"

    @tool
    def customer_agent(question: str) -> str:
        """Ask the Customer Agent to answer a customer analytics question."""
        result = customer_agent_graph.invoke({"messages": [("user", question)]})
        messages = result.get("messages", [])
        return messages[-1].content if messages else "(no response)"

    @tool
    def inventory_agent(question: str) -> str:
        """Ask the Inventory Agent to answer an inventory analytics question."""
        result = inventory_agent_graph.invoke({"messages": [("user", question)]})
        messages = result.get("messages", [])
        return messages[-1].content if messages else "(no response)"

    tools = [sales_agent, customer_agent, inventory_agent]

    conn = sqlite3.connect(db_path, check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    checkpointer.setup()

    return create_react_agent(
        llm,
        tools,
        prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )
