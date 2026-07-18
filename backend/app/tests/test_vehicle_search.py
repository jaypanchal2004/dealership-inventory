import pytest


class TestSearchVehicles:
    @pytest.mark.asyncio
    async def test_search_requires_auth(self, client):
        response = await client.get("/api/vehicles/search")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_search_by_make_is_case_insensitive(self, client, customer_headers):
        await client.post(
            "/api/vehicles",
            json={"make": "Toyota", "model": "Corolla", "category": "Sedan", "price": 22000, "quantity": 5},
            headers=customer_headers,
        )
        await client.post(
            "/api/vehicles",
            json={"make": "Honda", "model": "Civic", "category": "Sedan", "price": 21000, "quantity": 3},
            headers=customer_headers,
        )

        response = await client.get("/api/vehicles/search?make=toyota", headers=customer_headers)

        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert results[0]["make"] == "Toyota"

    @pytest.mark.asyncio
    async def test_search_by_category(self, client, customer_headers):
        await client.post(
            "/api/vehicles",
            json={"make": "Ford", "model": "F-150", "category": "Truck", "price": 35000, "quantity": 2},
            headers=customer_headers,
        )
        await client.post(
            "/api/vehicles",
            json={"make": "Honda", "model": "Civic", "category": "Sedan", "price": 21000, "quantity": 3},
            headers=customer_headers,
        )

        response = await client.get("/api/vehicles/search?category=truck", headers=customer_headers)

        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert results[0]["category"] == "Truck"

    @pytest.mark.asyncio
    async def test_search_by_price_range(self, client, customer_headers):
        await client.post(
            "/api/vehicles",
            json={"make": "Honda", "model": "Civic", "category": "Sedan", "price": 21000, "quantity": 3},
            headers=customer_headers,
        )
        await client.post(
            "/api/vehicles",
            json={"make": "Ford", "model": "F-150", "category": "Truck", "price": 35000, "quantity": 2},
            headers=customer_headers,
        )

        response = await client.get(
            "/api/vehicles/search?min_price=25000&max_price=40000", headers=customer_headers
        )

        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert results[0]["make"] == "Ford"

    @pytest.mark.asyncio
    async def test_search_with_no_matches_returns_empty_list(self, client, customer_headers):
        response = await client.get("/api/vehicles/search?make=nonexistent", headers=customer_headers)

        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_search_combines_multiple_filters(self, client, customer_headers):
        await client.post(
            "/api/vehicles",
            json={"make": "Toyota", "model": "Corolla", "category": "Sedan", "price": 22000, "quantity": 5},
            headers=customer_headers,
        )
        await client.post(
            "/api/vehicles",
            json={"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 27000, "quantity": 4},
            headers=customer_headers,
        )

        response = await client.get(
            "/api/vehicles/search?make=toyota&max_price=25000", headers=customer_headers
        )

        assert response.status_code == 200
        results = response.json()
        assert len(results) == 1
        assert results[0]["model"] == "Corolla"