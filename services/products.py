from models import *
from sqlalchemy.orm import Session

def get_all_products(session: Session):
    products = session.query(Product).order_by(Product.id.asc()).all()
    return (True, products)

def get_product_by_id(session: Session, product_id: int):
    product = session.query(Product).filter_by(id=product_id).first()
    return (True, product)

def get_product_by_name(session: Session, product_name: str):
    product = session.query(Product).filter_by(name=product_name).first()
    return (True, product)

def check_stock(session: Session, product_id: int, quantity: int):
    product = session.query(Product).filter_by(id=product_id).first()
    if not product:
        return (False, "ERROR: Product Not Found")
    if quantity > product.stock_quantity:
        return (False, "ERROR: Product Out Of Stock")
    return (True, "Product In Stock")

def update_product(session: Session, product_id: int, name: str, description: str, image: str, category_id, 
                    brand_id, cost_per_unit: float, stock_quantity: int):
    product = session.query(Product).filter_by(id=product_id).first()
    if not product:
        return (False, "ERROR: Product Not Found") 
    
    old_product = session.query(Product).filter_by(name=name).first()
    if old_product:
        if old_product.id != product_id:
            return (False, "ERROR: Product Name Already Existed")
        
    if not isinstance(category_id, int):
        return (False, "ERROR: Invalid Category ID")
    if not isinstance(brand_id, int):
        return (False, "ERROR: Invalid Brand ID")
    if not isinstance(cost_per_unit, float) or cost_per_unit < 0:
        return (False, "ERROR: Invalid Cost")
    if not isinstance(stock_quantity, int) or stock_quantity < 0:
        return (False, "ERROR: Invalid Stock Quantity")
    
    category = session.query(Category).filter_by(id=category_id).first()
    if not category:
        return (False, "ERROR: Category Do Not Exist")
    
    brand = session.query(Brand).filter_by(id=brand_id).first()
    if not brand:
        return (False, "ERROR: Brand Do Not Exist")
    
    product.name = name
    product.description = description
    product.image = image
    product.category_id = category_id
    product.brand_id = brand_id
    product.stock_quantity = stock_quantity
    product.cost_per_unit = cost_per_unit

    session.commit()
    return (True, f"Updated Product {product_id}")

def add_product(session: Session, name: str, description: str, image: str, category_id, brand_id, 
                cost_per_unit: float, stock_quantity: int):
    
    old_product = session.query(Product).filter_by(name=name).first()
    if old_product:
        return (False, "ERROR: Product Name Already Existed")
        
    if not isinstance(category_id, int):
        return (False, "ERROR: Invalid Category ID")
    if not isinstance(brand_id, int):
        return (False, "ERROR: Invalid Brand ID")
    if not isinstance(cost_per_unit, float) or cost_per_unit < 0:
        return (False, "ERROR: Invalid Cost")
    if not isinstance(stock_quantity, int) or stock_quantity < 0:
        return (False, "ERROR: Invalid Stock Quantity")
    
    category = session.query(Category).filter_by(id=category_id).first()
    if not category:
        return (False, "ERROR: Category Do Not Exist")
    
    brand = session.query(Brand).filter_by(id=brand_id).first()
    if not brand:
        return (False, "ERROR: Brand Do Not Exist")
    
    new_product = Product(name=name, description=description, image=image, category_id=category_id, brand_id=brand_id, cost_per_unit=cost_per_unit, stock_quantity=stock_quantity)

    session.add(new_product)
    session.commit()
    return (True, f"Created Product {name}")

def delete_product(session: Session, product_id: int):
    product = session.query(Product).filter_by(id=product_id).first()
    if not product:
        return (False, 'Product Does Not Exist')
    session.delete(product)
    session.commit()
    return (True, "Deleted Product {}".format(product_id))