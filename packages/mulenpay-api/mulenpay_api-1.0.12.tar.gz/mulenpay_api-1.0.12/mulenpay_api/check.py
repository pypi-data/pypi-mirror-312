from mulenpay_api.abstract import MulenpayClient


class Check:

    def __init__(self, api_key: str):
        self.client = MulenpayClient(api_key=api_key)

    async def get_check_by_id(self, check_id):
        return await self.client.get_request(f'/payments/{check_id}/receipt')
