from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    database_url: str
    test_database_url : str | None = None

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


settings = Settings()
