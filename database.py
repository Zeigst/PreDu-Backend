from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import *

def init_db():
    engine = create_engine(
        # "mysql+pymysql://usdxmdmf_meocon:shy*}xgkySOf@45.252.251.44/usdxmdmf_wifiattendance?charset=utf8mb4")
        "postgresql://postgres:CHM19902@localhost/predu")
    Base.metadata.create_all(bind = engine)


def create_session():
    engine = create_engine(
        # "mysql+pymysql://usdxmdmf_meocon:shy*}xgkySOf@45.252.251.44/usdxmdmf_wifiattendance?charset=utf8mb4")
        "postgresql://postgres:CHM19902@localhost/predu")
    Session = sessionmaker(bind=engine)
    return Session()


init_db()