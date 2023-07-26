from models import *
from sqlalchemy.orm import Session

def get_all_categories(session: Session):
    categories = session.query(Category).order_by(Category.id.asc()).all()
    return (True, categories)

def get_category_by_name(session: Session, category_name: str):
    category = session.query(Category).filter_by(name=category_name).first()
    if (not category):
        return (False, "Category does not exist")
    return (True, category)

def get_category(session: Session, category_id: int):
    category = session.query(Category).filter_by(id=category_id).first()
    if (not category):
        return (False, "Category does not exist")
    return (True, category)

def add_category(session: Session, name: str, description: str):
    old_category = session.query(Category).filter_by(name=name).first()
    if (old_category):
        return (False, 'Category already exists')
    
    new_category = Category(name=name, description=description)
    session.add(new_category)
    session.commit()
    return (True, "Created Category {}".format(name))

def update_category(session: Session, category_id: int, name: str, description: str):
    category = session.query(Category).filter_by(id=category_id).first()
    if (not category):
        return (False, "Category does not exist")
    
    if (name):
        old_category = session.query(Category).filter_by(name=name).first()
        if (old_category.id != category_id):
            return (False, "Category name already exists")
        else:
            category.name = name
    
    if (description):
        category.description = description

    session.commit()
    return (True, f"Updated Category {category_id}")

def delete_category(session: Session, category_id: int):
    category = session.query(Category).filter_by(id=category_id).first()
    if not category:
        return (False, 'Category does not exist')
    session.delete(category)
    session.commit()
    return (True, "Deleted Category {}".format(category_id))

def get_brands(session: Session, category_id: int):
    filtered_products = session.query(Product).filter(Product.category_id == category_id)
    distinct_brands = filtered_products.with_entities(Product.brand_id).distinct().all()
    distinct_brand_ids = [brand_id for brand_id, in distinct_brands]
    return (True, distinct_brand_ids)
