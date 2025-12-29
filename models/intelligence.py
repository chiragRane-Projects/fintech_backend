from pydantic import BaseModel 

class CategorySpend(BaseModel):
    category: str
    amount: float
    
class RiskFlags(BaseModel):
    overspending: bool
    low_savings: bool
    
class IntelligenceSummary(BaseModel):
    income: float
    total_expenses: float
    net_balance: float
    savings_rate: float
    fixed_expense_ratio: float
    top_categories: list[CategorySpend]
    risk_flags: RiskFlags