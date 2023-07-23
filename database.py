from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import *
import os
from dotenv import load_dotenv

load_dotenv()


def init_db():
    engine = create_engine(os.getenv("DB_URL"))
    Base.metadata.create_all(bind = engine)


def create_session():
    engine = create_engine(os.getenv("DB_URL"))
    Session = sessionmaker(bind=engine)
    return Session()

def get_session():
    session = create_session()
    try:
        yield session
    finally:
        session.close()

init_db()