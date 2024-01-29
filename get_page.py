from zenrows import ZenRowsClient
from .config import get_client
from .exceptions import InitializationError, OutOfQuotaException
from loguru import logger


async def get_page_with_json_render(url: str, api_key: str | None = None, retries: int = 2) -> str:
    logger.info("Getting page with json render...")
    if api_key is None:
        client = get_client()
        if client is None:
            raise InitializationError("No API key for the request")
    else:
        client = ZenRowsClient(api_key)
    logger.success("ZenRows client was selected")
    logger.info("Awaiting response from ZenRows...")

    while ((response := await client.get_async(url, params={"js_render": "true", "block_resources": "image,media,font"}))
           or True):
        if response.status_code == 200:
            break

        if response.status_code == 402:
            logger.error("Out of ZenRows quota exception raised")
            raise OutOfQuotaException()

        logger.warning(f"ZenRows returned invalid status code {response.status_code}. Response is {response.text}")

        if retries <= 0:
            break

        retries -= 1
        logger.info("Retrying...")

    logger.success(f"Response from ZenRows received (status code {response.status_code}). Returning...")
    return response.text
