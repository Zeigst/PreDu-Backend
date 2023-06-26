from models import *
from sqlalchemy.orm import Session

def get_all_coupons(session: Session):
    coupons = session.query(Coupon).all()
    return (True, coupons)

def get_coupon_by_code(session: Session, coupon_code: str):
    coupon = session.query(Coupon).filter_by(code=coupon_code).first()
    if (not coupon):
        return (False, "Invalid Coupon Code")
    return (True, coupon)

def get_coupon(session: Session, coupon_id: int):
    coupon = session.query(coupon).filter_by(id=coupon_id).first()
    if (not coupon):
        return (False, "Coupon does not exist")
    return (True, coupon)

def add_coupon(session: Session, code: str, type: str, value: float, min_order_required: float,
               max_discount_applicable: float, stock_quantity: int, limit_per_user: int):
    old_coupon = session.query(Coupon).filter_by(code=code).first()
    if (old_coupon):
        return (False, 'Coupon already exists')
    
    new_coupon = Coupon(code=code, type=type, value=value, min_order_required=min_order_required, max_discount_applicable=max_discount_applicable,
                        stock_quantity=stock_quantity, limit_per_user=limit_per_user, is_active=False)
    session.add(new_coupon)
    session.commit()
    return (True, "Created Coupon {}".format(code))

def update_coupon(session: Session, coupon_id: int, code: str, type: str, value: float, min_order_required: float,
                  max_discount_applicable: float, stock_quantity: int, limit_per_user: int):
    coupon = session.query(Coupon).filter_by(id=coupon_id).first()
    if (not coupon):
        return (False, "Coupon does not exist")
    
    if (code):
        old_coupon = session.query(Coupon).filter_by(code=code).first()
        if (old_coupon):
            return (False, "Coupon code already exist")
        else:
            coupon.code = code
    
    if (type):
        coupon.type = type

    if (value):
        coupon.value = value

    if (min_order_required):
        coupon.min_order_required = min_order_required

    if (max_discount_applicable):
        coupon.max_discount_applicable = max_discount_applicable

    if (stock_quantity):
        coupon.stock_quantity = stock_quantity

    if (limit_per_user):
        coupon.limit_per_user = limit_per_user

def delete_coupon(session: Session, coupon_id: int):
    coupon = session.query(coupon).filter_by(id=coupon_id).first()
    if not coupon:
        return (False, 'Coupon does not exist')
    session.delete(coupon)
    session.commit()
    return (True, "Deleted coupon {}".format(coupon_id))

def validate_coupon(session: Session, coupon: Coupon, user: User, total_cost: float):
    coupon = session.query(Coupon).filter_by(id=coupon.id).first()
    if not coupon.is_active:
        return (False, "This code is no longer active")
    if total_cost < coupon.min_order_required:
        return (False, "Min spend does not reach.")
    if coupon.stock_quantity <= 0:
        return (False, "Coupon out of stock.")
    
    user = session.query(User).filter_by(id=user.id).first()
    used_coupons = session.query(UsedCoupon).filter_by(coupon_id=coupon.id, user_id=user.id).all()

    
