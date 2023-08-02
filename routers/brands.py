from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from services import brands
from dtos.brands import BrandInput
from dependencies import *

router = APIRouter(prefix="/api/brands", tags=["brands"])

@router.get("/")
async def get_all_brands(session: Session = Depends(get_session)):
    success, data = brands.get_all_brands(session)
    return data

@router.put("/{brand_id}", dependencies=[Depends(authorize_admin_access)])
async def update_brand(input: BrandInput, brand_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = brands.update_brand(session=session, brand_id=brand_id, name=input.name, description=input.description)
    if success:
        return {"message": data}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        ) 
    
@router.post("/", dependencies=[Depends(authorize_admin_access)])
async def create_brand(input: BrandInput, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = brands.add_brand(session=session, name=input.name, description=input.description)
    if success:
        return {"message": data}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        ) 
    
@router.delete("/{brand_id}", dependencies=[Depends(authorize_admin_access)])
async def delete_brand(brand_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = brands.delete_brand(session, brand_id=brand_id)
    if success:
        return {"message": data}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        ) 
