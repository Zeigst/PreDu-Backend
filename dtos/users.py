from models import User
from pydantic import BaseModel

class UserOutput:
    id: int
    username: str
    firstname: str
    lastname: str
    phone: str
    email: str
    location: str
    is_admin: bool
    is_active: bool

    def __init__(self, user: User):
        self.id = user.id
        self.username = user.username
        self.firstname = user.firstname
        self.lastname = user.lastname
        self.phone = user.phone
        self.email = user.email
        self.location = user.location
        self.role = user.role
        self.currently_active = user.currently_active

class UserSignupInput(BaseModel):
    firstname: str
    lastname: str
    username: str
    password: str
    confirm_password: str
    phone: str
    email: str
    location: str
        