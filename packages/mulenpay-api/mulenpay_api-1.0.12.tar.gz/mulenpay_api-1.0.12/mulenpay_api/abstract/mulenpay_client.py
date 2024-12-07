import httpx


class MulenpayClient:
    def __init__(
        self,
        api_key=None,
        *,
        client: httpx.AsyncClient = None,
        base_url='https://mulenpay.ru/api/v2'
    ):
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {api_key}"
        }
        if not client:
            client = httpx.AsyncClient()
        
        client.base_url = base_url
        client.headers = self.headers

        self.client = client

    async def close(self):
        await self.client.aclose()

    async def get_request(self, path):
        response = await self.client.get(path)
        return response.json()

    async def put_request(self, path):
        response = await self.client.put(path)
        return response.json()

    async def delete_request(self, path):
        response = await self.client.delete(path)
        return response.json()
