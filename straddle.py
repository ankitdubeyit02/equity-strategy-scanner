import pandas as pd

def straddle_strategy(df, index_name=None):
    df['PnL'] = 0.0

    for i in range(len(df) - 1):
        entry = df['Close'].iloc[i]
        exit = df['Close'].iloc[i + 1]
        if pd.notnull(entry) and pd.notnull(exit):
            move = abs(exit - entry)
            df.at[i, 'PnL'] = move - 40.0
            df.at[i, 'Signal'] = 1
            df.at[i, 'Action'] = 'Straddle'
            strike = round(entry, -2)
            df.at[i, 'Call_Strike'] = strike
            df.at[i, 'Put_Strike'] = strike

    df = df[df['PnL'] != 0.0].reset_index(drop=True)
    return df
