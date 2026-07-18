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
