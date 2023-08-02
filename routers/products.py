from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from services import products
from dtos.products import ProductInput
from dependencies import *
from models import *

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("/")
async def get_all_products(session: Session = Depends(get_session)):
    success, data = products.get_all_products(session)
    return data

@router.put("/{product_id}", dependencies=[Depends(authorize_admin_access)])
async def update_product(input: ProductInput, product_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = products.update_product(session=session, product_id=product_id, name=input.name, description=input.description,
                                             image=input.image, category_id=input.category_id, brand_id=input.brand_id, 
                                             cost_per_unit=input.cost_per_unit, stock_quantity=input.stock_quantity)
    if success:
        return {"message": data}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
@router.post("/", dependencies=[Depends(authorize_admin_access)])
async def add_product(input: ProductInput, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = products.add_product(session=session, name=input.name, description=input.description,
                                             image=input.image, category_id=input.category_id, brand_id=input.brand_id, 
                                             cost_per_unit=input.cost_per_unit, stock_quantity=input.stock_quantity)
    if success:
        return {"message": data}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
@router.delete("/{product_id}", dependencies=[Depends(authorize_admin_access)])
async def delete_product(product_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = products.delete_product(session=session, product_id=product_id)
    if success:
        return {"message": data}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        )
