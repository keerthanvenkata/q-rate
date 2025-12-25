from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "q-rate"
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/qrate_db"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
