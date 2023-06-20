from models import *
from services.auth import get_password_hash
from sqlalchemy.orm import Session
from database import create_session

def seed(session: Session):
    admin = session.query(User).filter_by(username="admin").first()
    if  not admin:
        admin = User(username="admin", fullname="admin",password=get_password_hash("admin"), 
                        phone="0911223333", email="admin@mail.com" ,is_admin=True, is_active=True)
        session.add(admin)
        session.commit()
    
    user = session.query(User).filter_by(username="user").first()
    if  not user:
        user = User(username="user", fullname="user",password=get_password_hash("user"), 
                        phone="0944556666", email="user@mail.com", is_admin=False, is_active=True)
        session.add(user)
        session.commit()

session = create_session()
seed(session)