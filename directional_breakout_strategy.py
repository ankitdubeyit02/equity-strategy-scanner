import pandas as pd

def directional_breakout_strategy(df, index_name=None):
    # 📊 Compute breakout range
    df['Range'] = df['High'].rolling(window=5).max() - df['Low'].rolling(window=5).min()
    df['Breakout'] = df['Close'] > df['High'].rolling(window=5).max().shift(1)

    # 🎯 Generate signal
    df['Signal'] = df['Breakout'].astype(int)
    df['Action'] = df['Signal'].map({1: 'Buy Call', 0: None})

    # 📍 Suggest strike safely with float + null check
    df['Call_Strike'] = df['Close'].apply(lambda x: round(float(x) + 150, -2) if pd.notnull(x) else None)
    df['Put_Strike'] = None  # Not needed for breakout

    # 💹 Simulated PnL
    df['PnL'] = 0.0
    for i in range(len(df) - 1):
        signal = df['Signal'].iloc[i]
        if signal == 1 and pd.notnull(df['Close'].iloc[i]) and pd.notnull(df['Close'].iloc[i + 1]):
            entry = float(df['Close'].iloc[i])
            exit = float(df['Close'].iloc[i + 1])
            df.at[i, 'PnL'] = exit - entry

    return df
