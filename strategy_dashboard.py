import streamlit as st
import pandas as pd
import time
from strategy_runner import run_all_strategies
from strategy_scorer import analyze_strategy_outputs
from nse_live_fetcher import get_bank_nifty_ltp, get_nifty_ltp
from data_loader import get_data

st.set_page_config(layout="wide")
st.title("📈 F&O Strategy Scanner")

# Sidebar controls
st.sidebar.header("Dashboard Settings")
index_option = st.sidebar.radio("Choose Index", ["Nifty", "Bank Nifty"])
refresh_interval = st.sidebar.slider("🔁 Auto-refresh (sec)", 15, 60, 30)

# 🔎 Fetch Live Price
ltp = None
st.sidebar.subheader("Live Price (via NSE)")

if index_option == "Bank Nifty":
    ltp = get_bank_nifty_ltp()
    if ltp:
        st.sidebar.metric("Bank Nifty LTP", f"{ltp:.2f}")
    else:
        st.sidebar.warning("⚠️ Could not fetch Bank Nifty live price")

elif index_option == "Nifty":
    ltp = get_nifty_ltp()
    if ltp:
        st.sidebar.metric("Nifty LTP", f"{ltp:.2f}")
    else:
        st.sidebar.warning("⚠️ Could not fetch Nifty live price")

# 🧮 Load historical data
symbol = "^NSEI" if index_option == "Nifty" else "^NSEBANK"
df = get_data(symbol, start="2023-01-01")

# 🧹 FIX 1: Flatten multi-index column names if any
df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

# ✅ Override last 'Close' with live LTP if available
if ltp:
    df.loc[df.index[-1], 'Close'] = ltp

latest_price = float(df['Close'].iloc[-1])
st.subheader(f"📍 Current Price of {index_option}: {latest_price:.2f}")

# 🧠 Run strategy suite
strategy_outputs = run_all_strategies(df, index_option)
scanned = analyze_strategy_outputs(strategy_outputs, latest_price)
scanned_df = pd.DataFrame(scanned)

# 📌 Signal Table
st.subheader("🧠 Strategy Recommendations")
st.dataframe(scanned_df, use_container_width=True)

from strategy_backtester import backtest_strategy

backtest_reports = []
for name, strat_df in strategy_outputs.items():
    result = backtest_strategy(strat_df, strategy_name=name)
    backtest_reports.append(result)

backtest_df = pd.DataFrame(backtest_reports)
st.subheader("📊 Historical Strategy Performance")
st.dataframe(backtest_df, use_container_width=True)

# ✅ Highlight Top Signals
if not scanned_df.empty and 'Action' in scanned_df.columns:
    buy_calls = scanned_df[scanned_df['Action'] == 'Buy Call']
    buy_puts = scanned_df[scanned_df['Action'] == 'Buy Put']

    if not buy_calls.empty:
        top_call = buy_calls.iloc[0]
        st.success(f"💡 Suggested Call → Strategy: `{top_call['Strategy']}` | Strike: `{top_call['Suggested Strike']}`")

    if not buy_puts.empty:
        top_put = buy_puts.iloc[0]
        st.error(f"💡 Suggested Put → Strategy: `{top_put['Strategy']}` | Strike: `{top_put['Suggested Strike']}`")
else:
    st.info("📭 No actionable signals found — strategy outputs may be incomplete or invalid.")
