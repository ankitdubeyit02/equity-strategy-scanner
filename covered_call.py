import pandas as pd

def covered_call_strategy(df, index_name=None):
    df['PnL'] = 0.0

    for i in range(len(df) - 1):
        entry = df['Close'].iloc[i]
        exit = df['Close'].iloc[i + 1]
        if pd.notnull(entry) and pd.notnull(exit):
            premium = 40.0
            cap = round(entry + 100, -2)
            realized = min(exit, cap)
            df.at[i, 'PnL'] = (realized - entry) + premium
            df.at[i, 'Signal'] = 1
            df.at[i, 'Action'] = 'Covered Call'
            df.at[i, 'Call_Strike'] = cap
            df.at[i, 'Put_Strike'] = None

    df = df[df['PnL'] != 0.0].reset_index(drop=True)
    return df
