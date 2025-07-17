import pandas as pd
def straddle_strategy(df, index_name=None):
    df['Signal'] = 1
    df['Action'] = 'Buy Call'
    df['Call_Strike'] = df['Close'].apply(lambda x: round(float(x), -2) if pd.notnull(x) else None)
    df['Put_Strike'] = df['Close'].apply(lambda x: round(float(x), -2) if pd.notnull(x) else None)
    df['PnL'] = 0.0
    for i in range(len(df) - 1):
        entry = float(df['Close'].iloc[i])
        exit = float(df['Close'].iloc[i + 1])
        move = abs(exit - entry)
        df.at[i, 'PnL'] = move - 60
    return df
