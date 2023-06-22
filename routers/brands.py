from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from services import brands

router = APIRouter(prefix="/api/brands", tags=["brands"])

@router.get("/")
async def get_all_brands(session: Session = Depends(get_session)):
    success, data = brands.get_all_brands(session)
    return data