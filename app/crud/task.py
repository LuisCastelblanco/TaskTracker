from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.category import Category
from datetime import datetime
from fastapi import HTTPException


def create_task(db: Session, task: TaskCreate, user_id: int):

    category = db.query(Category).filter(Category.id == task.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Categoria no encontrada")

    db_task = Task(
        texto=task.texto,
        fecha_creacion=datetime.now(),
        fecha_tentiva_finalizacion=task.fecha_tentiva_finalizacion,
        estado=task.estado,
        user_id=user_id,
        category_id=task.category_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()


    

def update_task(db: Session, task_id: int, task: TaskUpdate):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None  

    if task.texto is not None:
        db_task.texto = task.texto
    if task.fecha_tentiva_finalizacion is not None:
        db_task.fecha_tentiva_finalizacion = task.fecha_tentiva_finalizacion
    if task.estado is not None:
        db_task.estado = task.estado
    if task.category_id is not None:
        db_task.category_id = task.category_id

    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None  

    db.delete(db_task)
    db.commit()
    return db_task
