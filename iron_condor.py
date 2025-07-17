import pandas as pd

def iron_condor_strategy(df, index_name=None):
    df['Signal'] = 0
    df['Action'] = 'Buy Call'
    df['Call_Strike'] = df['Close'].apply(lambda x: round(float(x) + 150, -2) if pd.notnull(x) else None)
    df['Put_Strike'] = df['Close'].apply(lambda x: round(float(x) - 150, -2) if pd.notnull(x) else None)
    df['PnL'] = 0.0
    for i in range(len(df) - 1):
        mid = float(df['Close'].iloc[i])
        exit = float(df['Close'].iloc[i + 1])
        condor_range = abs(exit - mid)
        df.at[i, 'PnL'] = max(80 - condor_range, -40)
    return df
