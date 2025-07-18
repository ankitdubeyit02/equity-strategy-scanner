import pandas as pd
import numpy as np

def expiry_risk_meter(ltp, strike, recent_highs):
    required_move = strike - ltp
    avg_weekly_move = np.mean(np.diff(recent_highs)) * 5 if len(recent_highs) >= 5 else 400
    move_ratio = required_move / avg_weekly_move

    if move_ratio < 0.5:
        label = "Low Risk – Likely ITM"
        chance = 80
    elif move_ratio < 1.0:
        label = "Medium Risk – Borderline"
        chance = 55
    else:
        label = "High Risk – Unlikely ITM"
        chance = 30

    return chance, label

def analyze_strategy_outputs(strategy_outputs, latest_price):
    scored_rows = []

    for strat_name, df in strategy_outputs.items():
        if df is None or df.empty:
            continue
        print(f"\n🧪 SCORER DEBUG — Strategy: {strat_name}")
        print(f"Returned rows: {len(df)}")
        print(f"Sample PnLs: {df['PnL'].head(3).tolist()}")
        print(f"Actions: {df['Action'].dropna().unique()}")

        # 🧹 Only keep rows where PnL is computed
        valid_df = df[df['PnL'].abs() > 0.0].reset_index(drop=True)
        if valid_df.empty:
            print(f"⚠️ No valid PnL rows for strategy: {strat_name}")   
            continue

        last = valid_df.iloc[-1]
        action = last.get('Action')
        pnl = last.get('PnL')
        call_strike = last.get('Call_Strike')
        put_strike = last.get('Put_Strike')

        if action is None or pd.isna(pnl):
            continue

        # 🎯 Confidence scoring
        confidence = (
            "High" if abs(pnl) >= 50 else
            "Moderate" if abs(pnl) >= 20 else
            "Low"
        )

        # 🧠 Strike fallback logic
        suggested_strike = None
        if pd.notnull(call_strike) and "call" in str(action).lower():
            suggested_strike = call_strike
        elif pd.notnull(put_strike) and "put" in str(action).lower():
            suggested_strike = put_strike
        elif pd.notnull(call_strike):
            suggested_strike = call_strike
        elif pd.notnull(put_strike):
            suggested_strike = put_strike
        else:
            suggested_strike = round(float(latest_price), -2)

        # 📶 Expiry Risk Meter
        try:
            recent_highs = df['High'].tail(10).dropna().values
            itm_chance, risk_label = expiry_risk_meter(float(latest_price), float(suggested_strike), recent_highs)
            expiry_info = f"📶 ITM Potential: {itm_chance}% → {risk_label}"
        except Exception as e:
            print(f"⚠️ Risk meter failed for {strat_name}: {e}")
            expiry_info = ""

        # ✨ Trade message generator
        action_raw = str(action).strip().lower()
        is_valid = action_raw not in ["none", "nan", "null", ""]

        if "buy call" in action_raw:
            signal_msg = f"Buy a Call option at ₹{suggested_strike}"
        elif "buy put" in action_raw:
            signal_msg = f"Buy a Put option at ₹{suggested_strike}"
        elif "straddle" in action_raw:
            signal_msg = f"Buy a Call and Put at ₹{suggested_strike}"
        elif "protective put" in action_raw:
            signal_msg = f"Buy a Put as downside protection at ₹{suggested_strike}"
        elif "covered call" in action_raw:
            signal_msg = f"Sell a Call while holding equity — Strike ₹{suggested_strike}"
        elif "iron condor" in action_raw:
            signal_msg = f"Expect sideways move — Iron Condor near ₹{suggested_strike}"
        elif is_valid:
            signal_msg = f"{action_raw.title()} at ₹{suggested_strike}"
        else:
            signal_msg = f"{strat_name} ➜ Trade suggestion at ₹{suggested_strike}"

        final_message = f"{signal_msg} | PnL: {round(pnl, 2)} | Confidence: {confidence}"
        if expiry_info:
            final_message += f"\n{expiry_info}"

        row = {
            "Strategy": strat_name,
            "Action": action,
            "Suggested Strike": suggested_strike,
            "PnL": round(pnl, 2),
            "Confidence": confidence,
            "Trade_Message": final_message
        }
        scored_rows.append(row)

    scored_rows.sort(key=lambda x: abs(x['PnL']), reverse=True)
    return scored_rows
