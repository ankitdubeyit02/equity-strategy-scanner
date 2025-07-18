import pandas as pd
import numpy as np

def generate_intraday_simulation(ltp, ticks=10, volatility=15, trend_bias="neutral"):
    """
    Generate synthetic intraday candles with realistic price evolution.

    Args:
    - ltp (float): Last traded price to seed simulation
    - ticks (int): Number of synthetic candles
    - volatility (float): Standard deviation of price movement per tick
    - trend_bias (str): "bullish", "bearish", or "neutral"
    """

    np.random.seed(42)

    drift_map = {
        "bullish": +5.0,
        "bearish": -5.0,
        "neutral": 0.0
    }
    drift = drift_map.get(trend_bias.lower(), 0.0)

    price = float(ltp)
    candles = []

    for i in range(ticks):
        change = np.random.normal(loc=drift, scale=volatility)
        open_price = price
        close_price = open_price + change
        high_price = max(open_price, close_price) + np.random.uniform(2, 10)
        low_price = min(open_price, close_price) - np.random.uniform(2, 10)
        volume = 1000 + np.random.randint(-300, 300)

        candles.append({
            "Open": round(open_price, 2),
            "High": round(high_price, 2),
            "Low": round(low_price, 2),
            "Close": round(close_price, 2),
            "Volume": volume
        })

        price = close_price  # evolve price for next tick

    df = pd.DataFrame(candles)
    df.index = pd.date_range(start=pd.Timestamp.now(), periods=ticks, freq="5min")

    return df
