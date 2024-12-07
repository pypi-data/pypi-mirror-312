from mulenpay_api.abstract import MulenpayClient


class Subscribe:

    def __init__(self, api_key: str):
        self.client = MulenpayClient(api_key=api_key)

    async def get_subscription_list(self):
        return await self.client.get_request('/subscribes')

    async def delete_subscription_by_id(self, subscrib_id):
        return await self.client.delete_request(f'/subscribes/{subscrib_id}')
