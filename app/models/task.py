from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String)
    fecha_creacion = Column(DateTime)
    fecha_tentiva_finalizacion = Column(DateTime)
    estado = Column(Enum("Sin Empezar", "Empezada", "Finalizada", name="task_status"))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category")
