"""Coordinator agent using LangChain + LangGraph with Azure OpenAI."""
import sqlite3
from pydantic import SecretStr
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent  # type: ignore
from langgraph.checkpoint.sqlite import SqliteSaver

from config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
    AZURE_API_VERSION,
    validate_config,
)
from agents.sales_agent import get_sales_tools
from agents.customer_agent import get_customer_tools


SYSTEM_PROMPT = """You answer questions using ONLY the available data and the two tools.
Your goal is to provide DATA-DRIVEN answers with exact numbers and actionable insights.

Available data:
- sales_transactions columns: date, product, category, revenue, region
- customer_behavior columns: customer_id, segment, lifetime_value, churn_risk, region

Tools:
- sales_genie: Query for sales, revenue, products, categories, regions, and trends
- customer_genie: Query for customer segments, churn_risk, lifetime_value, and regions

DEFAULT VALUES (use when user doesn't specify):
- Timeframe: "full available period"
- Sales metric: "total revenue"
- Customer metric: "customer segments and churn risk breakdown"
- Segments: all available regions and segments
- Dimensions: breakdown by region, by segment, by category
   
RESPONSE RULES:
1. ALWAYS provide an answer using defaults above for any unspecified aspect.
   
2. STRUCTURE your response with:
   - Direct answer with specific numbers (e.g., "$2.4M revenue", "42% churn rate")
   - Breakdown by relevant dimensions (by region, by segment, by category)
   - Key insights and patterns
   - Actionable recommendations based on the data

3. For combined questions (sales + customer), call BOTH tools and integrate results.

4. Never mention fields that do not exist: orders, AOV, channels, loyalty tiers, subscriptions, conversions, demographics beyond region.
"""


def build_coordinator(db_path: str = "checkpoints.sqlite"):
    """Build a multi-agent coordinator as a ReAct agent with SQLite memory."""
    validate_config()

    api_key = SecretStr(AZURE_OPENAI_API_KEY) if AZURE_OPENAI_API_KEY else None

    llm = AzureChatOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT,
        api_version=AZURE_API_VERSION,
        api_key=api_key,
        max_retries=3,  # Add retry support for transient errors
    )

    tools = get_sales_tools() + get_customer_tools()

    # Setup SQLite checkpointer for conversation memory
    conn = sqlite3.connect(db_path, check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    checkpointer.setup()  # Creates tables if needed

    return create_react_agent(
        llm,
        tools,
        prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )
