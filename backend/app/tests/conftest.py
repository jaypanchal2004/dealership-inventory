import pytest_asyncio
from beanie import init_beanie
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient

from app.main import app
from app.models.user import User
from app.models.vehicle import Vehicle


@pytest_asyncio.fixture(autouse=True)
async def init_test_db():
    """
    Give every test a fresh, isolated in-memory MongoDB instance.

    This keeps the suite fast and prevents tests from leaking state into
    each other. The production app (app/core/database.py) still connects
    to a real MongoDB — mongomock is a *test-only* substitute, not a
    replacement for the required real database.
    """
    client = AsyncMongoMockClient()
    await init_beanie(
        database=client.get_database("test_db"),
        document_models=[User, Vehicle],
    )
    yield


@pytest_asyncio.fixture
async def client():
    """An httpx client wired directly to the FastAPI app, no real server needed."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
