from pydantic import BaseModel, Field
from typing import Optional

class CategoryBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)

class CategoryResponse(CategoryBase):
    id: int = Field(...)

    class Config:
        orm_mode = True  
