from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from models import *
from dtos.oders import OrderInput
from dependencies import get_current_user

from services import orders

router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("/")
async def make_order(input: OrderInput, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = orders.add_order(session, current_user, input.coupon_code, input.cart)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return data

@router.get("/{user_id}")
async def get_orders(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = orders.get_orders(session, current_user)
    return data