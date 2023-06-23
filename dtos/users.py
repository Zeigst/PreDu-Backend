from models import User

class UserOutput:
    id: int
    username: str
    fullname: str
    phone: str
    email: str
    location: str
    is_admin: bool
    is_active: bool

    def __init__(self, user: User):
        self.id = user.id
        self.username = user.username
        self.fullname = user.fullname
        self.phone = user.phone
        self.email = user.email
        self.location = user.location
        self.is_admin = user.is_admin
        self.is_active = user.is_active
        