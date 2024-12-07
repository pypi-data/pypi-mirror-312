from mulenpay_api.abstract import MulenpayClient
from .schemas import CreatePayment
from mulenpay_api.utils import calculate_sign


class Payment:
    CreatePayment = CreatePayment

    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.client = MulenpayClient(api_key=api_key)

    async def _post_request(self, path, data):
        data = data.model_dump()
        data['sign'] = self._calculate_sign(data)
        response = await self.client.client.post(path, json=data)
        return response.json()

    def _calculate_sign(self, data: dict):
        data_to_sign = {key: data[key] for key in ["currency", "amount", "shopId"] if key in data}
        return calculate_sign(self.secret_key, data_to_sign)

    async def create_payment(self, data: CreatePayment):
        return await self._post_request('/payments', data)

    async def get_payment_list(self, page=1):
        return await self.client.get_request(f'/payments/page={page}')

    async def get_payment_by_id(self, payment_id):
        return await self.client.get_request(f'/payments/{payment_id}')

    async def confirm_payment(self, payment_id):
        return await self.client.put_request(f'/payments/{payment_id}/hold')

    async def cancel_payment(self, payment_id):
        return await self.client.delete_request(f'/payments/{payment_id}/hold')

    async def refund_payment(self, payment_id):
        return await self.client.put_request(f'/payments/{payment_id}/refund')

