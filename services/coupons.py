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

def add_coupon(session: Session, code: str, type: int, fixed_amount: float, percentage_amount: float, minimum_order: float,
                maximum_discount: float, quantity: int, limit_per_user: int, is_active: bool):
    old_coupon = session.query(Coupon).filter_by(code=code).first()
    if (old_coupon):
        return (False, 'coupon already exists')
    
    new_coupon = Coupon(code=code, type=type, fixed_amount=fixed_amount, percentage_amount=percentage_amount, minimum_order=minimum_order,
                        maximum_discount=maximum_discount, quantity=quantity, limit_per_user=limit_per_user, is_active=is_active)
    session.add(new_coupon)
    session.commit()
    return (True, "Created coupon {}".format(code))

def update_coupon(session: Session, coupon_id: int, code: str, type: int, fixed_amount: float, percentage_amount: float, 
                  minimum_order: float, maximum_discount: float, quantity: int, limit_per_user:int, is_active: bool):
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

    if (fixed_amount):
        coupon.fixed_amount = fixed_amount

    if (percentage_amount):
        coupon.percentage_amount = percentage_amount

    if (minimum_order):
        coupon.minimum_order = minimum_order

    if (maximum_discount):
        coupon.maximum_discount = maximum_discount

    if (quantity):
        coupon.quantity = quantity

    if (limit_per_user):
        coupon.limit_per_user = limit_per_user

def delete_coupon(session: Session, coupon_id: int):
    coupon = session.query(coupon).filter_by(id=coupon_id).first()
    if not coupon:
        return (False, 'Coupon does not exist')
    session.delete(coupon)
    session.commit()
    return (True, "Deleted coupon {}".format(coupon_id))
