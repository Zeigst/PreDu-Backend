from models import *
from sqlalchemy.orm import Session

def get_all_brands(session: Session):
    brands = session.query(Brand).order_by(Brand.id.asc()).all()
    return (True, brands)

def get_brand_by_name(session: Session, brand_name: str):
    brand = session.query(Brand).filter_by(name=brand_name).first()
    if (not brand):
        return (False, "Brand does not exist")
    return (True, brand)

def get_brand(session: Session, brand_id: int):
    brand = session.query(Brand).filter_by(id=brand_id).first()
    if (not brand):
        return (False, "Brand does not exist")
    return (True, brand)

def add_brand(session: Session, name: str, description: str):
    old_brand = session.query(Brand).filter_by(name=name).first()
    if (old_brand):
        return (False, 'Brand already exists')
    
    new_brand = Brand(name=name, description=description)
    session.add(new_brand)
    session.commit()
    return (True, "Created Brand {}".format(name))

def update_brand(session: Session, brand_id: int, name: str, description: str):
    brand = session.query(Brand).filter_by(id=brand_id).first()
    if (not brand):
        return (False, "Brand does not exist")
    
    if (name):
        old_brand = session.query(Brand).filter_by(name=name).first()
        if (old_brand.id != brand_id):
            return (False, "Brand name already exists")
        else:
            brand.name = name
    
    if (description):
        brand.description = description
    session.commit()
    return (True, f"Updated Brand {brand_id}")

def delete_brand(session: Session, brand_id: int):
    brand = session.query(Brand).filter_by(id=brand_id).first()
    if not brand:
        return (False, 'Brand does not exist')
    session.delete(brand)
    session.commit()
    return (True, "Deleted brand {}".format(brand_id))