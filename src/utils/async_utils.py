import asyncio
from functools import wraps

def async_retry(max_retries, delay=1, backoff=2):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        raise
                    await asyncio.sleep(delay * (backoff ** (retries - 1)))
        return wrapper
    return decorator

async def gather_with_concurrency(concurrency, *tasks):
    semaphore = asyncio.Semaphore(concurrency)
    async def sem_task(task):
        async with semaphore:
            return await task
    return await asyncio.gather(*(sem_task(task) for task in tasks))

async def periodic(interval, func, *args, **kwargs):
    while True:
        await func(*args, **kwargs)
        await asyncio.sleep(interval)
