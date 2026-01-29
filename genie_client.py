from databricks.sdk import WorkspaceClient
from config import DATABRICKS_HOST, DATABRICKS_TOKEN
import time
import logging

# Cache the WorkspaceClient as a singleton for better performance
_client: WorkspaceClient | None = None


def get_client() -> WorkspaceClient:
    """Get or create a cached WorkspaceClient instance.
    
    Returns:
        Configured WorkspaceClient for Databricks API calls
        
    Raises:
        ValueError: If Databricks credentials are not configured
    """
    global _client
    if _client is None:
        if not DATABRICKS_HOST or not DATABRICKS_TOKEN:
            raise ValueError("Databricks credentials not configured in .env file")
        _client = WorkspaceClient(host=DATABRICKS_HOST, token=DATABRICKS_TOKEN)
    return _client


def ask_genie(space_id: str, question: str) -> str:
    """Query the Databricks Genie API with a question.
    
    Args:
        space_id: The Genie space ID to query
        question: The question to ask
        
    Returns:
        The response from Genie, or "No response" if no answer found
        
    Raises:
        ValueError: If Databricks credentials are not configured
        RuntimeError: If the Genie API call fails
    """
    # Implement a small retry loop for transient connection errors
    max_retries = 3
    backoff = 1.0
    last_exc = None

    for attempt in range(1, max_retries + 1):
        try:
            client = get_client()
            message = client.genie.start_conversation_and_wait(
                space_id=space_id,
                content=question,
            )

            if message.attachments:
                for a in message.attachments:
                    if a.text and a.text.content:
                        return a.text.content

            return "No response from Genie. Try rephrasing your question."
        except ValueError:
            # Re-raise credential errors as-is
            raise
        except Exception as e:
            last_exc = e
            logging.warning(
                "ask_genie attempt %d/%d failed: %s",
                attempt,
                max_retries,
                str(e),
            )
            # If last attempt, break and raise below
            if attempt == max_retries:
                break
            time.sleep(backoff)
            backoff *= 2

    # After retries, raise a clear runtime error with original exception chained
    raise RuntimeError("Genie API connection error after retries") from last_exc

