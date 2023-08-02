from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import *
from database import get_session
from dtos.users import UserSignupInput, UpdateUserInput
from dependencies import get_current_user, authorize_admin_access
from services import users, orders, used_coupons

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/")
async def signup(input: UserSignupInput, session: Session = Depends(get_session)):
    success, data = users.add_user(session, input.username, input.password, input.confirm_password,
                                  input.firstname, input.lastname, input.phone, input.email, input.location, "user")
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": data}

@router.patch("/update-user")
async def update_user(input: UpdateUserInput, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = users.update_user(session=session, user_id=current_user.id, firstname=input.firstname, lastname=input.lastname,
                                      phone=input.phone, email=input.email, location=input.location, role="user")
    if success:
        return {"message": data}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        )  
    
@router.patch("/update-admin", dependencies=[Depends(authorize_admin_access)])
async def update_admin(input: UpdateUserInput, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = users.update_user(session=session, user_id=current_user.id, firstname=input.firstname, lastname=input.lastname,
                                      phone=input.phone, email=input.email, location=input.location, role="admin")
    if success:
        return {"message": data}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        )  

@router.get("/order-history")
async def get_order_history(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = orders.get_user_orders(session=session, user=current_user)
    return data

@router.get("/coupon-history")
async def get_coupon_history(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = used_coupons.get_user_used_coupons(session=session, user=current_user)
    return data


@router.get("/", dependencies=[Depends(authorize_admin_access)])
async def get_users(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = users.get_users(session=session)
    return data