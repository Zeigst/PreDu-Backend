from models import *
from sqlalchemy.orm import Session

def add_used_coupon(session: Session, user: User, coupon: Coupon, order: Order, applied_value: float):
    used_coupon = UsedCoupon(
        user_id=user.id, 
        order_id=order.id, 
        coupon_id=coupon.id,

        code=coupon.code,
        type = coupon.type,
        value = coupon.value,
        applied_value = applied_value,
        min_order_required = coupon.min_order_required,
        max_discount_applicable = coupon.max_discount_applicable,
        limit_per_user = coupon.limit_per_user
    )

    session.add(used_coupon)

    oldcoupon = session.query(Coupon).filter_by(id=coupon.id).first()
    oldcoupon.stock_quantity -= 1
    session.flush()
    session.commit()
    return (True, f"Add Used Coupon {used_coupon.id}")

def get_used_coupon_by_order_id(session: Session, order_id: int):
    used_coupon = session.query(UsedCoupon).filter_by(order_id=order_id).first()
    return (True, used_coupon)

def get_user_used_coupons(session: Session, user: User):
    used_coupons = session.query(UsedCoupon).filter_by(user_id=user.id).order_by(UsedCoupon.created_at.desc()).all()
    return (True, used_coupons)

def cancle_used_coupon(session: Session, used_coupon: UsedCoupon):
    coupon = session.query(Coupon).filter_by(id=used_coupon.coupon_id).first()
    if coupon:
        coupon.stock_quantity += 1

    session.commit()
    return (True, "Cancled Used Coupon")