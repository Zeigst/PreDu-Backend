from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_session
from models import *
from services import categories
from dtos.categories import CategoryInput
from dependencies import *


router = APIRouter(prefix="/api/categories", tags=["categories"])

@router.get("/")
async def get_all_categories(session: Session = Depends(get_session)):
    success, data = categories.get_all_categories(session)
    return data

@router.get("/{category_id}/brands")
async def get_brands(category_id: int, session: Session = Depends(get_session)):
    success, data = categories.get_brands(session, category_id)
    return data

@router.put("/{category_id}", dependencies=[Depends(authorize_admin_access)])
async def update_category(input: CategoryInput, category_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = categories.update_category(session=session, category_id=category_id, name=input.name, description=input.description)
    if success:
        return {"message": data}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        ) 
    
@router.post("/", dependencies=[Depends(authorize_admin_access)])
async def create_category(input: CategoryInput, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = categories.add_category(session=session, name=input.name, description=input.description)
    if success:
        return {"message": data}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        ) 
    
@router.delete("/{category_id}", dependencies=[Depends(authorize_admin_access)])
async def delete_category(category_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    success, data = categories.delete_category(session, category_id=category_id)
    if success:
        return {"message": data}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=data,
            headers={"WWW-Authenticate": "Bearer"},
        ) 
