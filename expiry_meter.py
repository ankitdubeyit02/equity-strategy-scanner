import numpy as np

def expiry_risk_meter(ltp, strike, recent_highs):
    required_move = strike - ltp
    avg_weekly_move = np.mean(np.diff(recent_highs)) * 5 if len(recent_highs) >= 5 else 400
    move_ratio = required_move / avg_weekly_move

    if move_ratio < 0.5:
        label = "Low Risk – Likely ITM"
        chance = 80
    elif move_ratio < 1.0:
        label = "Medium Risk – Borderline"
        chance = 55
    else:
        label = "High Risk – Unlikely ITM"
        chance = 30

    return chance, label
