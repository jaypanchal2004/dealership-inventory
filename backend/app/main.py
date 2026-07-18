from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import auth, vehicles
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Car Dealership Inventory API", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(vehicles.router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
