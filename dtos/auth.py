from ctypes import Union
from fastapi import FastAPI
from pydantic import BaseModel

class LoginInput(BaseModel):
    username: str
    password: str

class LoginOutput(BaseModel):
    access_token: str
    token_type: str

class ChangePasswordInput(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

class ChangePasswordOutput(BaseModel):
    message: str

class ChangeUsernameInput(BaseModel):
    new_username: str
    password:str

class ChangeUsernameOutput(BaseModel):
    message: str
    access_token: str