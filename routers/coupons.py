from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from models import *
from dependencies import *
from services import coupons
from dtos.coupons import CouponOutput, CouponInput


router = APIRouter(prefix="/api/coupons", tags=["coupons"])

@router.get("/{coupon_code}")
async def get_coupon_by_code(coupon_code: str, session: Session = Depends(get_session)):
    success, data = coupons.get_coupon_by_code(session, coupon_code)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return CouponOutput(data)

@router.get("/")
async def get_all_coupons(session: Session = Depends(get_session)):
    success, data = coupons.get_all_coupons(session=session)
    return data

@router.put("/{coupon_id}", dependencies=[Depends(authorize_admin_access)])
async def update_coupon(input: CouponInput, coupon_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = coupons.update_coupon(session=session, coupon_id=coupon_id, code=input.code, type=input.type, value=input.value, min_order_required=input.min_order_required,
                                           max_discount_applicable=input.max_discount_applicable, stock_quantity=input.stock_quantity, limit_per_user=input.limit_per_user, is_active=input.is_active)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": data}

@router.delete("/{coupon_id}", dependencies=[Depends(authorize_admin_access)])
async def delete_coupon(coupon_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = coupons.delete_coupon(session=session, coupon_id=coupon_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": data}

@router.post("/", dependencies=[Depends(authorize_admin_access)])
async def add_coupon(input: CouponInput, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = coupons.add_coupon(session=session, code=input.code, type=input.type, value=input.value, min_order_required=input.min_order_required,
                                           max_discount_applicable=input.max_discount_applicable, stock_quantity=input.stock_quantity, limit_per_user=input.limit_per_user, is_active=input.is_active)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": data}
