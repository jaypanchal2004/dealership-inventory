from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.core.config import settings
from app.models.user import User
from app.models.vehicle import Vehicle


async def init_db() -> None:
    """
    Connect to the real MongoDB instance and register Beanie document models.

    Called once at application startup (see main.py's lifespan handler).
    The test suite does NOT use this — tests initialize an isolated
    in-memory mock instead (see app/tests/conftest.py) so they stay fast
    and independent of a running Mongo server.
    """
    client = AsyncIOMotorClient(settings.mongodb_uri)
    await init_beanie(
        database=client[settings.database_name],
        document_models=[User, Vehicle],
    )
