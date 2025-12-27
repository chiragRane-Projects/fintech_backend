from fastapi import FastAPI
from .utils.mongo import connect_to_mongo, close_mongo_connection
from contextlib import asynccontextmanager
from .routes.auth import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()
    
app = FastAPI(title="Fintech Project", description="Fintech backend", version="1.0.0", lifespan=lifespan)
    
@app.get("/")
async def healthcheck():
    return {"Fintech backend activated"}

app.include_router(auth_router, prefix="/auth")