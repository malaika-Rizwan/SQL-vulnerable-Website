import time
from collections import defaultdict

# In-memory rate limiter for class / localhost use only.

_attempts: dict[str, list[float]] = defaultdict(list)


def check_rate_limit(key: str, max_attempts: int = 10, window_seconds: int = 60) -> bool:
    now = time.time()
    bucket = _attempts[key]
    _attempts[key] = [t for t in bucket if now - t < window_seconds]
    if len(_attempts[key]) >= max_attempts:
        return False
    _attempts[key].append(now)
    return True


def reset_rate_limit(key: str) -> None:
    _attempts.pop(key, None)
