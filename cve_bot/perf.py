import logging
from functools import wraps
from time import monotonic

logger = logging.getLogger(__name__)


def track(limit=0.5):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):  # noqa: WPS430
            start_time = monotonic()
            retval = func(*args, **kwargs)
            total_time = monotonic() - start_time
            if total_time > limit:
                logger.warning("Function %s took %f seconds", func.__name__, total_time)
            return retval

        return inner

    return decorator
