from models import *

def get_category_by_name(session, category_name):
    category = session.query(Category).filter_by(name=category_name).first()
    if (not category):
        return (False, "Category does not exist")
    return (True, category)

def get_category(session, category_id):
    category = session.query(Category).filter_by(id=category_id).first()
    if (not category):
        return (False, "Category does not exist")
    return (True, category)

def add_category(session, name, description):
    old_category = session.query(Category).filter_by(name=name).first()
    if (old_category):
        return (False, 'Category already exists')
    
    new_category = Category(name=name, description=description)
    session.add(new_category)
    session.commit()
    return (True, "Created Category {}".format(name))

def update_category(session, category_id, name, description):
    category = session.query(Category).filter_by(id=category_id).first()
    if (not category):
        return (False, "Category does not exist")
    
    if (name):
        old_category = session.query(Category).filter_by(name=name).first()
        if (old_category):
            return (False, "Category name already exist")
        else:
            category.name = name
    
    if (description):
        category.description = name

def delete_category(session, category_id):
    category = session.query(Category).filter_by(id=category_id).first()
    if not category:
        return (False, 'User does not exist')
    session.delete(category)
    session.commit()
    return (True, "Deleted Category {}".format(category_id))