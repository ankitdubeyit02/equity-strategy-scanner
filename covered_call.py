import pandas as pd

def covered_call_strategy(df, index_name=None):
    df['Signal'] = 1
    df['Action'] = 'Buy Call'
    df['Call_Strike'] = df['Close'].apply(lambda x: round(float(x) + 150, -2) if pd.notnull(x) else None)
    df['Put_Strike'] = None
    df['PnL'] = 0.0
    for i in range(len(df) - 1):
        entry = float(df['Close'].iloc[i])
        exit = float(df['Close'].iloc[i + 1])
        df.at[i, 'PnL'] = min(exit - entry, 100)
    return df
