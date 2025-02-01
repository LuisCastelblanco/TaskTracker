from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    descripcion = Column(String)
    tasks = relationship("Task", back_populates="category")
    