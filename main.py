from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .utils.mongo import connect_to_mongo, close_mongo_connection
from contextlib import asynccontextmanager
from .routes.auth import router as auth_router
from .routes.expense import router as expense_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()
    
app = FastAPI(title="Fintech Project", description="Fintech backend", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
@app.get("/")
async def healthcheck():
    return {"Fintech backend activated"}

app.include_router(auth_router, prefix="/auth")
app.include_router(expense_router, prefix="/expense")