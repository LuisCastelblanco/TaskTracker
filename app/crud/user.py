# app/crud/user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.contrasenia)
    db_user = User(
        nombre_usuario=user.nombre_usuario,
        contrasenia=hashed_password,  # Changed from hashed_contrasenia to contrasenia
        imagen_perfil=user.imagen_perfil
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, nombre_usuario: str):
    return db.query(User).filter(User.nombre_usuario == nombre_usuario).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None  

    if user.nombre_usuario is not None:
        db_user.nombre_usuario = user.nombre_usuario
    if user.contrasenia is not None:
        db_user.contrasenia = get_password_hash(user.contrasenia)  # Changed from hashed_contrasenia to contrasenia
    if user.imagen_perfil is not None:
        db_user.imagen_perfil = user.imagen_perfil

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None  

    db.delete(db_user)
    db.commit()
    return db_user