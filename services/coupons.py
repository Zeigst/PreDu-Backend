from models import *
from sqlalchemy.orm import Session

def get_all_coupons(session: Session):
    coupons = session.query(Coupon).order_by(Coupon.id.asc()).all()
    return (True, coupons)

def get_coupon_by_code(session: Session, coupon_code: str):
    coupon = session.query(Coupon).filter_by(code=coupon_code).first()
    if (not coupon):
        return (False, "Invalid Coupon Code")
    return (True, coupon)

def get_coupon_by_id(session: Session, coupon_id: int):
    coupon = session.query(coupon).filter_by(id=coupon_id).first()
    if (not coupon):
        return (False, "Coupon does not exist")
    return (True, coupon)

def add_coupon(session: Session, code: str, type: str, value: float, min_order_required: float,
               max_discount_applicable: float, stock_quantity: int, limit_per_user: int, is_active: bool):
    if len(code)<=5:
        return (False, "Invalid Code")
    if type!="fixed" and type!="percentage":
        return (False, "Invalid Type")
    if value < 0:
        return (False, "Invalid Value")
    if type=="percentage" and value>100:
        return (False, "Invalid Value")
    if min_order_required < 0:
        return (False, "Invalid Minimum Required")
    if max_discount_applicable < 0:
        return (False, "Invalid Maximum Applicable")
    if type == "fixed" and max_discount_applicable!=value:
        return (False, "Invalid Maximum Applicable")
    if stock_quantity < 0:
        return (False, "Invalid Stock")
    if limit_per_user <= 0:
        return (False, "Invalid Limit")
    
    old_coupon = session.query(Coupon).filter_by(code=code).first()
    if (old_coupon):
        return (False, 'Coupon Code Already Exists')
    
    new_coupon = Coupon(code=code, type=type, value=value, min_order_required=min_order_required, max_discount_applicable=max_discount_applicable,
                        stock_quantity=stock_quantity, limit_per_user=limit_per_user, is_active=is_active)
    session.add(new_coupon)
    session.commit()
    return (True, "Created Coupon {}".format(code))

def update_coupon(session: Session, coupon_id: int, code: str, type: str, value: float, min_order_required: float,
                  max_discount_applicable: float, stock_quantity: int, limit_per_user: int, is_active: bool):
    coupon = session.query(Coupon).filter_by(id=coupon_id).first()
    if (not coupon):
        return (False, "Coupon does not exist")
    
    if len(code)<=5:
        return (False, "Invalid Code")
    if type!="fixed" and type!="percentage":
        return (False, "Invalid Type")
    if value < 0:
        return (False, "Invalid Value")
    if type=="percentage" and value>100:
        return (False, "Invalid Value")
    if min_order_required < 0:
        return (False, "Invalid Minimum Required")
    if max_discount_applicable < 0:
        return (False, "Invalid Maximum Applicable")
    if type == "fixed" and max_discount_applicable!=value:
        return (False, "Invalid Maximum Applicable")
    if stock_quantity < 0:
        return (False, "Invalid Stock")
    if limit_per_user <= 0:
        return (False, "Invalid Limit")
      
    old_coupon = session.query(Coupon).filter_by(code=code).first()
    if (old_coupon):
        if old_coupon.id != coupon_id:
            return (False, "Coupon Code Already Exist")
    else:
        coupon.code = code
    
    coupon.type = type
    coupon.value = value
    coupon.min_order_required = min_order_required
    coupon.max_discount_applicable = max_discount_applicable
    coupon.stock_quantity = stock_quantity
    coupon.limit_per_user = limit_per_user
    coupon.is_active = is_active
    session.commit()

    return (True, f"Updated Coupon {coupon_id}")

def delete_coupon(session: Session, coupon_id: int):
    coupon = session.query(Coupon).filter_by(id=coupon_id).first()
    if not coupon:
        return (False, 'Coupon does not exist')
    session.delete(coupon)
    session.commit()
    return (True, "Deleted Coupon {}".format(coupon_id))

def validate_coupon(session: Session, coupon_code: str, current_user: User, total_cost: float):
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
    
    user = session.query(User).filter_by(id=current_user.id).first()
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


    
