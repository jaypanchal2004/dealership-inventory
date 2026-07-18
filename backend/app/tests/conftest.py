import pytest_asyncio
from beanie import init_beanie
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient

from app.core.security import create_access_token, hash_password
from app.main import app
from app.models.user import User, UserRole
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


@pytest_asyncio.fixture
async def customer_headers(client):
    """Registers a regular customer and returns an Authorization header for them."""
    await client.post(
        "/api/auth/register",
        json={
            "username": "customer1",
            "email": "customer1@example.com",
            "password": "SecurePass123!",
        },
    )
    login = await client.post(
        "/api/auth/login",
        json={"email": "customer1@example.com", "password": "SecurePass123!"},
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def admin_headers():
    """
    Creates an admin user directly via the model (not the register endpoint,
    since public registration never grants the ADMIN role) and returns an
    Authorization header for them.
    """
    admin = User(
        username="admin1",
        email="admin1@example.com",
        password_hash=hash_password("AdminPass123!"),
        role=UserRole.ADMIN,
    )
    await admin.insert()
    token = create_access_token(data={"sub": str(admin.id), "role": admin.role.value})
    return {"Authorization": f"Bearer {token}"}
