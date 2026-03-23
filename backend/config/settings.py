from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_env: str = "development"
    database_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        # Support starting uvicorn from the repo root OR from backend/ directory
        env_file = ("backend/.env", ".env")
        case_sensitive = False


settings = Settings()
