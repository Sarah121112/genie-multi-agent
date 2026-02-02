# Multi-Agent System with Databricks Genie

A production-grade multi-agent system using **LangChain** and **Azure OpenAI** to orchestrate queries across **three Databricks Genie workspaces** (Sales Analytics, Customer Insights, Inventory Management). The coordinator synthesizes cross-domain insights through intelligent agent routing and conversation memory.

## Features

- **3 Specialized Agents:**
  - **Sales Agent** – Revenue, products, categories, regional performance, growth trends
  - **Customer Agent** – Segmentation, churn risk, lifetime value (LTV), demographics
  - **Inventory Agent** – Stock levels, reorder risk, inventory optimization
  
- **Coordinator Agent** – Orchestrates multi-agent workflows and synthesizes cross-domain insights
- **Conversation Memory** – SQLite-backed persistence for multi-turn conversations
- **Robust Error Handling** – Automatic retry logic with exponential backoff for transient failures
- **LangChain ReAct Pattern** – Agents reason and act, with proper tool invocation tracking

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│              Coordinator Agent (ReAct)                       │
│          with SQLite Conversation Memory                     │
│         (Azure OpenAI GPT-5, max_retries=3)                 │
└──────────────────┬──────────────────────────────────────────┘
                   │
     ┌─────────────┼─────────────┬──────────────┐
     │             │             │              │
┌────▼────┐  ┌────▼────┐  ┌────▼────┐  ┌────▼────┐
│  Sales  │  │ Customer│  │Inventory│  │ ReAct   │
│  Agent  │  │  Agent  │  │  Agent  │  │ Engine  │
└────┬────┘  └────┬────┘  └────┬────┘  └─────────┘
     │            │            │
┌────▼────┐  ┌────▼────┐  ┌────▼────┐
│ Databr- │  │ Databr- │  │ Databr- │
│ icks    │  │ icks    │  │ icks    │
│ Genie   │  │ Genie   │  │ Genie   │
│ (Sales) │  │(Customer│  │ (Inv.)  │
└─────────┘  └─────────┘  └─────────┘
```

**Data Flow:**
1. User asks a question via CLI
2. Coordinator evaluates the query and routes to appropriate agents
3. Agents invoke Databricks Genie via REST API
4. Coordinator synthesizes multi-agent responses
5. Conversation state persisted to SQLite

## Prerequisites

- **Python 3.10+** (tested on 3.10.6)
- **Databricks Free/Pro Edition** with three Genie workspaces configured:
  - Sales Analytics (Genie Space)
  - Customer Insights (Genie Space)
  - Inventory Management (Genie Space)
- **Azure OpenAI Account** with a deployed LLM (GPT-5 recommended)
- **Personal Access Token (PAT)** from Databricks with "Can View" access to all Genie spaces

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Sarah121112/CaseStudyAgent.git
cd genie-multi-agent
```

### 2. Create a Python Virtual Environment
```bash
# On Windows:
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy and edit the `.env` file with your credentials:

```bash
cp .env.example .env
```

Edit `.env` with:
```env
# Databricks Configuration
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=dapi1234567890abcdef  # Must have "Can View" access to Genie spaces

# Genie Space IDs (from Databricks UI or API)
SALES_SPACE_ID=01f0fc1ec5061fb7a86dc65b6cba282f
CUSTOMER_SPACE_ID=01f0fc1f1e8e169b90f27502dafe332c
INVENTORY_SPACE_ID=01f0fc1f2a1c2d3e4f5a6b7c8d9e0f1a2

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_DEPLOYMENT=gpt-5  # Your deployment name
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_API_VERSION=2025-01-01-preview
```

**Troubleshooting:** If you get a "Can View" permission error:
1. Log into your Databricks workspace
2. Navigate to each Genie space (Sales, Customer, Inventory)
3. In the space settings, add your PAT user/token with "Can View" permissions
4. Restart the agent

## Usage

### Run the Interactive Agent

```bash
python main.py
```

### Example Queries

**Sales Questions:**
```
Questions: What is the total revenue?
Agent: Total revenue is $3,275 (North: $2,525, South: $750)

Questions: Which product is the top seller?
Agent: Top product: Laptop ($2,400)
```

**Customer Questions:**
```
Questions: What are customer segments?
Agent: Premium (2 customers, Low churn), Standard (1 customer, High churn)

Questions: Which regions have high churn?
Agent: South has High churn (C002 customer), North has Low churn (C001, C003 customers)
```

**Inventory Questions:**
```
Questions: What needs reordering?
Agent: Chair needs reordering (6 units, reorder level 10)
```

**Multi-Agent Analysis:**
```
Questions: What regions have high revenue but high churn?
Agent: North has high revenue ($2,525) with Low churn. South has lower revenue ($750) but High churn.

Questions: Which product categories appeal to Premium customers?
Agent: Premium customers in North prefer Electronics (Laptop $2,400 + Mouse $125 = $2,525) over Furniture ($750).
```

Type `exit` or `quit` to stop.

---

## Project Structure

```
genie-multi-agent/
├── main.py                      # CLI entry point - interactive agent loop
├── config.py                    # Environment config + validation
├── genie_client.py              # Databricks Genie API client with retry logic
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── README.md                    # This file
├── LICENSE                      # MIT License
│
├── agents/
│   ├── __init__.py             # Package exports
│   ├── coordinator.py          # Coordinator agent (ReAct orchestrator)
│   ├── sales_agent.py          # Sales agent (queries Sales Genie)
│   ├── customer_agent.py       # Customer agent (queries Customer Genie)
│   └── inventory_agent.py      # Inventory agent (queries Inventory Genie)
│
├── utils/
│   ├── __init__.py
│   └── retry.py                # Retry logic with exponential backoff
│
└── checkpoints.sqlite          # SQLite DB for conversation memory
```

### Key Files

| File | Purpose |
|------|---------|
| `main.py` | Interactive CLI; routes user input to coordinator agent |
| `agents/coordinator.py` | Coordinator agent using LangChain ReAct; orchestrates Sales/Customer/Inventory agents |
| `agents/sales_agent.py` | Sales domain agent; queries Sales Genie for revenue, products, regions |
| `agents/customer_agent.py` | Customer domain agent; queries Customer Genie for segments, churn, LTV |
| `agents/inventory_agent.py` | Inventory domain agent; queries Inventory Genie for stock, reorder risk |
| `genie_client.py` | Databricks REST client; handles Genie API calls + retry/backoff |
| `config.py` | Loads `.env` variables; validates required config |
| `utils/retry.py` | Generic retry mechanism with exponential backoff |

## Configuration Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABRICKS_HOST` | Databricks workspace URL | `https://dbc-01b83ad9-d4d6.cloud.databricks.com` |
| `DATABRICKS_TOKEN` | Personal access token (PAT) | `dapi1234567890abcdef` |
| `SALES_SPACE_ID` | Sales Analytics Genie space ID | `01f0fc1ec5061fb7a86dc65b6cba282f` |
| `CUSTOMER_SPACE_ID` | Customer Insights Genie space ID | `01f0fc1f1e8e169b90f27502dafe332c` |
| `INVENTORY_SPACE_ID` | Inventory Management Genie space ID | `01f0fc1f2a1c2d3e4f5a6b7c8d9e0f1a2` |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | (from Azure portal) |
| `AZURE_OPENAI_DEPLOYMENT` | LLM deployment name | `gpt-5` |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint | `https://your-resource.openai.azure.com/` |
| `AZURE_API_VERSION` | Azure OpenAI API version | `2025-01-01-preview` |

### How to Find Genie Space IDs

1. Log into your Databricks workspace
2. Navigate to **Genie** in the left sidebar
3. Open each Genie space (Sales Analytics, Customer Insights, Inventory Management)
4. Copy the space ID from the URL:
   ```
   https://your-workspace.cloud.databricks.com/genie/spaces/01f0fc1ec5061fb7a86dc65b6cba282f
                                                                 ^^ this is the space ID
   ```

## Security Considerations

- **Never commit `.env` file** – It contains sensitive credentials
- **PAT Permissions**: Grant only "Can View" access to necessary Genie spaces
- **API Keys**: Rotate Azure OpenAI and Databricks tokens regularly
- **SQLite Checkpoints**: Contains conversation history; keep `checkpoints.sqlite` secure

---

## Implementation Details

### LangChain ReAct Pattern

The Coordinator uses ReAct (Reasoning + Acting):

1. **Reason**: LLM evaluates the question and decides which agent(s) to call
2. **Act**: LLM invokes tools (sales_agent, customer_agent, inventory_agent)
3. **Observe**: LLM receives tool output
4. **Repeat**: If more information needed, iterate until answer is complete

Benefits:
- Agents reason transparently (visible thought process)
- Efficient routing (only calls necessary agents)
- Handles complex queries naturally

### Databricks Genie Integration

**Why Genie?**
- Natural language SQL generation over enterprise data
- Works with existing Databricks tables/dashboards
- Secure (leverages Databricks IAM)
- Fast (optimized queries)

**API Used:**
```python
WorkspaceClient(host, token).dashboards.start_conversation_and_wait(
    content="What is total revenue?",
    space_id="<space_id>"
)
```

---

## Troubleshooting

### Error: "You need 'Can View' permission"

**Solution:**
1. Go to Databricks workspace → Genie → (space name) → Settings
2. Add your PAT user with "Can View" permission
3. Restart the agent

### Error: "DATABRICKS_TOKEN not configured"

**Solution:**
- Check `.env` file exists and has `DATABRICKS_TOKEN` set
- Run: `python -c "from config import validate_config; validate_config()"`

### Error: "Connection error" to Azure OpenAI

**Solution:**
- Verify `AZURE_OPENAI_ENDPOINT` is reachable: `ping banaj-openai-swedencentral.cognitiveservices.azure.com`
- Check DNS: `nslookup banaj-openai-swedencentral.cognitiveservices.azure.com`
- Flush DNS cache: `ipconfig /flushdns` (Windows)

### Slow Response Times

**Cause:** Network latency or Genie query complexity  
**Solution:**
- Check Databricks workspace health
- Verify Genie space query performance in Databricks UI
- Consider adding query timeouts

---

## References

- [Databricks Genie API Docs](https://docs.databricks.com/en/genie/index.html)
- [LangChain ReAct Agent](https://python.langchain.com/docs/modules/agents/agent_types/react)
- [LangGraph Checkpointer](https://langchain-ai.github.io/langgraph/reference/checkpointers/)
- [Azure OpenAI API](https://learn.microsoft.com/en-us/azure/ai-services/openai/)

---

## License

MIT License - see [LICENSE](LICENSE) for details.

Author: Sarah (University of Sharjah)  
Date: January 2026
