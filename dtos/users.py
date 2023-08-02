from models import User
from pydantic import BaseModel
from typing import Optional

class UserOutput:
    id: int
    username: str
    firstname: str
    lastname: str
    phone: str
    email: str
    location: str
    role: str

    def __init__(self, user: User):
        self.id = user.id
        self.username = user.username
        self.firstname = user.firstname
        self.lastname = user.lastname
        self.phone = user.phone
        self.email = user.email
        self.location = user.location
        self.role = user.role

class UserSignupInput(BaseModel):
    firstname: str
    lastname: str
    username: str
    password: str
    confirm_password: str
    phone: str
    email: str
    location: str
        
class UpdateUserInput(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    location: Optional[str]

class UpdateAdminInput(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    location: Optional[str]