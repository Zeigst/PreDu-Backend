from models import *
from sqlalchemy.orm import Session

def add_ordered_product(session: Session, order: Order, product: Product, quantity: int):
    product.stock_quantity = product.stock_quantity - quantity
    total_cost = product.cost_per_unit * quantity

    ordered_product = OrderedProduct(
        order_id = order.id, 
        product_id = product.id, 
        name = product.name, 
        description = product.description,
        cost_per_unit = product.cost_per_unit, 
        quantity = quantity, 
        total_cost = total_cost
    )
    
    session.add(ordered_product)
    session.flush()
    session.commit()
    return (True, f"Add Orderd Product {ordered_product.id}")

def get_ordered_products_by_order_id(session: Session, order_id: int):
    ordered_products = session.query(OrderedProduct).filter_by(order_id=order_id).all()
    return (True, ordered_products)

def cancel_ordered_product(session: Session, ordered_product: OrderedProduct):
    product = session.query(Product).filter_by(id=ordered_product.product_id).first()
    if not product:
        return (False, "Product No Longer Exist")
    if product.name != ordered_product.name:
        return (False, "Product No Longer Exist")
    
    product.stock_quantity = product.stock_quantity + ordered_product.quantity
    session.commit()
    return (True, f"Canceled Ordered Product {ordered_product.id}")
