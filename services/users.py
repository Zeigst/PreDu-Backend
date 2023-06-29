from models import *
from sqlalchemy.orm import Session
import re
from services import auth


def change_password(session: Session, current_user: User, current_password: str, new_password: str , confirm_password: str):
    if new_password != confirm_password:
        return (False, "Incorrrect confirmation of new password")
    user = session.query(User).filter_by(username=current_user.username).first()
    if not auth.verify_password(current_password, user.password):
        return (False, "Incorrect Password")
    if len(new_password) < 6:
        return (False, 'Password is too short')
    elif current_password == new_password:
        return (False, "New password must be different from current password")
    else:
        new_password_hashed = auth.get_password_hash(new_password)
        user.password = new_password_hashed
        session.commit()
        return (True, "Change Successful")
    

def change_username(session: Session, current_user: User, new_username: str, password: str):
    regex_username = '^[a-zA-Z0-9]+([a-zA-Z0-9](_|-| )[a-zA-Z0-9])*[a-zA-Z0-9]+$'
    if not re.search(regex_username, new_username):
        return (False, 'Invalid Username')
    old_user = session.query(User).filter_by(username=new_username).first()
    if old_user:
        return (False, "Username already exists")
    user = session.query(User).filter_by(username=current_user.username).first()
    if not auth.verify_password(password, user.password):
        return (False, "Incorrect Password")
    else:
        user.username = new_username
        session.commit()
        return (True, "Change Successful")
    

def add_user(session: Session, username: str, password: str, confirm_password: str, firstname: str, lastname: str,
             phone: str, email: str, location: str, role: str):
    regex_username = '^[a-zA-Z0-9]+([a-zA-Z0-9](_|-| )[a-zA-Z0-9])*[a-zA-Z0-9]+$'
    if not re.search(regex_username, username):
        return (False, 'Invalid Username')

    regex_name = '[^a-zA-Z\s]'
    if re.search(regex_name, firstname):
        return (False, 'Invalid Name')
    if re.search(regex_name, lastname):
        return (False, 'Invalid Name')
    
    
    if len(password) < 6:
        return (False, 'Password is too short')
    if password != confirm_password:
        return (False, 'The password confirmation does not match')

    user = session.query(User).filter_by(username=username).first()
    if user:
        return (False, 'Username already exists')

    new_user = User(username=username, password=auth.get_password_hash(password), firstname=firstname,
                    lastname=lastname, phone=phone, email=email, location=location, role=role, currently_active=True)
    session.add(new_user)
    session.commit()
    return (True, "Created User {}".format(username))


def get_user(session: Session, user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if (not user):
        return (False, "User does not exist")
    return (True, user)


def get_user_by_username(session: Session, username: str):
    user = session.query(User).filter_by(username=username).first()
    if (not user):
        return (False, "User does not exist")
    return (True, user)


def get_users(session: Session):
    users = session.query(User).all()
    return users


def update_user(session: Session, user_id: int, firstname: str, lastname: str, phone: str, email: str, 
                location: str, role: str):
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        return (False, 'User does not exist')
    if (firstname):
        user.firstname = firstname
    if (lastname):
        user.lastname = lastname
    if (phone):
        user.phone = phone
    if (email):
        user.email = email
    if (location):
        user.location = location
    if (role):
        user.role = role

    session.commit()
    return (True, "Updated User {}".format(user.username))


def delete_user(session: Session, user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        return (False, 'User does not exist')
    session.delete(user)
    session.commit()
    return (True, "Deleted User {}".format(user_id))