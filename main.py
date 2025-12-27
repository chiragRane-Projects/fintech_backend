from fastapi import FastAPI
from .utils.mongo import connect_to_mongo, close_mongo_connection
from contextlib import asynccontextmanager

app = FastAPI(title="Fintech Project", description="Fintech backend", version="1.0.0")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()
    
@app.get("/")
async def healthcheck():
    return {"Fintech backend activated"}