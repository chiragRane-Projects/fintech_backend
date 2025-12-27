from pydantic import BaseModel, Field
from datetime import datetime, date
from bson import ObjectId

class ExpenseCreate(BaseModel):
    user_id: str                 
    amount: float
    category: str
    description: str | None = None
    is_fixed: bool = False
    expense_date: date

class ExpenseResponse(BaseModel):
    id: str
    user_id: str
    amount: float
    category: str
    description: str | None
    is_fixed: bool
    expense_date: date
    created_at: datetime

class ExpenseDB(BaseModel):
    id: ObjectId | None = Field(default=None, alias="_id")
    user_id: ObjectId
    amount: float
    category: str
    description: str | None = None
    is_fixed: bool = False
    expense_date: date
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
