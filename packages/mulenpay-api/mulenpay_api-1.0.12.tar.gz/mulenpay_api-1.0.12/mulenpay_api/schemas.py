from typing import Optional, List
from pydantic import BaseModel


class Item(BaseModel):
    description: str
    quantity: float
    price: float
    vat_code: int
    payment_subject: int
    payment_mode: int
    product_code: str | None
    country_of_origin_code: str | None
    customs_declaration_number: str | None
    excise: str | None
    measurement_unit: int | None


class CreatePayment(BaseModel):
    currency: str = "rub"
    amount: float
    uuid: str
    shopId: int
    description: str
    subscribe: Optional[str] = None
    holdTime: Optional[str] = None
    items: List[Item]

