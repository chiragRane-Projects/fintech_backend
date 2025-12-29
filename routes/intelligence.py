from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from ..utils.mongo import get_database
from ..utils.aggregation import expense_aggregation, category_aggregation
from ..utils.metrics import calculate_fixed_ratio, calculate_savings_rate, risk_flags
from ..models.intelligence import IntelligenceSummary
from bson import ObjectId

router = APIRouter(tags=["Intelligence"])

@router.get("/summary",response_model=IntelligenceSummary)
async def intelligence_summary(
    user_id: str,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(...)
): 
    db = get_database()
    
    start = datetime(year, month, 1)
    end = (
        datetime(year + 1, 1, 1)
        if month == 12
        else datetime(year, month + 1, 1)
    )
    
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    
    income = user["monthly_income"]
    
    expense_stats = await db.expenses.aggregate(expense_aggregation(user_id, start, end)).to_list(1)
    
    total_expense = expense_stats[0]["total_expense"] if expense_stats else 0
    fixed_expense = expense_stats[0]["fixed_expense"] if expense_stats else 0

    net_balance = income - total_expense
    savings_rate = calculate_savings_rate(income, net_balance)
    fixed_ratio = calculate_fixed_ratio(fixed_expense, total_expense)
    
    categories = await db.expenses.aggregate(category_aggregation(user_id, start, end)).to_list(5)
    
    top_categories = [
        {"category": c["_id"], "amount": c["amount"]}
        for c in categories
    ]
    
    return {
        "income": income,
        "total_expenses": total_expense,
        "net_balance": net_balance,
        "savings_rate": savings_rate,
        "fixed_expense_ratio": fixed_ratio,
        "top_categories": top_categories,
        "risk_flags": risk_flags(income, total_expense, savings_rate)
    }