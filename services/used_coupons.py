from models import *
from sqlalchemy.orm import Session

def add_used_coupon(session: Session, user_id: int, coupon_id: int, order_id: int):
    used_coupon = UsedCoupon(user_id=user_id, coupon_id=coupon_id, order_id=order_id)
    session.add(used_coupon)
    session.flush()
    session.commit()
    return (True, f"Add Used Coupon {used_coupon.id}")