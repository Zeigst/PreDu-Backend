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

def validate_coupon(session: Session, coupon_code: str, user: User, total_cost: float):
    if coupon_code == "":
        return (True, "No Coupon")
    coupon = session.query(Coupon).filter_by(code=coupon_code).first()
    if (not coupon):
        return (False, "ERROR: Invalid Coupon Code")
    if not coupon.is_active:
        return (False, "ERROR: Coupon No Longer Active")
    if total_cost < coupon.min_order_required:
        return (False, "ERROR: Minimum Spend Does Not Reach.")
    if coupon.stock_quantity <= 0:
        return (False, "ERROR: Coupon Out Of Stock.")
    
    user = session.query(User).filter_by(id=user.id).first()
    used_coupons = session.query(UsedCoupon).filter_by(coupon_id=coupon.id, user_id=user.id).all()
    if len(used_coupons) >= coupon.limit_per_user:
        return (False, "ERROR: Coupon Use Reached Limit")
    
    return (True, "Valid Coupon")

def get_discount_value(session: Session, coupon_code: str, total_cost: float):
    if coupon_code == "":
        return 0
    coupon = session.query(Coupon).filter_by(code=coupon_code).first()
    if coupon.type == "fixed":
        discount_value = coupon.value
    elif coupon.type == "percentage":
        discount_value = total_cost / 100 * coupon.value
    
    if discount_value >= coupon.max_discount_applicable:
        discount_value = coupon.max_discount_applicable
    
    if discount_value >= total_cost:
        discount_value = total_cost

    return discount_value

    
