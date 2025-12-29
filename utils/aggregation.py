from bson import ObjectId
from datetime import datetime

def expense_aggregation(user_id: str, start: datetime, end: datetime):
    return[
        {
            "$match": {
                "user_id": ObjectId(user_id),
                "expense_date": {"$gte": start, "$lt": end}
            }
        },
        {
            "$group": {
                "_id": None,
                "total_expense": {"$sum": "$amount"},
                "fixed_expense": {
                    "$sum": {
                        "$cond": [{"$eq": ["$is_fixed", True]}, "$amount", 0]
                    }
            }
        }
        }
    ]
    
def category_aggregation(user_id: str, start: datetime, end: datetime):
    return [
        {
            "$match": {
                "user_id": ObjectId(user_id),
                "expense_date": {"$gte": start, "$lt": end}
            }
        },
        {
            "$group": {
                "_id": "$category",
                "amount": {"$sum": "$amount"}
            }
        },
        {"$sort": {"amount": -1}},
        {"$limit": 5}
    ]