from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional

class TaskStatus(str, Enum):
    sin_empezar = "Sin Empezar"
    empezada = "Empezada"
    finalizada = "Finalizada"

class TaskBase(BaseModel):
    texto: str = Field(..., max_length=255)
    fecha_tentiva_finalizacion: Optional[datetime] = Field(
        None
    )
    estado: TaskStatus = Field(
        ...
    )
    category_id: int = Field(...)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    texto: Optional[str] = Field(None, max_length=255)
    fecha_tentiva_finalizacion: Optional[datetime]
    estado: Optional[TaskStatus]
    category_id: Optional[int]

class TaskResponse(TaskBase):
    id: int
    fecha_creacion: datetime = Field(...)
    user_id: int = Field(...)

    class Config:
        orm_mode = True 
