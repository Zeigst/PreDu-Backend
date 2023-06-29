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

def get_orders(session: Session, current_user: User):
    orders = session.query(Order).filter_by(user_id=3).all()
    for order in orders:
        order_json = {}
        order_json["id"] = order.id
        order_json["status"] = order.status
        order_json["user_id"] = order.user_id
        order_json["coupon_id"] = order.coupon_id
        order_json["raw_total_cost"] = order.raw_total_cost
        order_json["discounted_amount"] = order.discounted_amount
        order_json["final_total_cost"] = order.final_total_cost
        order_json["raw_total_cost"] = order.raw_total_cost
        order_json["created_at"] = order.created_at
        order_json["updated_at"] = order.updated_at

        ordered_products = session.query(OrderedProduct).filter_by(order_id=order.id).all()
        ordered_products_processed = []
        for ordered_product in ordered_products :
            ordered_product_json = {}
            ordered_product_json["id"] = ordered_product.id
            ordered_product_json["order_id"] = ordered_product.order_id
            ordered_product_json["product_id"] = ordered_product.product_id
            ordered_product_json["quantity"] = ordered_product.quantity
            ordered_product_json["total_cost"] = ordered_product.total_cost
            ordered_product_json["created_at"] = ordered_product.created_at
            ordered_product_json["updated_at"] = ordered_product.updated_at

            product = session.query(Product).filter_by(id=ordered_product.product_id).first()
            ordered_product_json["product"] = product
            ordered_products_processed.append(ordered_product_json)

        order_json["ordered_products"] = ordered_products_processed
    return (True, order_json)
