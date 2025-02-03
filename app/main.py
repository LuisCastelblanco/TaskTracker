# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


origins = [
    "http://localhost:5173",  
    "http://localhost:3000",  
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_db()

from app.api import auth, tasks, categories, user

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(user.router, prefix="/users", tags=["users"])

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to TaskTracker API"}

def setup_postman_generator(app: FastAPI):
    """Setup Postman collection generator routes."""
    app.include_router(router, prefix="/postman", tags=["postman"])