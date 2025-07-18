import pandas as pd

def iron_condor_strategy(df, index_name=None):
    df['PnL'] = 0.0

    for i in range(len(df) - 1):
        entry = df['Close'].iloc[i]
        exit = df['Close'].iloc[i + 1]
        if pd.notnull(entry) and pd.notnull(exit):
            upper = round(entry + 300, -2)
            lower = round(entry - 300, -2)
            if lower < exit < upper:
                df.at[i, 'PnL'] = 40.0
            else:
                df.at[i, 'PnL'] = -60.0

            df.at[i, 'Signal'] = 1
            df.at[i, 'Action'] = 'Iron Condor'
            df.at[i, 'Call_Strike'] = upper
            df.at[i, 'Put_Strike'] = lower

    df = df[df['PnL'] != 0.0].reset_index(drop=True)
    return df
