from fastapi import APIRouter, HTTPException
from datetime import datetime
from ..models.auth import RegisterRequest, LoginRequest
from ..utils.auth import get_password_hash, verify_password
from ..utils.mongo import get_database

router = APIRouter(tags=["Auth"])

@router.post("/register")
async def register_user(data: RegisterRequest):
    db = get_database()

    existing = await db.users.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    password_hash = get_password_hash(data.password)

    user_doc = {
        "name": data.name,
        "email": data.email,
        "password_hash": password_hash,
        "monthly_income": data.monthly_income,
        "occupation": data.occupation,
        "created_at": datetime.utcnow()
    }

    result = await db.users.insert_one(user_doc)

    return {
        "user_id": str(result.inserted_id),
        "message": "Registration successful"
    }


@router.post("/login")
async def login_user(data: LoginRequest):
    db = get_database()

    user_doc = await db.users.find_one({"email": data.email})
    if not user_doc:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user_doc["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "user_id": str(user_doc["_id"]),
        "message": "Login successful"
    }
