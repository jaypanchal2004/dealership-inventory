from beanie import Document
from pydantic import Field


class Vehicle(Document):
    """
    Minimal stub for now — deliberately incomplete.

    This exists only so app/core/database.py and the test suite can
    register it with Beanie. The real fields and validation rules get
    added test-first in their own red-green-refactor cycle, not here.
    """

    make: str
    model: str
    category: str
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)

    class Settings:
        name = "vehicles"
