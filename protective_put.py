import pandas as pd
def protective_put_strategy(df, index_name=None):
    df['Signal'] = -1
    df['Action'] = 'Buy Put'
    df['Call_Strike'] = df['Close'].apply(lambda x: round(float(x) + 100, -2) if pd.notnull(x) else None)
    df['Put_Strike'] = df['Close'].apply(lambda x: round(float(x) - 100, -2) if pd.notnull(x) else None)
    df['PnL'] = 0.0
    for i in range(len(df) - 1):
        entry = float(df['Close'].iloc[i])
        exit = float(df['Close'].iloc[i + 1])
        df.at[i, 'PnL'] = max(entry - exit, -30)
    return df
