import pandas as pd

def backtest_strategy(df, strategy_name=""):
    if df is None or df.empty or 'PnL' not in df.columns:
        return {
            "Strategy": strategy_name,
            "Total Trades": 0,
            "Wins": 0,
            "Losses": 0,
            "Net PnL": 0.0,
            "Avg PnL": 0.0,
            "Win Rate (%)": 0.0
        }

    # Filter out zero or missing signals
    df = df[df['Signal'] != 0].copy()
    df = df[pd.notnull(df['PnL'])]

    total = len(df)
    wins = len(df[df['PnL'] > 0])
    losses = len(df[df['PnL'] <= 0])
    net_pnl = df['PnL'].sum()
    avg_pnl = df['PnL'].mean() if total > 0 else 0.0
    win_rate = (wins / total * 100) if total > 0 else 0.0

    return {
        "Strategy": strategy_name,
        "Total Trades": total,
        "Wins": wins,
        "Losses": losses,
        "Net PnL": round(net_pnl, 2),
        "Avg PnL": round(avg_pnl, 2),
        "Win Rate (%)": round(win_rate, 2)
    }
