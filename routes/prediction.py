from fastapi import APIRouter, Query, HTTPException
from ..utils.mongo import get_database
from bson import ObjectId
from datetime import datetime
from ..models.prediction import PredictionResponse
from ..utils.forecaster import predict_next_month_expense
from ..utils.heuristics import confidence_score

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

    # -------------------------------
    # Build expense history (last 3 months)
    # -------------------------------
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

    # -------------------------------
    # Normalize history (CRITICAL FIX)
    # -------------------------------
    while len(history) < 3:
        history.append(0)

    # -------------------------------
    # Momentum (safe)
    # -------------------------------
    if history[1] > 0:
        momentum = (history[0] - history[1]) / history[1]
    else:
        momentum = 0

    # -------------------------------
    # Volatility (safe)
    # -------------------------------
    avg = sum(history) / len(history)
    if avg > 0:
        variance = sum((x - avg) ** 2 for x in history) / len(history)
        volatility = (variance ** 0.5) / avg
    else:
        volatility = 0

    # -------------------------------
    # Prediction
    # -------------------------------
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
