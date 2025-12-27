from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    monthly_income: float
    occupation: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
