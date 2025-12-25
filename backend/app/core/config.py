from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "q-rate"
    GEMINI_API_KEY: str = "TODO_ADD_KEY"
    GEMINI_MODEL_NAME: str = "gemini-2.0-flash-exp"
    
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings()
