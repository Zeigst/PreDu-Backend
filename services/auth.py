from datetime import datetime, timedelta
from typing import Union
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import jwt

from models import User

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def encode_token(session: Session, username: str, password: str):
    user: User = session.query(User).filter_by(username=username).first()
    if user:
        if not verify_password(password, user.password):
            return (False, "Incorrect Password")
        else:
            data = {
                "id": f"{user.id}",
                "firstname": f"{user.firstname}",
                "lastname": f"{user.lastname}",
                "username": f"{user.username}",
                "phone": f"{user.phone}",
                "email": f"{user.email}",
                "location": f"{user.location}",
                "role": user.role,
            }
            return (True, create_access_token(data, timedelta(hours=48)))
    elif user == None:
        return (False, "User Not Found")