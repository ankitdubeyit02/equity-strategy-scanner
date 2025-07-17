import pandas as pd

def analyze_strategy_outputs(strategy_outputs, latest_price):
    results = []

    for name, df in strategy_outputs.items():
        try:
            # Ensure required columns exist
            if 'Action' not in df.columns:
                continue

            action = df['Action'].iloc[-1] if 'Action' in df.columns else None

            # Safely extract strike values
            call_strike = df['Call_Strike'].iloc[-1] if 'Call_Strike' in df.columns else None
            put_strike = df['Put_Strike'].iloc[-1] if 'Put_Strike' in df.columns else None

            # Clean NaN values
            call_strike = int(call_strike) if pd.notnull(call_strike) else None
            put_strike = int(put_strike) if pd.notnull(put_strike) else None

            # Decide which strike to use
            suggested_strike = call_strike if action == 'Buy Call' else put_strike

            # Skip if signal is invalid
            if suggested_strike is None or action is None:
                continue

            # 🧠 Assemble signal metadata
            signal_summary = {
                'Strategy': name,
                'Action': action,
                'Suggested Strike': suggested_strike,
                'Index Price': round(latest_price, 2),
            }

            results.append(signal_summary)

        except Exception as e:
            print(f"[Strategy {name}] skipped due to error: {e}")
            continue

    return results
