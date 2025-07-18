import streamlit as st
import pandas as pd
import time
from strategy_runner import run_all_strategies
from strategy_scorer import analyze_strategy_outputs
from nse_live_fetcher import get_bank_nifty_ltp, get_nifty_ltp
from data_loader import get_data
from synthetic_generator import generate_intraday_simulation
from strategy_backtester import backtest_strategy

st.set_page_config(layout="wide")
st.title("📈 F&O Strategy Scanner")

# 🎛️ Sidebar
st.sidebar.header("Dashboard Settings")
index_option = st.sidebar.radio("Choose Index", ["Nifty", "Bank Nifty"])
refresh_interval = st.sidebar.slider("🔁 Auto-refresh (sec)", 15, 60, 30)

# 🛰️ Fetch Live Price
ltp = None
st.sidebar.subheader("Live Price (via NSE)")
if index_option == "Bank Nifty":
    ltp = get_bank_nifty_ltp()
    if ltp:
        st.sidebar.metric("Bank Nifty LTP", f"{ltp:.2f}")
    else:
        st.sidebar.warning("⚠️ Could not fetch Bank Nifty live price")
else:
    ltp = get_nifty_ltp()
    if ltp:
        st.sidebar.metric("Nifty LTP", f"{ltp:.2f}")
    else:
        st.sidebar.warning("⚠️ Could not fetch Nifty live price")

# 📦 Load historical data
symbol = "^NSEI" if index_option == "Nifty" else "^NSEBANK"
df_hist = get_data(symbol, start="2023-01-01")
df_hist.columns = [col[0] if isinstance(col, tuple) else col for col in df_hist.columns]

# 🔬 Simulate price movement using synthetic candles
if ltp:
    synthetic_df = generate_intraday_simulation(ltp, ticks=10, volatility=25, trend_bias="bearish")
    df = pd.concat([df_hist.tail(50), synthetic_df], ignore_index=False)
    latest_price = float(synthetic_df['Close'].iloc[-1])
    st.subheader(f"📍 Synthetic Price Used: {latest_price:.2f}")
else:
    df = df_hist
    latest_price = float(df['Close'].iloc[-1])
    st.subheader(f"📍 Last Price from History: {latest_price:.2f}")

# 🧠 Run strategies and score results
strategy_outputs = run_all_strategies(df, index_option)
scored_rows = analyze_strategy_outputs(strategy_outputs, latest_price)
scanned_df = pd.DataFrame(scored_rows)

# 🏆 Top Trade Highlight
st.subheader("🏆 Top Trade of the Day")
if not scanned_df.empty:
    best_trade = scanned_df.iloc[0]
    emoji = "✅" if best_trade['Confidence'] == "High" else "⚠️" if best_trade['Confidence'] == "Moderate" else "😴"
    st.success(f"{emoji} **{best_trade['Strategy']}** ➜ {best_trade['Trade_Message']} | PnL: `{best_trade['PnL']}` | Confidence: **{best_trade['Confidence']}**")
else:
    st.info("📭 No actionable trades found — filters may be too tight or market is flat.")

# 🏹 Plain-English Trade Summary Panel
st.subheader("🏹 Clear Trade Suggestions")
if not scanned_df.empty:
    for _, row in scanned_df.head(5).iterrows():  # top 5 signals
        emoji = "✅" if row['Confidence'] == "High" else "⚠️" if row['Confidence'] == "Moderate" else "😴"
        st.markdown(f"{emoji} **{row['Trade_Message']}** | Expected PnL: `{row['PnL']}` | Confidence: **{row['Confidence']}**")
else:
    st.warning("🔍 No valid strategies triggered at current price levels.")

# 📊 Historical Backtest Results
backtest_reports = []
for strat_name, strat_df in strategy_outputs.items():
    result = backtest_strategy(strat_df, strategy_name=strat_name)
    backtest_reports.append(result)

bt_df = pd.DataFrame(backtest_reports)
st.subheader("📊 Historical Strategy Performance")
st.dataframe(bt_df, use_container_width=True)
