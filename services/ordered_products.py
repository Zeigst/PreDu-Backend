from models import *
from sqlalchemy.orm import Session

def add_ordered_product(session: Session, order_id: int, product_id: int, quantity: int):
    product = session.query(Product).filter_by(id=product_id).first()
    product.stock_quantity = product.stock_quantity - quantity
    total_cost = product.cost_per_unit * quantity

    ordered_product = OrderedProduct(order_id=order_id, product_id=product.id, quantity=quantity, total_cost=total_cost)
    session.add(ordered_product)
    session.flush()
    session.commit()
    return (True, f"Add Orderd Product {ordered_product.id}")