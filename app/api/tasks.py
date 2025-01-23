from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.crud.task import create_task, get_task, get_tasks, update_task, delete_task
from app.db.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TaskResponse)
def create_task_endpoint(task: TaskCreate, db: Session = Depends(get_db), user_id: int = 1):
 
    return create_task(db, task, user_id)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task_endpoint(task_id: int, db: Session = Depends(get_db)):
 
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="No se encontró el Task")
    return task

@router.get("/", response_model=list[TaskResponse])
def get_tasks_endpoint(db: Session = Depends(get_db), user_id: int = 1, skip: int = 0, limit: int = 100):
  
    return get_tasks(db, user_id, skip, limit)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
   
    updated_task = update_task(db, task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="No se encontró el Task")
    return updated_task

@router.delete("/{task_id}", response_model=TaskResponse)
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):

    deleted_task = delete_task(db, task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="No se encontro el Task")
    return deleted_task
