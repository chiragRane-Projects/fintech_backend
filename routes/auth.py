from fastapi import APIRouter, HTTPException
from ..models.auth import RegisterRequest, LoginRequest
from ..utils.auth import get_password_hash, verify_password
from ..utils.mongo import get_database

router = APIRouter(tags=['Auth'])

@router.post("/register")
async def register_user(user: RegisterRequest):
    db = get_database()
    
    userExists = await db.users.find_one({"email": user.email})
    
    if userExists:
        raise HTTPException(status_code=400, detail="Email already resgistered")
    
    hash_pwd = get_password_hash(user.password_hash)
    
    user_doc = {
        "name": user.name,
        "email": user.email,
        "password_hash": hash_pwd,
        "monthly_income": user.monthly_income,
        "occupation": user.occupation
    }
    
    result = await db.users.insert_one(user_doc)
    
    return {
        "user_id": str(result.inserted_id),
        "message": "Registration successful"
    }
    
@router.post("/login")
async def login_user(user: LoginRequest):
    db = get_database()
    
    user = await db.users.find_one({"email": user.email})
    
    if not user: 
        raise HTTPException(status_code=400, detail="Invalid email")
    
    if not verify_password(user.password, user['password_hash']):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    return {
        "user_id": str(user["_id"]),
        "message": "Login successful"
    }