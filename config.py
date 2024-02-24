import asyncio

from zenrows import ZenRowsClient
from loguru import logger


client: ZenRowsClient | None = None
requests_semaphore: asyncio.Semaphore | None = None


def set_api_key(key: str) -> None:
    global client

    client = ZenRowsClient(key)
    logger.success("API key for ZenRows was set up")


def get_client() -> ZenRowsClient | None:
    return client


def set_requests_concurrency_limit(limit: int):
    global requests_semaphore

    requests_semaphore = asyncio.Semaphore(limit)
