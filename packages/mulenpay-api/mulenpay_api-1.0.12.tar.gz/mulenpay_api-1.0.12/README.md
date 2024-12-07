# MulenPay API Client

## Описание

Асинхронный Python-клиент для работы с API MulenPay. Подходит для управления платежами и подписками.

## Установка

```bash
pip install pydantic==2.9.2
pip install httpx==0.27.2
pip install mulenpay-api
```

Использование
Настройка клиента
Для начала работы создайте экземпляр Payment или Subscribe, указав ваш api_key и secret_key.

```python
from mulenpay_api import Payment
from mulenpay_api.subscribe import Subscribe

api_key = 'ВАШ_API_KEY'
secret_key = 'ВАШ_SECRET_KEY'

payment = Payment(api_key=api_key, secret_key=secret_key)
subscribe = Subscribe(api_key=api_key)
```
# **Работа с платежами**

Создание платежа
```python
import asyncio

async def create_payment():
    response = await payment.create_payment(payment.CreatePayment(
        currency="rub",
        amount="1000.50",
        uuid="invoice_123",
        shopId=5,
        description="Покупка булочек",
        subscribe=None,
        holdTime=None
    ))
    print(response)

if __name__ == '__main__':
    asyncio.run(create_payment())
```
Получение списка платежей
```python
async def get_list():
    response = await payment.get_payment_list()
    print(response)

if __name__ == '__main__':
    asyncio.run(get_list())
```
Получение платежа по ID
```python
async def get_by_id():
    response = await payment.get_payment_by_id(5)
    print(response)

if __name__ == '__main__':
    asyncio.run(get_by_id())
```
Подтверждение платежа
```python
async def confirm_payment():
    response = await payment.confirm_payment(5)
    print(response)

if __name__ == '__main__':
    asyncio.run(confirm_payment())
```
Отмена платежа
```python
async def cancel_payment():
    response = await payment.cancel_payment(5)
    print(response)

if __name__ == '__main__':
    asyncio.run(cancel_payment())
```
Возврат платежа
```python
async def refund_payment():
    response = await payment.refund_payment(5)
    print(response)

if __name__ == '__main__':
    asyncio.run(refund_payment())
```
# **Работа с подписками**
Получение списка подписок
```python
async def get_subscription_list():
    response = await subscribe.get_subscription_list()
    print(response)

if __name__ == '__main__':
    asyncio.run(get_subscription_list())
```
Удаление подписки по ID
```python
async def delete_subscription():
    response = await subscribe.delete_subscription_by_id(5)
    print(response)

if __name__ == '__main__':
    asyncio.run(delete_subscription())
```
# Требования
-Python 3.7+

-Установленная библиотека mulenpay-api
