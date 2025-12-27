async def create_indexes(db):
    await db.users.create_index("email", unique=True)
    
    await db.expenses.create_index("user_id")
    await db.expenses.create_index("expense_date")
    await db.expenses.create_index(
        [("user_id", 1), ("expense_date", -1)]
    )

    print("✅ MongoDB indexes created")