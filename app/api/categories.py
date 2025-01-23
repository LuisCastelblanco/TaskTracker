from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.crud.category import create_category, get_category, get_categories, update_category, delete_category
from app.db.database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CategoryResponse)
def create_category_endpoint(category: CategoryCreate, db: Session = Depends(get_db)):
 
    return create_category(db, category)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category_endpoint(category_id: int, db: Session = Depends(get_db)):
  
    category = get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="No se encuentra la categoria")
    return category

@router.get("/", response_model=list[CategoryResponse])
def get_categories_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    return get_categories(db, skip, limit)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category_endpoint(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):

    updated_category = update_category(db, category_id, category)
    if not updated_category:
        raise HTTPException(status_code=404, detail="No se encuentra la categoria")
    return updated_category

@router.delete("/{category_id}", response_model=CategoryResponse)
def delete_category_endpoint(category_id: int, db: Session = Depends(get_db)):
  
    deleted_category = delete_category(db, category_id)
    if not deleted_category:
        raise HTTPException(status_code=404, detail="No se encuentra la categoria")
    return deleted_category
