from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from dtos.users import UserSignupInput
from services import users

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/signup")
async def signup(input: UserSignupInput, session: Session = Depends(get_session)):
    success, data = users.add_user(session, input.username, input.password, input.confirm_password,
                                  input.firstname, input.lastname, input.phone, input.email, input.location, "user")
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return data