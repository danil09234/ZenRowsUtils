from zenrows import ZenRowsClient
from .config import get_client
from .exceptions import InitializationError
from loguru import logger


async def get_page_with_json_render(url: str, api_key: str | None = None) -> str:
    logger.info("Getting page with json render...")
    if api_key is None:
        client = get_client()
        if client is None:
            raise InitializationError("No API key for the request")
    else:
        client = ZenRowsClient(api_key)
    logger.success("ZenRows client was selected")
    logger.info("Awaiting response from ZenRows...")
    response = await client.get_async(url, params={"js_render": "true", "block_resources": "image,media,font"})
    logger.success("Response from ZenRows received. Returning...")
    return response.text
