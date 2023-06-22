from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from services import categories


router = APIRouter(prefix="/api/categories", tags=["categories"])

@router.get("/")
async def get_all_categories(session: Session = Depends(get_session)):
    success, data = categories.get_all_categories(session)
    return data

@router.get("/brands/{category_id}")
async def get_brands(category_id: int, session: Session = Depends(get_session)):
    success, data = categories.get_brands(session, category_id)
    return data