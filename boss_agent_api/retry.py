import asyncio
from functools import wraps
import logging

def async_retry(max_retries=3, delay=1, backoff=2, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries == max_retries:
                        logging.error(f"Function {func.__name__} failed after {max_retries} retries. Error: {str(e)}")
                        raise
                    logging.warning(f"Retry {retries}/{max_retries} for function {func.__name__} after error: {str(e)}")
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator
