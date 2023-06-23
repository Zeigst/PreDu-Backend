from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from services import coupons
from dtos.coupons import CouponOutput


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