from database import create_session
from models import *
from dtos.orders import *

from services.coupons import get_all_coupons

session = create_session()

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

print(order_json)




        
