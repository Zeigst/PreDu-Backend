from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from database import get_session
from sqlalchemy.orm import Session
from jose import JWTError
from models import User
from services import auth, users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth.decode_token(token)
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    success, user_data = users.get_user_by_username(session, username)
    if user_data is None:
        raise credentials_exception
    return user_data

async def authorize_admin_access(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth.decode_token(token)
        role: str = payload.get("role")
        if role is None:
            raise credentials_exception
        elif role == "user":
            raise credentials_exception
    except JWTError:
        raise credentials_exception