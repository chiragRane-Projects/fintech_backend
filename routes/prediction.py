from fastapi import APIRouter, Query, HTTPException
from bson import ObjectId
from datetime import datetime
from ..utils.mongo import get_database
from ..utils.forecaster import predict_next_month_expense
from ..utils.heuristics import confidence_score
from ..models.prediction import PredictionResponse

router = APIRouter(tags=["Prediction"])

@router.get("/next-month", response_model=PredictionResponse)
async def predict_next_month(
    user_id: str,
    month: int = Query(..., ge=1, le=12),
    year: int = Query(...)
):
    db = get_database()

    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    income = user["monthly_income"]

    # --------------------------------------------------
    # 🔥 STEP 1: COLD START DETECTION (CRITICAL FIX)
    # --------------------------------------------------
    expenses = await db.expenses.find(
        {"user_id": ObjectId(user_id)}
    ).to_list(1000)

    if not expenses:
        return {
            "predicted_expense": 0,
            "predicted_net_balance": income,
            "confidence": 0.05,
            "risk_projection": {
                "overspending_likely": False,
                "savings_decline_likely": False
            }
        }

    # count unique active days
    active_days = len(
        set(e["expense_date"].date() for e in expenses)
    )

    total_spent = sum(e["amount"] for e in expenses)

    # --------------------------------------------------
    # 🔥 STEP 2: EARLY USER MODE (< 7 days)
    # --------------------------------------------------
    if active_days < 7:
        daily_avg = total_spent / active_days
        ramp_multiplier = min(2 + active_days, 5)
        predicted_expense = daily_avg * ramp_multiplier
        predicted_balance = round(income - predicted_expense, 2)

        return {
            "predicted_expense": predicted_expense,
            "predicted_net_balance": predicted_balance,
            "confidence": 0.1,
            "risk_projection": {
                "overspending_likely": predicted_expense > income,
                "savings_decline_likely": predicted_balance < income * 0.2
            }
        }

    # --------------------------------------------------
    # 🔁 STEP 3: NORMAL MONTHLY MODEL (YOUR ORIGINAL LOGIC)
    # --------------------------------------------------
    history = []

    for i in range(1, 4):
        m = month - i
        y = year
        if m <= 0:
            m += 12
            y -= 1

        start = datetime(y, m, 1)
        end = datetime(y + 1, 1, 1) if m == 12 else datetime(y, m + 1, 1)

        result = await db.expenses.aggregate([
            {
                "$match": {
                    "user_id": ObjectId(user_id),
                    "expense_date": {"$gte": start, "$lt": end}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total": {"$sum": "$amount"}
                }
            }
        ]).to_list(1)

        history.append(result[0]["total"] if result else 0)

    while len(history) < 3:
        history.append(0)

    # momentum
    if history[1] > 0:
        momentum = (history[0] - history[1]) / history[1]
    else:
        momentum = 0

    avg = sum(history) / len(history)
    if avg > 0:
        variance = sum((x - avg) ** 2 for x in history) / len(history)
        volatility = (variance ** 0.5) / avg
    else:
        volatility = 0

    predicted_expense = predict_next_month_expense(
        history,
        momentum,
        volatility
    )

    predicted_balance = round(income - predicted_expense, 2)

    return {
        "predicted_expense": predicted_expense,
        "predicted_net_balance": predicted_balance,
        "confidence": confidence_score(len(history), volatility),
        "risk_projection": {
            "overspending_likely": predicted_expense > income,
            "savings_decline_likely": predicted_balance < income * 0.2
        }
    }