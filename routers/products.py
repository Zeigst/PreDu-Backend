from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from services import products

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("/")
async def get_all_products(session: Session = Depends(get_session)):
    success, data = products.get_all_products(session)
    return data