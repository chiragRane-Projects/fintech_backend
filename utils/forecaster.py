def predict_next_month_expense(
    last_months: list[float],
    momentum: float,
    volatility: float
) -> float:
    weights = [0.5, 0.3, 0.2][:len(last_months)]
    base = sum(m * w for m,w in zip(last_months, weights))
    
    trend_adjustment = base * momentum
    noise_penalty = base * volatility * 0.3
    
    prediction = base + trend_adjustment - noise_penalty
    return round(max(prediction, 0), 2)