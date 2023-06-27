from pydantic import BaseModel

class OrderInput(BaseModel):
    cart: dict
    coupon_code: str
