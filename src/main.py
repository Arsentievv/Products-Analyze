from fastapi import FastAPI

from src.settings import get_settings
from src.users.handlers import router as user_router

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(user_router, prefix=f"/{settings.API_VERSION}")
