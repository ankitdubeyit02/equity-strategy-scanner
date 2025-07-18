import pandas as pd

def strangle_strategy(df, index_name=None):
    df['PnL'] = 0.0

    for i in range(len(df) - 1):
        entry = df['Close'].iloc[i]
        exit = df['Close'].iloc[i + 1]
        if pd.notnull(entry) and pd.notnull(exit):
            move = abs(exit - entry)
            df.at[i, 'PnL'] = move - 50.0
            df.at[i, 'Signal'] = 1
            df.at[i, 'Action'] = 'Strangle'
            df.at[i, 'Call_Strike'] = round(entry + 200, -2)
            df.at[i, 'Put_Strike'] = round(entry - 200, -2)

    df = df[df['PnL'] != 0.0].reset_index(drop=True)
    return df
