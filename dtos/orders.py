import datetime
from models import *

from pydantic import BaseModel

class OrderInput(BaseModel):
    cart: dict
    coupon_code: str

class OrderOutput:
    id: int
    user_id: int  
    status: str
    applied_coupon: bool
    raw_total_cost: float
    final_total_cost: float 
    created_at: datetime
    updated_at: datetime

    def __init__(self, order: Order) -> None:
        self.id = order.id
        self.user_id = order.user_id
        self.status = order.status
        self.applied_coupond = order.applied_coupon
        self.raw_total_cost = order.raw_total_cost
        self.final_total_cost = order.final_total_cost
        self.created_at = order.created_at
        self.updated_at = order.updated_at