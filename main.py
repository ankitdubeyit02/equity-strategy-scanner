from data_loader import get_data
from strategy_runner import run_all_strategies
from utils.plotter import plot_signals

# 🗂️ Load live historical data
nifty_data = get_data("^NSEI", start="2023-01-01")
bn_data = get_data("^NSEBANK", start="2023-01-01")

# ⚙️ Run all strategies
nifty_strategies = run_all_strategies(nifty_data, "Nifty")
banknifty_strategies = run_all_strategies(bn_data, "Bank Nifty")

# 📊 Plot selected signals
plot_signals(nifty_strategies['MA_Crossover'], "Nifty - MA Crossover")
plot_signals(nifty_strategies['Directional_Breakout'], "Nifty - Directional Breakout")
plot_signals(nifty_strategies['Straddle'], "Nifty - Straddle Strategy")

plot_signals(banknifty_strategies['MA_Crossover'], "Bank Nifty - MA Crossover")
plot_signals(banknifty_strategies['Directional_Breakout'], "Bank Nifty - Directional Breakout")
plot_signals(banknifty_strategies['Straddle'], "Bank Nifty - Straddle Strategy")

# ✨ You can add more plots like:
# plot_signals(nifty_strategies['Iron_Condor'], "Nifty - Iron Condor")
# plot_signals(banknifty_strategies['Covered_Call'], "Bank Nifty - Covered Call")
