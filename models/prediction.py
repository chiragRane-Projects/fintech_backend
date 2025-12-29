from pydantic import BaseModel

class RiskProjection(BaseModel):
    overspending_likely: bool
    savings_decline_likely: bool
    
class PredictionResponse(BaseModel):
    predicted_expense: float
    predicted_net_balance: float
    confidence: float
    risk_projection: RiskProjection