from pathlib import Path
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
        # Absolute path, independent of the current working directory the
        # app happens to be launched from. Adjust the number of .parent
        # calls if this file moves relative to the project root.
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"


settings = Settings()