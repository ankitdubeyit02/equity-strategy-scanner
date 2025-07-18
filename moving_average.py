import pandas as pd

def ma_crossover_strategy(df, index_name=None):
    df['MA_5'] = df['Close'].rolling(window=5).mean()
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['PnL'] = 0.0

    for i in range(len(df) - 1):
        if df['MA_5'].iloc[i] > df['MA_20'].iloc[i]:
            entry = df['Close'].iloc[i]
            exit = df['Close'].iloc[i + 1]
            if pd.notnull(entry) and pd.notnull(exit):
                df.at[i, 'PnL'] = float(exit) - float(entry)
                df.at[i, 'Signal'] = 1
                df.at[i, 'Action'] = 'Buy Call'
                df.at[i, 'Call_Strike'] = round(entry + 100, -2)
                df.at[i, 'Put_Strike'] = None

    df = df[df['PnL'] != 0.0].reset_index(drop=True)
    return df
