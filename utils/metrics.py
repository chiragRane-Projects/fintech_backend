def calculate_savings_rate(income: float, net_balance: float) -> float:
    if income <= 0:
        return 0.0
    return round((net_balance / income) * 100 , 2)

def calculate_fixed_ratio(fixed: float, total: float) -> float:
    if total <= 0:
        return 0.0
    return round((fixed / total) * 100, 2)

def risk_flags(income: float, total_expense: float, savings_rate: float):
    return {
        "overspending": total_expense > income,
        "low_savings": savings_rate < 20
    }