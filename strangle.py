import pandas as pd
def strangle_strategy(df, index_name=None):
    df['Signal'] = 1
    df['Action'] = 'Buy Call'
    df['Call_Strike'] = df['Close'].apply(lambda x: round(float(x) + 200, -2) if pd.notnull(x) else None)
    df['Put_Strike'] = df['Close'].apply(lambda x: round(float(x) - 200, -2) if pd.notnull(x) else None)
    df['PnL'] = 0.0
    for i in range(len(df) - 1):
        entry = float(df['Close'].iloc[i])
        exit = float(df['Close'].iloc[i + 1])
        df.at[i, 'PnL'] = (exit - entry) - 50
    return df
