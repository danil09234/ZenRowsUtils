from zenrows import ZenRowsClient
from .config import client


async def get_page_with_json_render(url: str, api_key: str | None = None) -> str:
    if api_key is None:
        if client is None:
            raise RuntimeError("No API key for the request")
        response = await client.get_async(url, params={"js_render": "true"})
    else:
        local_client = ZenRowsClient(api_key)
        response = await local_client.get_async(url, params={"js_render": "true"})
    return response.text
