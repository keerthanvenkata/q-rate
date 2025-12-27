from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "q-rate"

    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5433/qrate_db"

    DEBUG: bool = True

    GEMINI_API_KEY: str = "TODO_ADD_KEY"

    GEMINI_MODEL_NAME: str = "gemini-3.0-flash"

    WHATSAPP_ACCESS_TOKEN: str = "TODO_ADD_TOKEN"

    WHATSAPP_PHONE_NUMBER_ID: str = "TODO_ADD_ID"

    WHATSAPP_VERIFY_TOKEN: str = "my_secure_verify_token"

    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=".env", env_ignore_empty=True, extra="ignore"
    )


settings = Settings()
