import os
import random
import time
import datetime as dt
from typing import Any, Optional

from databricks.sdk import WorkspaceClient
from databricks.sdk.errors.platform import PermissionDenied, Unauthenticated, NotFound, BadRequest


TRANSIENT_HINTS = (
    "rate limit",
    "429",
    "timeout",
    "timed out",
    "temporarily",
    "service unavailable",
    "connection reset",
    "connection aborted",
    "connection error",
    "502",
    "503",
    "504",
    "try again",
)

NON_RETRYABLE_HINTS = (
    "can view",
    "permission",
    "forbidden",
    "unauthorized",
    "401",
    "403",
    "invalid token",
    "not authorized",
    "access denied",
)


def _is_transient_exception(e: Exception) -> bool:
    msg = str(e).lower()
    if any(h in msg for h in NON_RETRYABLE_HINTS):
        return False
    return any(h in msg for h in TRANSIENT_HINTS)


def _extract_text(message: Any) -> str:
    attachments = getattr(message, "attachments", None)
    if attachments:
        parts: list[str] = []
        for att in attachments:
            text = getattr(att, "text", None) or getattr(att, "content", None)
            if text:
                parts.append(str(text))
        if parts:
            return "\n\n".join(parts)

    for field in ("text", "answer", "content", "final_summary"):
        v = getattr(message, field, None)
        if v:
            return str(v)

    return str(message)


def ask_genie(space_id: str, question: str, retries: int = 3, timeout_seconds: int = 120) -> str:
    if not space_id:
        raise ValueError("space_id is required")
    if not question or not question.strip():
        raise ValueError("question must be a non-empty string")

    if not os.getenv("DATABRICKS_HOST") or not os.getenv("DATABRICKS_TOKEN"):
        raise ValueError('Missing Databricks auth. Set DATABRICKS_HOST and DATABRICKS_TOKEN.')

    client = WorkspaceClient()

    last_err: Optional[Exception] = None
    for attempt in range(1, retries + 1):
        try:
            msg = client.genie.start_conversation_and_wait(
                space_id=space_id,
                content=question,
                timeout=dt.timedelta(seconds=timeout_seconds),
            )
            return _extract_text(msg)

        except (PermissionDenied, Unauthenticated, NotFound, BadRequest):
            raise

        except Exception as e:
            last_err = e
            if not _is_transient_exception(e):
                raise

            if attempt < retries:
                delay = min(8.0, 1.0 * (2 ** (attempt - 1)))
                delay += random.uniform(0, 0.25 * delay)
                time.sleep(delay)
            else:
                raise

    raise last_err if last_err else RuntimeError("Unknown ask_genie failure")
