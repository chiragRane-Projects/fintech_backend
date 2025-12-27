from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime
from ..models.expenses import ExpenseCreate, ExpenseResponse
from ..utils.mongo import get_database
from datetime import datetime, time
from fastapi import Query

router = APIRouter(tags=["Expense"])

@router.post("/add-expense", response_model=ExpenseResponse)
async def add_expense(expense: ExpenseCreate):
    db = get_database()

    expense_doc = {
        "user_id": ObjectId(expense.user_id),
        "amount": expense.amount,
        "category": expense.category,
        "description": expense.description,
        "is_fixed": expense.is_fixed,
        "expense_date": datetime.combine(expense.expense_date, time.min),
        "created_at": datetime.utcnow()
    }

    result = await db.expenses.insert_one(expense_doc)

    return {
        "id": str(result.inserted_id),
        "user_id": expense.user_id,
        "amount": expense.amount,
        "category": expense.category,
        "description": expense.description,
        "is_fixed": expense.is_fixed,
        "expense_date": expense.expense_date,
        "created_at": expense_doc["created_at"]
    }

@router.get("/", response_model=list[ExpenseResponse])
async def get_expenses(
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

    expenses = await db.expenses.find({
        "user_id": ObjectId(user_id),
        "expense_date": {"$gte": start, "$lt": end}
    }).to_list(1000)

    response = []
    for e in expenses:
        response.append({
            "id": str(e["_id"]),
            "user_id": str(e["user_id"]),
            "amount": e["amount"],
            "category": e["category"],
            "description": e.get("description"),
            "is_fixed": e["is_fixed"],
            "expense_date": e["expense_date"].date(),
            "created_at": e["created_at"]
        })

    return response

@router.patch("/edit-expenses/{expense_id}")
async def update_expense(expense_id: str, updates: dict):
    db = get_database()

    if not ObjectId.is_valid(expense_id):
        raise HTTPException(status_code=400, detail="Invalid expense ID")

    updates.pop("_id", None)
    updates.pop("user_id", None)

    if "expense_date" in updates:
        updates["expense_date"] = datetime.combine(
            datetime.fromisoformat(updates["expense_date"]).date(),
            time.min
        )

    result = await db.expenses.update_one(
        {"_id": ObjectId(expense_id)},
        {"$set": updates}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")

    return {"message": "Expense updated"}

@router.delete("/delete-expenses/{expense_id}")
async def delete_expense(expense_id: str):
    db = get_database()

    if not ObjectId.is_valid(expense_id):
        raise HTTPException(status_code=400, detail="Invalid expense ID")

    result = await db.expenses.delete_one({"_id": ObjectId(expense_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")

    return {"message": "Expense deleted"}
