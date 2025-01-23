import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Task Tracker"
    VERSION: str = "0.1.0"

settings = Settings()
