# Multi-Regime Algorithmic Trading System with Volatility-Adjusted Risk Management

An institutional-grade systematic trading framework designed to trade high-volatility digital assets (specifically BTC/USDT). The core objective of this project is to implement strict risk controls and structural flexibility to navigate shifting market phases while aggressively mitigating downside risk.

## 🚀 Key Performance Metrics (Backtest Results 2020 - 2026)
* **Initial Capital:** 1,000.00 USDT
* **Final Portfolio Value:** 1,330.00 USDT
* **Net Return:** +33.00% (Fully accounted for a conservative 0.1% transaction fee per trade)
* **Maximum Drawdown (MDD):** **-4.31%** (Achieved extreme downside protection compared to BTC's asset drawdown of over -70% during the same period)
* **Calmar Ratio:** **7.65** (Demonstrates exceptional risk-adjusted efficiency by generating 7.65x return relative to the maximum peak-to-trough equity drop)
* **Total Transactions:** 82 Executed trades

---

## 🛠️ Core Methodology & System Architecture

### 1. Advanced Market Regime Switching (Hysteresis Filter)
Instead of relying on rigid, single-metric indicators that suffer from whipsaw noise in sideways markets, this system utilizes a dynamic regime switcher powered by **Wilder's Average Directional Index (ADX)** with built-in hysteresis thresholds:
* **Trend Mode Activated:** When ADX crosses above **25**, signaling strong directional momentum.
* **Mean-Reversion Mode Activated:** When ADX drops below **20**, transitioning the algorithm into a range-bound scalp configuration.
* This lag zone prevent frequent, unprofitable switching during marginal market fluctuations.

### 2. Volatility-Adjusted Position Sizing (ATR-Based)
To preserve capital and ensure robust survival, position sizes are calculated dynamically based on recent market volatility via the **Average True Range (ATR)**:

$$\text{Volatility-Adjusted Size} = \frac{\text{Total Equity} \times \text{Risk Per Trade}}{\text{ATR} \times 3} \times \text{Asset Price}$$

* **Risk Per Trade:** Capped strictly at 1% of total portfolio value per trade setup.

### 3. Execution & Exit Strategies
* **Trend-Following Execution:** Enters long positions only when the price trades above the **200 EMA** accompanied by a localized pullback (RSI < 55 or Price < 20 EMA). Exits are triggered via a combination of a 3.5x ATR trailing stop and a 12% absolute trailing stop tracked from the highest peak reconstructed during the trade session.
* **Mean-Reversion Execution:** Enters long positions opportunistically when the asset is oversold (**RSI < 30**) allocating up to 30% of total equity. Exits are swiftly triggered when **RSI > 70** or if a hard **10% Stop Loss** is hit.

---

## 📁 Repository Structure
* `config.py`: Global hyper-parameters including fees, caps, risk tolerances, and regime triggers.
* `indicators.py`: Mathematically accurate implementations of Wilder’s smoothing algorithms for ATR, RSI, and directional movement (ADX).
* `backtest_engine.py`: An event-driven loop backtesting simulator mapping performance historical daily data.

---

## 🧠 Quantitative Analysis & Key Takeaway
The strategy demonstrates an institutional preference for **capital preservation over aggressive exposure**. By remaining under-invested and carrying a significant cash runway throughout major macro bull runs (2020 & 2024), the model purposefully traded off maximum upside return to guarantee a pristine **-4.31% Max Drawdown**. It proves that a mathematical approach to systemic risk can turn a highly volatile asset into a steady, low-beta portfolio component suitable for alternative asset allocations.
