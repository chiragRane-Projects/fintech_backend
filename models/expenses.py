from pydantic import BaseModel, Field
from datetime import datetime, date
from bson import ObjectId

class Expense(BaseModel):
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
        json_encoders = {
            ObjectId: str
        }