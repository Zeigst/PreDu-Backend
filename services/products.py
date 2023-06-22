from models import *
from sqlalchemy.orm import Session

def get_all_products(session: Session):
    products = session.query(Product).all()
    return (True, products)