import pandas as pd

def directional_breakout_strategy(df, index_name=None):
    df['PrevHigh'] = df['High'].rolling(window=5).max().shift(1)
    df['PnL'] = 0.0

    for i in range(len(df) - 1):
        if df['Close'].iloc[i] > df['PrevHigh'].iloc[i]:
            entry = df['Close'].iloc[i]
            exit = df['Close'].iloc[i + 1]
            if pd.notnull(entry) and pd.notnull(exit):
                df.at[i, 'PnL'] = float(exit) - float(entry)
                df.at[i, 'Signal'] = 1
                df.at[i, 'Action'] = 'Buy Call'
                df.at[i, 'Call_Strike'] = round(entry + 150, -2)
                df.at[i, 'Put_Strike'] = None

    df = df[df['PnL'] != 0.0].reset_index(drop=True)
    return df
