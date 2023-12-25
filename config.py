from zenrows import ZenRowsClient
from loguru import logger


client: ZenRowsClient | None = None


def set_api_key(key: str):
    global client

    client = ZenRowsClient(key)
    logger.success("API key for ZenRows was set up")


def get_client() -> ZenRowsClient | None:
    return client
