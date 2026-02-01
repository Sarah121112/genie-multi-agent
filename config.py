import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root explicitly (important for Streamlit on Windows)
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Azure OpenAI configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")

# Databricks Genie space IDs
SALES_SPACE_ID = os.getenv("SALES_SPACE_ID")
CUSTOMER_SPACE_ID = os.getenv("CUSTOMER_SPACE_ID")
INVENTORY_SPACE_ID = os.getenv("INVENTORY_SPACE_ID")


def validate_config() -> None:
    missing = []

    if not AZURE_OPENAI_API_KEY:
        missing.append("AZURE_OPENAI_API_KEY")
    if not AZURE_OPENAI_DEPLOYMENT:
        missing.append("AZURE_OPENAI_DEPLOYMENT")
    if not AZURE_OPENAI_ENDPOINT:
        missing.append("AZURE_OPENAI_ENDPOINT")
    if not AZURE_API_VERSION:
        missing.append("AZURE_API_VERSION")

    if not SALES_SPACE_ID:
        missing.append("SALES_SPACE_ID")
    if not CUSTOMER_SPACE_ID:
        missing.append("CUSTOMER_SPACE_ID")
    if not INVENTORY_SPACE_ID:
        missing.append("INVENTORY_SPACE_ID")

    if missing:
        raise ValueError(
            "Missing required environment variables: " + ", ".join(missing)
        )
