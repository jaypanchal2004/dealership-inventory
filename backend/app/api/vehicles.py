from fastapi import APIRouter, Depends, status

from app.core.deps import get_current_user, require_admin
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreateRequest, VehicleResponse, VehicleUpdateRequest
from app.services.vehicle_service import (
    create_vehicle,
    delete_vehicle,
    list_vehicles,
    search_vehicles,
    update_vehicle,
)

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])


def _to_response(vehicle: Vehicle) -> VehicleResponse:
    return VehicleResponse(
        id=str(vehicle.id),
        make=vehicle.make,
        model=vehicle.model,
        category=vehicle.category,
        price=vehicle.price,
        quantity=vehicle.quantity,
    )


@router.post("", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
async def create(data: VehicleCreateRequest, _=Depends(get_current_user)):
    vehicle = await create_vehicle(data)
    return _to_response(vehicle)

@router.get("/search", response_model=list[VehicleResponse])
async def search(
    make: str | None = None,
    model: str | None = None,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    _=Depends(get_current_user),
):
    vehicles = await search_vehicles(make, model, category, min_price, max_price)
    return [_to_response(v) for v in vehicles]


@router.get("", response_model=list[VehicleResponse])
async def list_all(_=Depends(get_current_user)):
    vehicles = await list_vehicles()
    return [_to_response(v) for v in vehicles]


@router.put("/{vehicle_id}", response_model=VehicleResponse)
async def update(vehicle_id: str, data: VehicleUpdateRequest, _=Depends(get_current_user)):
    vehicle = await update_vehicle(vehicle_id, data)
    return _to_response(vehicle)


@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(vehicle_id: str, _=Depends(require_admin)):
    await delete_vehicle(vehicle_id)
