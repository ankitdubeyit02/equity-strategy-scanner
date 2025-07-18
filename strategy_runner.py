import sys
import traceback
from strategies.moving_average import ma_crossover_strategy
from strategies.strangle import strangle_strategy
from strategies.iron_condor import iron_condor_strategy
from strategies.covered_call import covered_call_strategy
from strategies.straddle import straddle_strategy
from strategies.protective_put import protective_put_strategy
from strategies.directional_breakout_strategy import directional_breakout_strategy

def run_all_strategies(df, index_name):
    print(f"\n▶ Running strategy suite on {index_name}...")
    results = {}

    strategy_funcs = {
        'MA_Crossover': ma_crossover_strategy,
        'Strangle': strangle_strategy,
        'Iron_Condor': iron_condor_strategy,
        'Covered_Call': covered_call_strategy,
        'Straddle': straddle_strategy,
        'Protective_Put': protective_put_strategy,
        'Directional_Breakout': directional_breakout_strategy,
    }

    for name, func in strategy_funcs.items():
        try:
            strat_df = func(df.copy(), index_name) if 'index_name' in func.__code__.co_varnames else func(df.copy())
            
            print(f"[{name}] Output shape: {strat_df.shape}")
            print(f"[{name}] Columns: {strat_df.columns.tolist()}")
            print(strat_df.tail(2))

            results[name] = strat_df

        except Exception as e:
            print(f"\n⚠️ [Strategy {name}] failed due to:")
            traceback.print_exc(file=sys.stdout)
            continue

    print("✅ Strategy suite execution complete.\n")
    return results
