from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = BASE_DIR / ".env"


settings = Settings()
