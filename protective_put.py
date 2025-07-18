import pandas as pd

def protective_put_strategy(df, index_name=None):
    df['PnL'] = 0.0

    for i in range(len(df) - 1):
        entry = df['Close'].iloc[i]
        exit = df['Close'].iloc[i + 1]
        if pd.notnull(entry) and pd.notnull(exit):
            protection = 50.0
            downside = float(entry) - float(exit)
            df.at[i, 'PnL'] = -protection + max(downside, 0)
            df.at[i, 'Signal'] = 1
            df.at[i, 'Action'] = 'Protective Put'
            df.at[i, 'Put_Strike'] = round(entry - 150, -2)
            df.at[i, 'Call_Strike'] = None

    df = df[df['PnL'] != 0.0].reset_index(drop=True)
    return df
