from pydantic import BaseModel, Field


class VehicleCreateRequest(BaseModel):
    make: str = Field(min_length=1)
    model: str = Field(min_length=1)
    category: str = Field(min_length=1)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)


class VehicleUpdateRequest(BaseModel):
    make: str = Field(min_length=1)
    model: str = Field(min_length=1)
    category: str = Field(min_length=1)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)


class VehicleResponse(BaseModel):
    id: str
    make: str
    model: str
    category: str
    price: float
    quantity: int

class RestockRequest(BaseModel):
    quantity: int = Field(gt=0)