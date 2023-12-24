import sys

from zenrows import ZenRowsClient
from .config import get_client
from .exceptions import InitializationError


async def get_page_with_json_render(url: str, api_key: str | None = None) -> str:
    if api_key is None:
        client = get_client()
        if client is None:
            raise InitializationError("No API key for the request")
    else:
        client = ZenRowsClient(api_key)
    response = await client.get_async(url, params={"js_render": "true", "block_resources": "image,media,font"})
    return response.text
