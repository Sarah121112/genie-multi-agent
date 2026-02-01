import random
import time
from typing import Any, Callable, Optional, Tuple

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


def is_transient_error(e: Exception) -> bool:
    msg = str(e).lower()
    if any(hint in msg for hint in NON_RETRYABLE_HINTS):
        return False
    return any(hint in msg for hint in TRANSIENT_HINTS)


def retry_call(
    fn: Callable[[], Any],
    retries: int = 2,
    base_delay: float = 1.0,
    max_delay: float = 6.0,
) -> Tuple[bool, Any, Optional[Exception], int]:
    last_err: Optional[Exception] = None

    for attempt in range(retries + 1):
        try:
            return True, fn(), None, attempt + 1
        except Exception as e:
            last_err = e
            if attempt >= retries or not is_transient_error(e):
                break

            delay = min(max_delay, base_delay * (2 ** attempt))
            delay = delay + random.uniform(0, 0.25 * delay)
            time.sleep(delay)

    return False, None, last_err, retries + 1
