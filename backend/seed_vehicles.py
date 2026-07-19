"""
Mass-insert sample vehicles into the dealership database.

Run from the backend/ folder (same place you run make_admin.py / uvicorn):

    python seed_vehicles.py

Uses the same settings (Atlas URI + database name) as the real app, via
app.core.config, so it always writes to wherever the app actually reads
from.
"""

import asyncio

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.models.vehicle import Vehicle


SAMPLE_VEHICLES = [
    {"make": "Toyota", "model": "Camry", "category": "Sedan", "price": 28500, "quantity": 5},
    {"make": "Toyota", "model": "Corolla", "category": "Sedan", "price": 22000, "quantity": 8},
    {"make": "Toyota", "model": "RAV4", "category": "SUV", "price": 31500, "quantity": 6},
    {"make": "Honda", "model": "Civic", "category": "Sedan", "price": 24000, "quantity": 7},
    {"make": "Honda", "model": "CR-V", "category": "SUV", "price": 32000, "quantity": 4},
    {"make": "Honda", "model": "Accord", "category": "Sedan", "price": 27500, "quantity": 5},
    {"make": "Ford", "model": "F-150", "category": "Truck", "price": 42000, "quantity": 3},
    {"make": "Ford", "model": "Mustang", "category": "Coupe", "price": 39500, "quantity": 2},
    {"make": "Ford", "model": "Explorer", "category": "SUV", "price": 36000, "quantity": 4},
    {"make": "Chevrolet", "model": "Silverado", "category": "Truck", "price": 41000, "quantity": 3},
    {"make": "Chevrolet", "model": "Malibu", "category": "Sedan", "price": 25500, "quantity": 6},
    {"make": "Chevrolet", "model": "Equinox", "category": "SUV", "price": 29500, "quantity": 5},
    {"make": "Tesla", "model": "Model 3", "category": "Sedan", "price": 41000, "quantity": 3},
    {"make": "Tesla", "model": "Model Y", "category": "SUV", "price": 47000, "quantity": 2},
    {"make": "BMW", "model": "3 Series", "category": "Sedan", "price": 43500, "quantity": 2},
    {"make": "BMW", "model": "X5", "category": "SUV", "price": 61000, "quantity": 1},
    {"make": "Mercedes-Benz", "model": "C-Class", "category": "Sedan", "price": 46000, "quantity": 2},
    {"make": "Hyundai", "model": "Elantra", "category": "Sedan", "price": 21000, "quantity": 9},
    {"make": "Hyundai", "model": "Tucson", "category": "SUV", "price": 27500, "quantity": 5},
    {"make": "Kia", "model": "Sportage", "category": "SUV", "price": 26500, "quantity": 6},
]


async def seed() -> None:
    client = AsyncIOMotorClient(settings.mongodb_uri)
    await init_beanie(database=client[settings.database_name], document_models=[Vehicle])

    inserted = 0
    for data in SAMPLE_VEHICLES:
        vehicle = Vehicle(**data)
        await vehicle.insert()
        inserted += 1
        print(f"Inserted: {vehicle.make} {vehicle.model}")

    print(f"\nDone. Inserted {inserted} vehicles into '{settings.database_name}'.")


if __name__ == "__main__":
    asyncio.run(seed())