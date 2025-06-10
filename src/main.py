from fastapi import FastAPI

from src.settings import get_settings
from src.users.handlers import router as user_router
from src.products.handlers import router as product_router

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(user_router, prefix=f"/{settings.API_VERSION}")
app.include_router(product_router, prefix=f"/{settings.API_VERSION}")
