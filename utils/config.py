from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str
    MONGODB_DB_NAME: str = "fintech_db"
    JWT_SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
