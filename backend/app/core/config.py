from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Central application configuration.

    All values are overridable via environment variables or a .env file —
    see .env.example in the project root for the full list.
    """

    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "dealership"
    jwt_secret_key: str = "change-me-in-.env"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24 hours

    class Config:
        env_file = ".env"


settings = Settings()
