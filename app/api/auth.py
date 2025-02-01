from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.db.database import SessionLocal
from app.schemas.auth import Token, TokenData
from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, get_user_by_username
from app.core.security import (
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    oauth2_scheme
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, nombre_usuario=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user.nombre_usuario)
    if existing_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
    return create_user(db, user)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.contrasenia):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    access_token = create_access_token(
        data={"sub": user.nombre_usuario},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user