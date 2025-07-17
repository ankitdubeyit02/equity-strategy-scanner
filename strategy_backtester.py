def backtest_strategy(df, strategy_name, entry_col='Signal', pnl_col='PnL'):
    if pnl_col not in df.columns:
        return {
            'Strategy': strategy_name,
            'Total Trades': 0,
            'Wins': 0,
            'Losses': 0,
            'Net PnL': 0,
            'Avg PnL': 0,
            'Win Rate (%)': 0,
            'ROI': 0
        }

    trades = df[df[entry_col].notnull()]
    total_trades = len(trades)
    wins = trades[trades[pnl_col] > 0].shape[0]
    losses = trades[trades[pnl_col] <= 0].shape[0]
    net_pnl = trades[pnl_col].sum()
    avg_pnl = trades[pnl_col].mean() if total_trades else 0
    win_rate = (wins / total_trades) * 100 if total_trades else 0
    roi = (net_pnl / total_trades) if total_trades else 0

    return {
        'Strategy': strategy_name,
        'Total Trades': total_trades,
        'Wins': wins,
        'Losses': losses,
        'Net PnL': round(net_pnl, 2),
        'Avg PnL': round(avg_pnl, 2),
        'Win Rate (%)': round(win_rate, 2),
        'ROI': round(roi, 2),
    }
