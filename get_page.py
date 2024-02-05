from requests import Response
from zenrows import ZenRowsClient
from .config import get_client
from .exceptions import InitializationError, OutOfQuotaException
from loguru import logger


def get_client_helper(api_key: str | None) -> ZenRowsClient:
    if api_key is None:
        client = get_client()
        if client is None:
            raise InitializationError("No API key for the request")
    else:
        client = ZenRowsClient(api_key)
    return client


async def retries_helper(client: ZenRowsClient, retries: int, url: str, *args, **kwargs) -> Response:
    while (response := await client.get_async(url, *args, **kwargs)) or True:
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
    return response


async def get_page_with_json_render(url: str, api_key: str | None = None, retries: int = 2) -> str:
    logger.info("Getting page with json render...")
    client = get_client_helper(api_key)
    logger.success("ZenRows client was selected")
    logger.info("Awaiting response from ZenRows...")

    response = await retries_helper(
        client, retries, url,
        params={"js_render": "true", "block_resources": "image,media,font"}
    )

    logger.success(f"Response from ZenRows received (status code {response.status_code}). Returning...")
    return response.text


async def get_page_with_custom_headers(url: str, headers: dict, api_key: str | None = None, retries: int = 2) -> str:
    logger.info("Getting page with custom headers render...")
    client = get_client_helper(api_key)
    logger.success("ZenRows client was selected")
    logger.info("Awaiting response from ZenRows...")

    response = await retries_helper(client, retries, url, headers=headers)

    logger.success(f"Response from ZenRows received (status code {response.status_code}). Returning...")
    return response.text
