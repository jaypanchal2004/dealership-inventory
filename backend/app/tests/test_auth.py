import pytest


class TestUserRegistration:
    @pytest.mark.asyncio
    async def test_register_new_user_returns_201(self, client):
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "johndoe",
                "email": "john@example.com",
                "password": "SecurePass123!",
            },
        )

        assert response.status_code == 201
        body = response.json()
        assert body["username"] == "johndoe"
        assert body["email"] == "john@example.com"
        assert "password" not in body
        assert "password_hash" not in body

    @pytest.mark.asyncio
    async def test_register_duplicate_email_returns_400(self, client):
        payload = {
            "username": "johndoe",
            "email": "john@example.com",
            "password": "SecurePass123!",
        }
        await client.post("/api/auth/register", json=payload)

        response = await client.post("/api/auth/register", json=payload)

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_register_missing_field_returns_422(self, client):
        response = await client.post(
            "/api/auth/register",
            json={"email": "john@example.com", "password": "SecurePass123!"},
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_short_password_returns_422(self, client):
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "johndoe",
                "email": "john@example.com",
                "password": "short",
            },
        )

        assert response.status_code == 422


class TestUserLogin:
    @pytest.mark.asyncio
    async def test_login_with_correct_credentials_returns_token(self, client):
        await client.post(
            "/api/auth/register",
            json={
                "username": "johndoe",
                "email": "john@example.com",
                "password": "SecurePass123!",
            },
        )

        response = await client.post(
            "/api/auth/login",
            json={"email": "john@example.com", "password": "SecurePass123!"},
        )

        assert response.status_code == 200
        body = response.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_with_wrong_password_returns_401(self, client):
        await client.post(
            "/api/auth/register",
            json={
                "username": "johndoe",
                "email": "john@example.com",
                "password": "SecurePass123!",
            },
        )

        response = await client.post(
            "/api/auth/login",
            json={"email": "john@example.com", "password": "WrongPassword"},
        )

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_with_unknown_email_returns_401(self, client):
        response = await client.post(
            "/api/auth/login",
            json={"email": "ghost@example.com", "password": "SecurePass123!"},
        )

        assert response.status_code == 401
