python main.py# CaseStudyAgent

A multi-agent system that uses LangChain and Azure OpenAI to answer questions about sales and customer data via Databricks Genie.

## Features

- **Sales Agent** - Query sales data including revenue, products, regional performance, and trends
- **Customer Agent** - Query customer data including segments, churn risk, LTV, and demographics
- **Intelligent Routing** - Automatically routes questions to the appropriate agent
- **Multi-tool Support** - Can use multiple agents for cross-domain questions

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Coordinator                          │
│              (LangChain ReAct Agent)                    │
│                   Azure OpenAI                          │
└─────────────────┬───────────────────┬───────────────────┘
                  │                   │
        ┌─────────▼─────────┐ ┌───────▼─────────┐
        │   Sales Agent     │ │ Customer Agent  │
        │   (Genie Tool)    │ │  (Genie Tool)   │
        └─────────┬─────────┘ └───────┬─────────┘
                  │                   │
        ┌─────────▼─────────┐ ┌───────▼─────────┐
        │  Databricks Genie │ │ Databricks Genie│
        │   (Sales Space)   │ │ (Customer Space)│
        └───────────────────┘ └─────────────────┘
```

## Prerequisites

- Python 3.10+
- Azure OpenAI account with a deployed model
- Databricks workspace with Genie spaces configured

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sarah121112/CaseStudyAgent.git
   cd CaseStudyAgent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your credentials:
   - `DATABRICKS_HOST` - Your Databricks workspace URL
   - `DATABRICKS_TOKEN` - Your Databricks personal access token
   - `SALES_SPACE_ID` - Genie space ID for sales data
   - `CUSTOMER_SPACE_ID` - Genie space ID for customer data
   - `AZURE_OPENAI_API_KEY` - Your Azure OpenAI API key
   - `AZURE_OPENAI_DEPLOYMENT` - Your Azure OpenAI deployment name
   - `AZURE_OPENAI_ENDPOINT` - Your Azure OpenAI endpoint URL

## Usage

Run the interactive agent:

```bash
python main.py
```

Example questions:
- "What are the top selling products?"
- "Which customers have the highest churn risk?"
- "Compare sales performance across regions"
- "What is the average customer lifetime value by segment?"

Type `exit` or `quit` to stop.

## Project Structure

```
CaseStudyAgent/
├── main.py              # Entry point - interactive CLI
├── config.py            # Configuration and environment variables
├── genie_client.py      # Databricks Genie API client
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment configuration
├── .gitignore           # Git ignore rules
└── agents/
    ├── __init__.py      # Package exports
    ├── coordinator.py   # Main agent coordinator
    ├── sales_agent.py   # Sales data tools
    └── customer_agent.py # Customer data tools
```

## Configuration

| Variable | Description |
|----------|-------------|
| `DATABRICKS_HOST` | Databricks workspace URL |
| `DATABRICKS_TOKEN` | Databricks personal access token |
| `SALES_SPACE_ID` | Genie space ID for sales queries |
| `CUSTOMER_SPACE_ID` | Genie space ID for customer queries |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key |
| `AZURE_OPENAI_DEPLOYMENT` | Azure OpenAI model deployment name |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL |
| `AZURE_API_VERSION` | Azure OpenAI API version (default: 2025-01-01-preview) |

## License

MIT License - see [LICENSE](LICENSE) for details.
