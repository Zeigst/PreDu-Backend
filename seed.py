from models import *
from services.auth import get_password_hash
from database import create_session

def seed(session):
    admin = session.query(User).filter_by(username="admin").first()
    if  not admin:
        admin = User(username="admin", fullname="admin",password=get_password_hash("admin"), is_admin=True, is_active=True)
        session.add(admin)
        session.commit()
    
    user = session.query(User).filter_by(username="user").first()
    if  not user:
        user = User(username="user", fullname="user",password=get_password_hash("user"), is_admin=False, is_active=True)
        session.add(user)
        session.commit()

session = create_session()
seed(session)