import time
from collections import defaultdict
from typing import Dict, List

from app.core.config import Config
from app.utils.responses import api_response

request_log: Dict[str, List[float]] = defaultdict(list)


def rate_limit():
    def decorator(f):
        def wrapper(*args, **kwargs):
            remote_addr = "global"
            now = time.time()
            window = Config.RATE_LIMIT_WINDOW_SECONDS
            timestamps = request_log[remote_addr]
            timestamps[:] = [t for t in timestamps if t > now - window]
            if len(timestamps) >= Config.RATE_LIMIT_MAX_REQUESTS:
                return api_response(error="Rate limit exceeded", status=429)
            timestamps.append(now)
            return f(*args, **kwargs)
        return wrapper
    return decorator
