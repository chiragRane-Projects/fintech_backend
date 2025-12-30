def predict_next_month_expense(history, momentum, volatility):
    weights = [0.5, 0.3, 0.2]
    base = sum(h * w for h, w in zip(history, weights))

    momentum_factor = 1 + max(min(momentum, 0.3), -0.2)
    volatility_penalty = 1 - min(volatility * 0.3, 0.4)

    prediction = base * momentum_factor * volatility_penalty
    return round(prediction, 2)