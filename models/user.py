from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, date
from bson import ObjectId

class User(BaseModel):
    id: ObjectId | None = Field(default=None, alias="_id")
    name: str
    email: EmailStr
    password_hash: str
    monthly_income: float
    occupation: str
    
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }