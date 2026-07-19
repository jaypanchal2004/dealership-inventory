import pytest


class TestPurchaseVehicle:
    @pytest.mark.asyncio
    async def test_purchase_requires_auth(self, client):
        response = await client.post("/api/vehicles/000000000000000000000000/purchase")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_purchase_decreases_quantity_by_one(self, client, admin_headers, customer_headers):
        create = await client.post(
            "/api/vehicles",
            json={"make": "Honda", "model": "Civic", "category": "Sedan", "price": 21000, "quantity": 3},
            headers=admin_headers,
        )
        vehicle_id = create.json()["id"]

        response = await client.post(f"/api/vehicles/{vehicle_id}/purchase", headers=customer_headers)

        assert response.status_code == 200
        assert response.json()["quantity"] == 2

    @pytest.mark.asyncio
    async def test_purchase_with_zero_stock_returns_400(self, client, admin_headers, customer_headers):
        create = await client.post(
            "/api/vehicles",
            json={"make": "Honda", "model": "Civic", "category": "Sedan", "price": 21000, "quantity": 0},
            headers=admin_headers,
        )
        vehicle_id = create.json()["id"]

        response = await client.post(f"/api/vehicles/{vehicle_id}/purchase", headers=customer_headers)

        assert response.status_code == 400
        assert "out of stock" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_purchase_nonexistent_vehicle_returns_404(self, client, customer_headers):
        response = await client.post(
            "/api/vehicles/000000000000000000000000/purchase", headers=customer_headers
        )
        assert response.status_code == 404


class TestRestockVehicle:
    @pytest.mark.asyncio
    async def test_customer_cannot_restock(self, client, admin_headers, customer_headers):
        create = await client.post(
            "/api/vehicles",
            json={"make": "Honda", "model": "Civic", "category": "Sedan", "price": 21000, "quantity": 3},
            headers=admin_headers,
        )
        vehicle_id = create.json()["id"]

        response = await client.post(
            f"/api/vehicles/{vehicle_id}/restock",
            json={"quantity": 5},
            headers=customer_headers,
        )

        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_admin_can_restock(self, client, admin_headers):
        create = await client.post(
            "/api/vehicles",
            json={"make": "Honda", "model": "Civic", "category": "Sedan", "price": 21000, "quantity": 3},
            headers=admin_headers,
        )
        vehicle_id = create.json()["id"]

        response = await client.post(
            f"/api/vehicles/{vehicle_id}/restock",
            json={"quantity": 5},
            headers=admin_headers,
        )

        assert response.status_code == 200
        assert response.json()["quantity"] == 8

    @pytest.mark.asyncio
    async def test_restock_with_negative_quantity_returns_422(self, client, admin_headers):
        create = await client.post(
            "/api/vehicles",
            json={"make": "Honda", "model": "Civic", "category": "Sedan", "price": 21000, "quantity": 3},
            headers=admin_headers,
        )
        vehicle_id = create.json()["id"]

        response = await client.post(
            f"/api/vehicles/{vehicle_id}/restock",
            json={"quantity": -2},
            headers=admin_headers,
        )

        assert response.status_code == 422