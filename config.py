import os
from dotenv import load_dotenv

load_dotenv()

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", "2025-01-01-preview")

# Databricks Configuration
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")

# Genie Configuration
SALES_SPACE_ID = os.getenv("SALES_SPACE_ID")
CUSTOMER_SPACE_ID = os.getenv("CUSTOMER_SPACE_ID")


def validate_config():
    """Validate that all required environment variables are set."""
    required = {
        "AZURE_OPENAI_API_KEY": AZURE_OPENAI_API_KEY,
        "DATABRICKS_HOST": DATABRICKS_HOST,
        "DATABRICKS_TOKEN": DATABRICKS_TOKEN,
        "SALES_SPACE_ID": SALES_SPACE_ID,
        "CUSTOMER_SPACE_ID": CUSTOMER_SPACE_ID,
        "AZURE_OPENAI_ENDPOINT": AZURE_OPENAI_ENDPOINT,
    }
    
    missing = [key for key, value in required.items() if not value]
    if missing:
        raise ValueError(f"Missing environment variables: {', '.join(missing)}")



