import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class AnalyzerBaseSettings(BaseSettings):
    PROJECT_NAME: str = "Products Analizer"
    API_VERSION: str = "API_V001"
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ENCODE_ALGORYTHM: str = os.environ.get("ENCODE_ALGORYTHM")


class AnalyzerDBSettings(AnalyzerBaseSettings):
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD")
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: int = os.environ.get("DB_PORT")

    @property
    def get_db_uri(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@" \
               f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


def get_settings(db=False):
    if db:
        return AnalyzerDBSettings()
    else:
        return AnalyzerBaseSettings()

