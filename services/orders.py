from models import *
from sqlalchemy.orm import Session
from services.products import get_product_by_id
from services.coupons import get_coupon_by_code

def new_order(session: Session, current_user: User, coupon_code: str, cart: dict):
    cost_total = 0
    product_ids = cart.keys()
    for product_id in product_ids:
        success, product = get_product_by_id(session, product_id)
        if not success:
            return (False, f"Cannot find product {product_id}")
        cost_total += cart[product_id] * product.cost_per_unit

    if coupon_code != "":
        success, coupon = get_coupon_by_code
        if not success:
            return (False, f"Invalid Coupon")
        else: 
            pass #TODO


    