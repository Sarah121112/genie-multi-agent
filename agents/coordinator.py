"""Coordinator agent using LangChain + LangGraph with Azure OpenAI."""
from pydantic import SecretStr
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent  # type: ignore

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
Your goal is to provide SPECIFIC, DATA-DRIVEN answers with exact numbers and actionable insights.

Available data:
- sales_transactions columns: date, product, category, revenue, region
- customer_behavior columns: customer_id, segment, lifetime_value, churn_risk, region

Tools:
- sales_genie: Query for sales, revenue, products, categories, regions, and trends
- customer_genie: Query for customer segments, churn_risk, lifetime_value, and regions

CRITICAL RULES FOR SPECIFIC ANSWERS:
1. ALWAYS ask clarifying questions BEFORE answering if the user doesn't specify:
   - Exact timeframe (e.g., "January 2026", "last 30 days", "Q4 2025")
   - Specific metric (e.g., "total revenue", "average order value per customer", "top 5 products")
   - Specific segments (e.g., "Premium vs Standard customers", "specific regions", "high churn risk only")
   - Exact threshold definitions (e.g., what counts as "high" revenue/churn for them)

2. STRUCTURE your response with:
   - Direct answer with specific numbers (e.g., "$2.4M revenue", "42% churn rate", "Top 3 products: X, Y, Z")
   - Breakdown by relevant dimensions (by region, by segment, by category)
   - Key insights and patterns (e.g., "North region shows 15% growth vs 5% overall")
   - Comparison context (e.g., "This is 23% higher than last period")
   - Actionable recommendations based on the data

3. For combined questions (sales + customer), call BOTH tools and create an integrated analysis.

4. Never make assumptions. Ask exactly ONE clarifying question when details are missing.

5. Never mention fields that do not exist: orders, AOV, channels, loyalty tiers, subscriptions, conversions, demographics beyond region.

EXAMPLE FORMAT:
Question: "What about sales?"
Response: "I need more specifics to give you a detailed answer. Could you clarify: Are you asking about total revenue by region, product performance, or sales trends? And what timeframe interests you - last month, this quarter, or year-to-date?"
"""


def build_coordinator():
    """Build a multi-agent coordinator as a ReAct agent."""
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

    return create_react_agent(
        llm,
        tools,
        prompt=SYSTEM_PROMPT,
    )
