import pandas as pd

def ma_crossover_strategy(df, index_name=None):
    df['MA10'] = df['Close'].rolling(window=10).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['Signal'] = 0
    df.loc[df['MA10'] > df['MA50'], 'Signal'] = 1
    df.loc[df['MA10'] < df['MA50'], 'Signal'] = -1
    df['Action'] = df['Signal'].map({1: 'Buy Call', -1: 'Buy Put', 0: None})
    df['Call_Strike'] = df['Close'].apply(lambda x: round(float(x) + 100, -2) if pd.notnull(x) else None)
    df['Put_Strike'] = df['Close'].apply(lambda x: round(float(x) - 100, -2) if pd.notnull(x) else None)
    df['PnL'] = 0.0
    for i in range(len(df) - 1):
        signal = df['Signal'].iloc[i]
        entry = float(df['Close'].iloc[i])
        exit = float(df['Close'].iloc[i + 1])
        if signal == 1:
            df.at[i, 'PnL'] = exit - entry
        elif signal == -1:
            df.at[i, 'PnL'] = entry - exit
    return df
