import datetime
from models import *

class OrderOutput:
    id: int
    status: str
    user_id: int
    coupon_id: int
    raw_total_cost: float
    discounted_amount: float
    final_total_cost: float
    created_at: datetime
    updated_at: datetime

    def __init__(self, order: Order) -> None:
        self.id = order.id
        self.status = order.status
        self.user_id = order.user_id
        self.coupon_id = order.coupon_id
        self.raw_total_cost = order.raw_total_cost
        self.discounted_amount = order.discounted_amount
        self.final_total_cost = order.final_total_cost
        self.created_at = order.created_at
        self.updated_at = order.updated_at