from zenrows import ZenRowsClient


client: ZenRowsClient | None = None


def set_api_key(key: str):
    global client

    client = ZenRowsClient(key)
