from pydantic import BaseModel
from models import Coupon

class CouponInput(BaseModel):
    code: str
    type: str
    value: float
    min_order_required: float
    max_discount_applicable: float
    stock_quantity: int
    limit_per_user: int
    is_active: bool

class CouponOutput:
    id: int
    code: str
    type: str
    value: float
    min_order_required: float
    max_discount_applicable: float
    stock_quantity: int
    limit_per_user: int
    is_active: bool

    def __init__(self, coupon: Coupon):
        self.id = coupon.id
        self.code = coupon.code
        self.type = coupon.type
        self.value = coupon.value
        self.min_order_required = coupon.min_order_required
        self.max_discount_applicable = coupon.max_discount_applicable
        self.stock_quantity = coupon.stock_quantity
        self.limit_per_user = coupon.limit_per_user
        self.is_active = coupon.is_active