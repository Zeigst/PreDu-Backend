from pydantic import BaseModel
from models import Coupon

class CouponInput(BaseModel):
    code: str
    order_value: float

class CouponOutput:
    id: int
    code: str
    type: int
    fixed_amount: float
    percentage_amount: float
    minimum_order: float
    maximum_discount: float
    quantity: int
    limit_per_user: int
    is_active: bool

    def __init__(self, coupon: Coupon):
        self.id = coupon.id
        self.code = coupon.code
        self.type = coupon.type
        self.fixed_amount = coupon.fixed_amount
        self.percentage_amount = coupon.percentage_amount
        self.minimum_order = coupon.minimum_order
        self.maximum_discount = coupon.maximum_discount
        self.limit_per_user = coupon.limit_per_user
        self.is_active = coupon.is_active