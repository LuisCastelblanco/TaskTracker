from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Category(base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    descripcion = Column(String)
    