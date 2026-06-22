# backtest_engine.py
import yfinance as yf
import pandas as pd
import numpy as np
import config as cfg
from indicators import calculate_wilders_indicators

print("⏳ กำลังโหลดข้อมูลและคำนวณ Backtest...")
df = yf.download("BTC-USD", start="2020-01-01", end="2026-06-22", auto_adjust=False)
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df = calculate_wilders_indicators(df)

# สถานะพอร์ตเริ่มต้นจาก Config
cash_balance = cfg.INITIAL_CAPITAL
btc_amount = 0.0
we_have_btc = False
cost_basis = 0.0
avg_buy_price = 0.0
highest_price_since_entry = 0.0
current_regime = "MEAN_REVERSION"

equity_curve = []

for date, row in df.iterrows():
    current_price = row['Close']
    current_adx = row['ADX']
    current_rsi = row['RSI']
    current_ema200 = row['EMA_200']
    current_ema20 = row['EMA_20']
    current_atr = row['ATR']
    current_high = row['High']
    
    total_portfolio_value = cash_balance + (btc_amount * current_price)
    equity_curve.append({"Date": date, "Total_Equity": total_portfolio_value, "BTC_Price": current_price})
    
    # ADX Hysteresis
    if current_regime == "MEAN_REVERSION" and current_adx > cfg.ADX_TREND_ON:
        current_regime = "TREND"
    elif current_regime == "TREND" and current_adx < cfg.ADX_TREND_OFF:
        current_regime = "MEAN_REVERSION"
        
    if we_have_btc:
        highest_price_since_entry = max(highest_price_since_entry, current_high, current_price)
        
    # Execution Logic
    if current_regime == "TREND":
        if not we_have_btc:
            is_pullback = (current_rsi < 55) or (current_price < current_ema20)
            if (current_price > current_ema200) and is_pullback and (cash_balance > 0):
                vol_adjusted_size = (total_portfolio_value * cfg.RISK_PER_TRADE) / (current_atr * 3)
                buy_budget = min(vol_adjusted_size * current_price, total_portfolio_value * cfg.MAX_POSITION_CAP)
                buy_budget = min(buy_budget, cash_balance)
                
                if buy_budget > 1:
                    btc_amount = (buy_budget * (1 - cfg.FEE_RATE)) / current_price
                    cash_balance -= buy_budget
                    cost_basis = buy_budget
                    avg_buy_price = current_price
                    highest_price_since_entry = current_price
                    we_have_btc = True
        else:
            atr_stop = highest_price_since_entry - (current_atr * 3.5)
            pct_stop = highest_price_since_entry * 0.88
            final_trailing_stop = max(atr_stop, pct_stop)
            
            if current_price < final_trailing_stop:
                cash_balance += (btc_amount * current_price) * (1 - cfg.FEE_RATE)
                we_have_btc, btc_amount, cost_basis = False, 0.0, 0.0
    else:
        if not we_have_btc:
            if (current_rsi < cfg.RSI_BUY_THRESHOLD) and (cash_balance > 0):
                buy_budget = min(total_portfolio_value * 0.3, cash_balance)
                if buy_budget > 1:
                    btc_amount = (buy_budget * (1 - cfg.FEE_RATE)) / current_price
                    cash_balance -= buy_budget
                    cost_basis = buy_budget
                    avg_buy_price = current_price
                    we_have_btc = True
        else:
            mr_hard_stop = avg_buy_price * (1 - cfg.MR_STOP_LOSS_PCT)
            if current_price < mr_hard_stop or current_rsi > 70:
                cash_balance += (btc_amount * current_price) * (1 - cfg.FEE_RATE)
                we_have_btc, btc_amount, cost_basis = False, 0.0, 0.0

# สรุปผลตัวเลข
perf_df = pd.DataFrame(equity_curve).set_index("Date")
final_value = perf_df['Total_Equity'].iloc[-1]
bot_return = ((final_value - cfg.INITIAL_CAPITAL) / cfg.INITIAL_CAPITAL) * 100
perf_df['Peak'] = perf_df['Total_Equity'].cummax()
max_dd = ((perf_df['Total_Equity'] - perf_df['Peak']) / perf_df['Peak']).min() * 100

print(f"✅ Backtest Finished! Final Equity: {final_value:,.2f} USDT | Return: {bot_return:.2f}% | Max DD: {max_dd:.2f}%")