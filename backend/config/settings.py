from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_env: str = "development"
    database_url: str
    jwt_secret: str
    jwt_algorithm: str = Field(default="HS256", validation_alias=AliasChoices("JWT_ALGORITHM", "ALGORITHM"))
    access_token_expire_minutes: int = 60
    iot_api_key: str = "change_me_iot_api_key"
    frontend_url: str = "http://localhost:3000"

    class Config:
        # Support starting uvicorn from the repo root OR from backend/ directory
        env_file = ("backend/.env", ".env")
        case_sensitive = False
        extra = "ignore"


settings = Settings()
