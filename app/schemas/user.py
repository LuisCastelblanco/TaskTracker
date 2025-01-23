from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    nombre_usuario: str = Field(..., max_length=50)
    imagen_perfil: Optional[str] = Field(None)

class UserCreate(UserBase):
    contrasenia: str = Field(..., min_length=8, )

class UserUpdate(BaseModel):
    nombre_usuario: Optional[str] = Field(None, max_length=50)
    contrasenia: Optional[str] = Field(None, min_length=8)
    imagen_perfil: Optional[str] = None

class UserResponse(UserBase):
    id: int = Field(..., )

    class Config:
        orm_mode = True 
