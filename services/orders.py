from models import *
from sqlalchemy.orm import Session
from services.products import get_product_by_id, check_stock
from services.coupons import get_coupon_by_code, validate_coupon, get_discount_value
from services.ordered_products import add_ordered_product, get_ordered_products_by_order_id, cancel_ordered_product
from services.used_coupons import add_used_coupon, get_used_coupon_by_order_id, cancle_used_coupon


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

    if message == "Valid Coupon":
        applied_coupon = True
    else:
        applied_coupon = False

    order = Order(
        status = "processing", 
        user_id = current_user.id,
        
        user_firstname = current_user.firstname,
        user_lastname = current_user.lastname,
        user_phone = current_user.phone,
        user_email = current_user.email,
        user_location = current_user.location,

        applied_coupon = applied_coupon,
        raw_total_cost = total_cost, 
        final_total_cost = final_cost
    )
        
    session.add(order)
    session.flush()

    if message == "Valid Coupon":
        success, coupon = get_coupon_by_code(session, coupon_code)
        success, data = add_used_coupon(session, current_user, coupon, order, discount_value)

    product_ids = cart.keys()
    for product_id in product_ids:
        if cart[product_id] > 0:
            success, product = get_product_by_id(session, product_id)
            success, data = add_ordered_product(session, order, product, cart[product_id])
    
    session.commit()
    return (True, {"order_id": order.id, "message": f"Created Order {order.id}"})


def get_user_orders(session: Session, user: User):
    orders = session.query(Order).filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
    
    processed_orders = []
    for order in orders:
        success, ordered_products = get_ordered_products_by_order_id(session, order.id)
        if order.applied_coupon:
            success, used_coupon = get_used_coupon_by_order_id(session, order.id)
        else:
            used_coupon = {}
        
        order_json = {}
        order_json["id"] = order.id
        order_json["user_id"] = order.user_id

        order_json["user_firstname"] = order.user_firstname
        order_json["user_lastname"] = order.user_lastname
        order_json["user_phone"] = order.user_phone
        order_json["user_email"] = order.user_email
        order_json["user_location"] = order.user_location
        
        order_json["status"] = order.status
        order_json["applied_coupon"] = order.applied_coupon
        order_json["raw_total_cost"] = order.raw_total_cost
        order_json["final_total_cost"] = order.final_total_cost

        order_json["ordered_products"] = ordered_products
        order_json["used_coupon"] = used_coupon

        order_json["created_at"] = order.created_at
        order_json["updated_at"] = order.updated_at

        processed_orders.append(order_json)
        
    return (True, processed_orders)


def get_order_by_id(session: Session, user: User, order_id: int): 
    order = session.query(Order).filter_by(id=order_id).first()
    if not order:
        return (False, "Order Do Not Exist")
    if user.role != "admin":
        if order.user_id != user.id:
            return (False, "Invalid Credentials")
    
    success, ordered_products = get_ordered_products_by_order_id(session, order.id)
    if order.applied_coupon:
        success, used_coupon = get_used_coupon_by_order_id(session, order.id)
    else:
        used_coupon = {}
    
    order_json = {}
    order_json["id"] = order.id
    order_json["user_id"] = order.user_id

    order_json["user_firstname"] = order.user_firstname
    order_json["user_lastname"] = order.user_lastname
    order_json["user_phone"] = order.user_phone
    order_json["user_email"] = order.user_email
    order_json["user_location"] = order.user_location
    
    order_json["status"] = order.status
    order_json["applied_coupon"] = order.applied_coupon
    order_json["raw_total_cost"] = order.raw_total_cost
    order_json["final_total_cost"] = order.final_total_cost

    order_json["ordered_products"] = ordered_products
    order_json["used_coupon"] = used_coupon

    order_json["created_at"] = order.created_at
    order_json["updated_at"] = order.updated_at

    return (True, order_json)


def cancel_order(session: Session, user: User, order_id: int):
    order = session.query(Order).filter_by(id=order_id).first()
    if not order:
        return (False, "Order Do Not Exist")
    if user.role != "admin":
        if user.id != order.user_id:
            return (False, "Invalid Credentials")
    if order.status == "canceled":
        return (False, "Order Already Canceled")
    if order.status == "completed":
        return (False, "Order Already Completed")
    
    order.status = "canceled"
    success, ordered_products = get_ordered_products_by_order_id(session=session, order_id=order_id)
    for ordered_product in ordered_products:
        success, data = cancel_ordered_product(session=session, ordered_product=ordered_product)

    success, used_coupon = get_used_coupon_by_order_id(session=session, order_id=order_id)
    success, data = cancle_used_coupon(session=session, used_coupon=used_coupon)

    session.commit()
    return (True, "Order Canceled")

def complete_order(session: Session, order_id: int):
    order = session.query(Order).filter_by(id=order_id).first()
    if not order:
        return (False, "Order Do Not Exist")
    if order.status == "canceled":
        return (False, "Order Already Canceled")
    if order.status == "completed":
        return (False, "Order Already Completed")
    
    order.status = "completed"
    session.commit()
    return (True, "Order Completed")
    
def get_orders(session: Session):
    orders = session.query(Order).order_by(Order.id.asc()).all()
    return (True, orders)
