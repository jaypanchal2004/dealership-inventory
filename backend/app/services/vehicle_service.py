from beanie.operators import Inc
from beanie import PydanticObjectId
from fastapi import HTTPException, status

from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreateRequest, VehicleUpdateRequest


async def create_vehicle(data: VehicleCreateRequest) -> Vehicle:
    vehicle = Vehicle(**data.model_dump())
    await vehicle.insert()
    return vehicle


async def list_vehicles() -> list[Vehicle]:
    return await Vehicle.find_all().to_list()

async def search_vehicles(
    make: str | None = None,
    model: str | None = None,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
) -> list[Vehicle]:
    query: dict = {}

    if make:
        query["make"] = {"$regex": f"^{make}$", "$options": "i"}
    if model:
        query["model"] = {"$regex": f"^{model}$", "$options": "i"}
    if category:
        query["category"] = {"$regex": f"^{category}$", "$options": "i"}
    if min_price is not None or max_price is not None:
        price_filter = {}
        if min_price is not None:
            price_filter["$gte"] = min_price
        if max_price is not None:
            price_filter["$lte"] = max_price
        query["price"] = price_filter

    return await Vehicle.find(query).to_list()


async def get_vehicle_or_404(vehicle_id: str) -> Vehicle:
    try:
        oid = PydanticObjectId(vehicle_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found"
        )

    vehicle = await Vehicle.get(oid)
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found"
        )
    return vehicle


async def update_vehicle(vehicle_id: str, data: VehicleUpdateRequest) -> Vehicle:
    vehicle = await get_vehicle_or_404(vehicle_id)
    for field, value in data.model_dump().items():
        setattr(vehicle, field, value)
    await vehicle.save()
    return vehicle


async def delete_vehicle(vehicle_id: str) -> None:
    vehicle = await get_vehicle_or_404(vehicle_id)
    await vehicle.delete()


async def purchase_vehicle(vehicle_id: str) -> Vehicle:
    vehicle = await get_vehicle_or_404(vehicle_id)
    if vehicle.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle is out of stock",
        )

    # Atomic decrement guarded by quantity > 0 — protects against a race
    # where two concurrent purchases both pass the check above but only
    # one should actually succeed in reducing stock.
    await Vehicle.find_one(Vehicle.id == vehicle.id, Vehicle.quantity > 0).update(
        Inc({Vehicle.quantity: -1})
    )
    return await get_vehicle_or_404(vehicle_id)


async def restock_vehicle(vehicle_id: str, quantity: int) -> Vehicle:
    vehicle = await get_vehicle_or_404(vehicle_id)
    await vehicle.update(Inc({Vehicle.quantity: quantity}))
    return await get_vehicle_or_404(vehicle_id)