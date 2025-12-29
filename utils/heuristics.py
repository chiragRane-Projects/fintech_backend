def weighted_average(values: list[float], weights: list[float]) -> float:
    return sum(v * w for v, w in zip(values, weights)) / sum(weights)

def confidence_score(months: int, volatility: float) -> float:
    base = min(months / 6, 1)
    penalty = min(volatility, 0.5)
    return  round(max(base - penalty, 0.1), 2)