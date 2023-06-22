from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from services import coupons
from dtos.coupons import CouponOutput


router = APIRouter(prefix="/api/coupons", tags=["coupons"])

@router.get("/{coupon_code}")
async def get_coupon_by_code(coupon_code: str, session: Session = Depends(get_session)):
    success, data = coupons.get_coupon_by_code(session, coupon_code)
    return CouponOutput(data)