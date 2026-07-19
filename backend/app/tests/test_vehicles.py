import pytest


class TestCreateVehicle:
    @pytest.mark.asyncio
    async def test_create_vehicle_requires_auth(self, client):
        response = await client.post(
            "/api/vehicles",
            json={
                "make": "Toyota",
                "model": "Corolla",
                "category": "Sedan",
                "price": 22000,
                "quantity": 5,
            },
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_customer_cannot_create_vehicle(self, client, customer_headers):
        response = await client.post(
            "/api/vehicles",
            json={
                "make": "Toyota",
                "model": "Corolla",
                "category": "Sedan",
                "price": 22000,
                "quantity": 5,
            },
            headers=customer_headers,
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_admin_can_create_vehicle(self, client, admin_headers):
        response = await client.post(
            "/api/vehicles",
            json={
                "make": "Toyota",
                "model": "Corolla",
                "category": "Sedan",
                "price": 22000,
                "quantity": 5,
            },
            headers=admin_headers,
        )
        assert response.status_code == 201
        body = response.json()
        assert body["make"] == "Toyota"
        assert body["quantity"] == 5

    @pytest.mark.asyncio
    async def test_create_vehicle_rejects_negative_price(self, client, admin_headers):
        response = await client.post(
            "/api/vehicles",
            json={
                "make": "Toyota",
                "model": "Corolla",
                "category": "Sedan",
                "price": -5000,
                "quantity": 5,
            },
            headers=admin_headers,
        )
        assert response.status_code == 422


class TestListVehicles:
    @pytest.mark.asyncio
    async def test_list_vehicles_returns_all(self, client, admin_headers, customer_headers):
        await client.post(
            "/api/vehicles",
            json={"make": "Honda", "model": "Civic", "category": "Sedan", "price": 21000, "quantity": 3},
            headers=admin_headers,
        )
        await client.post(
            "/api/vehicles",
            json={"make": "Ford", "model": "F-150", "category": "Truck", "price": 35000, "quantity": 2},
            headers=admin_headers,
        )

        response = await client.get("/api/vehicles", headers=customer_headers)

        assert response.status_code == 200
        assert len(response.json()) == 2


class TestUpdateVehicle:
    @pytest.mark.asyncio
    async def test_update_vehicle_changes_fields(self, client, admin_headers):
        create = await client.post(
            "/api/vehicles",
            json={"make": "Honda", "model": "Civic", "category": "Sedan", "price": 21000, "quantity": 3},
            headers=admin_headers,
        )
        vehicle_id = create.json()["id"]

        response = await client.put(
            f"/api/vehicles/{vehicle_id}",
            json={"make": "Honda", "model": "Civic", "category": "Sedan", "price": 19999, "quantity": 3},
            headers=admin_headers,
        )

        assert response.status_code == 200
        assert response.json()["price"] == 19999

    @pytest.mark.asyncio
    async def test_customer_cannot_update_vehicle(self, client, admin_headers, customer_headers):
        create = await client.post(
            "/api/vehicles",
            json={"make": "Honda", "model": "Civic", "category": "Sedan", "price": 21000, "quantity": 3},
            headers=admin_headers,
        )
        vehicle_id = create.json()["id"]

        response = await client.put(
            f"/api/vehicles/{vehicle_id}",
            json={"make": "Honda", "model": "Civic", "category": "Sedan", "price": 19999, "quantity": 3},
            headers=customer_headers,
        )

        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_update_nonexistent_vehicle_returns_404(self, client, admin_headers):
        response = await client.put(
            "/api/vehicles/000000000000000000000000",
            json={"make": "Honda", "model": "Civic", "category": "Sedan", "price": 19999, "quantity": 3},
            headers=admin_headers,
        )
        assert response.status_code == 404


class TestDeleteVehicle:
    @pytest.mark.asyncio
    async def test_customer_cannot_delete_vehicle(self, client, admin_headers, customer_headers):
        create = await client.post(
            "/api/vehicles",
            json={"make": "Honda", "model": "Civic", "category": "Sedan", "price": 21000, "quantity": 3},
            headers=admin_headers,
        )
        vehicle_id = create.json()["id"]

        response = await client.delete(f"/api/vehicles/{vehicle_id}", headers=customer_headers)

        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_admin_can_delete_vehicle(self, client, admin_headers):
        create = await client.post(
            "/api/vehicles",
            json={"make": "Honda", "model": "Civic", "category": "Sedan", "price": 21000, "quantity": 3},
            headers=admin_headers,
        )
        vehicle_id = create.json()["id"]

        response = await client.delete(f"/api/vehicles/{vehicle_id}", headers=admin_headers)

        assert response.status_code == 204

'''test_create_vehicle_with_auth_returns_201 → renamed test_admin_can_create_vehicle, now uses admin_headers
Added test_customer_cannot_create_vehicle (new 403 check)
Every setup call that creates a vehicle (in TestListVehicles, TestUpdateVehicle, TestDeleteVehicle) now uses admin_headers instead of customer_headers, since creation is admin-only now
Added test_customer_cannot_update_vehicle (new 403 check)
test_create_vehicle_rejects_negative_price switched to admin_headers so it's actually testing validation, not accidentally testing the auth layer'''