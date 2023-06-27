from models import *
from sqlalchemy.orm import Session

def get_all_products(session: Session):
    products = session.query(Product).all()
    return (True, products)

def get_product_by_id(session: Session, product_id: int):
    product = session.query(Product).filter_by(id=product_id).first()
    return (True, product)

def get_product_by_name(session: Session, product_name: int):
    product = session.query(Product).filter_by(name=product_name).first()
    return (True, product)

def check_stock(session: Session, product_id: int, quantity: int):
    product = session.query(Product).filter_by(id=product_id).first()
    if not product:
        return (False, "ERROR: Product Not Found")
    if quantity > product.stock_quantity:
        return (False, "ERROR: Product Out Of Stock")
    return (True, "Product In Stock")
        