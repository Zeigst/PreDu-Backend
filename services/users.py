from models import *
from sqlalchemy.orm import Session
import re
from services import auth


def change_password(session: Session, user: User, current_password: str, new_password: str , confirm_password: str):
    if new_password != confirm_password:
        return (False, "Incorrrect confirmation of new password")
    user = session.query(User).filter_by(username=user.username).first()
    if not auth.verify_password(current_password, user.password):
        return (False, "Incorrect Password")
    elif current_password == new_password:
        return (False, "New password must be different from current password")
    else:
        new_password_hashed = auth.get_password_hash(new_password)
        user.password = new_password_hashed
        session.commit()
        return (True, "Change Successful")


def add_user(session: Session, fullname: str, username: str, password: str, confirm_password: str, 
             phone: str, email: str, location: str, is_admin: bool):
    regex_user = '^[a-zA-Z0-9]+([a-zA-Z0-9](_|-| )[a-zA-Z0-9])*[a-zA-Z0-9]+$'
    if not re.search(regex_user, username):
        return (False, 'Invalid Username')

    regex_username = '[^a-zA-Z\d\s:]'
    if re.search(regex_username, fullname):
        return (False, 'Invalid Name')
    if len(password) < 6:
        return (False, 'Password is too short')
    if password != confirm_password:
        return (False, 'The password confirmation does not match')

    user = session.query(User).filter_by(username=username).first()
    if user:
        return (False, 'Username already exists')

    new_user = User(username=username, password=auth.get_password_hash(password), 
        fullname=fullname, phone=phone, email=email, location=location, is_admin=is_admin, is_active=True)
    session.add(new_user)
    session.commit()
    return (True, "Created {}".format(username))


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


def update_user(session: Session, user_id: int, fullname: str, phone: str, email: str, location: str):
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        return (False, 'User does not exist')
    if (fullname):
        user.fullname = fullname
    if (phone):
        user.phone = phone
    if (email):
        user.email = email
    if (location):
        user.location = location

    session.commit()
    return (True, "Updated {}".format(user.username))




def delete_user(session: Session, user_id: int):
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        return (False, 'User does not exist')
    session.delete(user)
    session.commit()
    return (True, "Deleted {}".format(user_id))