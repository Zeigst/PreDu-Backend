from models import *
from sqlalchemy.orm import Session
from services.products import get_product_by_id, check_stock
from services.coupons import get_coupon_by_code, validate_coupon, get_discount_value
from services.ordered_products import add_ordered_product
from services.used_coupons import add_used_coupon


def validate_cart(session: Session, cart: dict):
    empty_cart = all(value == 0 for value in cart.values())
    if empty_cart:
        return (False, "Cart Empty")
    
    product_ids = cart.keys()
    for product_id in product_ids:
        product_in_stock, message = check_stock(session, product_id, cart[product_id])
        if not product_in_stock:
            return (False, message)
    
    return (True, "Cart Valid")


def get_cart_total_cost(session: Session, cart: dict):
    total_cost = 0
    product_ids = cart.keys()
    for product_id in product_ids:
        product = session.query(Product).filter_by(id=product_id).first()
        total_cost += cart[product_id] * product.cost_per_unit

    return total_cost


def add_order(session: Session, current_user: User, coupon_code: str, cart: dict):
    valid_cart, message = validate_cart(session, cart)
    if not valid_cart:
        return (False, message)
    
    total_cost = get_cart_total_cost(session, cart)
    
    valid_coupon, message = validate_coupon(session, coupon_code, current_user, total_cost)
    if not valid_coupon:
        return (False, message)
    
    discount_value = get_discount_value(session, coupon_code, total_cost)

    final_cost = total_cost - discount_value

    order = Order(status="processing", user_id=current_user.id, raw_total_cost=total_cost,
                      discounted_amount=discount_value, final_total_cost=final_cost)

    if message == "Valid Coupon":
        coupon = session.query(Coupon).filter_by(code=coupon_code).first()
        order.coupon_id = coupon.id
        
    session.add(order)
    session.flush()

    product_ids = cart.keys()
    for product_id in product_ids:
        if cart[product_id] > 0:
            success, data = add_ordered_product(session, order.id, product_id, cart[product_id])
    
    if message == "Valid Coupon":
        success, data = add_used_coupon(session, current_user.id, order.coupon_id, order.id)

    session.commit()
    return (True, f"Add Order {order.id}")