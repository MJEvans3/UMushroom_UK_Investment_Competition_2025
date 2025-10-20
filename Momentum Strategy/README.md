# Competition Strategy Files

This folder contains all essential files for the 8-week Investment Portfolio Management Competition (October 10 - December 5, 2025).

## Files Overview

### 📄 FINAL_COMPETITION_STRATEGY.md
**Purpose**: Complete strategy documentation
**Contents**:
- Mathematical methodology (momentum score calculation)
- Parameter optimization process (2,772 backtests across 21 periods)
- Implementation guide and workflow
- Risk management and expected performance
- Competition presentation talking points

**Use this for**: Strategy documentation, explaining your approach to judges, understanding the methodology

---

### 🐍 calculate_momentum_signals.py
**Purpose**: Live signal generator - YOUR MAIN EXECUTION FILE
**When to run**: Every 4 trading days (rebalancing frequency)
**What it does**:
- Downloads current market data for top 50 S&P 500 stocks
- Calculates momentum scores using 14-day lookback
- Selects top 30% (15 stocks) based on momentum
- Generates buy/sell orders with position sizing
- Exports signals to CSV file

**How to run**:
```bash
python calculate_momentum_signals.py
```

**Output**: Creates `momentum_signals_YYYYMMDD_HHMMSS.csv` with your buy orders

---

### 🔬 seven_week_optimization.py
**Purpose**: Parameter testing framework
**What it does**: Tests 132 parameter combinations across 21 seven-week periods (Apr-Oct 2025)
**Why included**: Proves why 14/4/30% parameters were chosen
**Results**: Shows 14-day momentum / 4-day rebalance / 30% selection ranked #4 out of 132 combinations

**Use this for**: Reference, showing your rigorous testing methodology

---

### 📊 seven_week_results_20251017_015939.csv
**Purpose**: Optimization results proving parameter selection
**Contents**: All 132 parameter combinations tested across 21 periods (2,772 total backtests)
**Key finding**: 14/4/30% delivered 9.3% avg 7-week return, 3.27 Sharpe, 2.44 consistency score

**Use this for**: Evidence of robust parameter selection, competition documentation

---

### 📈 momentum_signals_20251017_021017.csv
**Purpose**: Most recent buy signals
**Contents**: Latest momentum rankings and buy recommendations (15 stocks)
**Includes**: Ticker, momentum score, current price, shares to buy, allocation

**Use this for**: Executing your current portfolio positions

---

## Quick Start Guide

### For Daily Operations:
1. Run `calculate_momentum_signals.py` every 4 trading days
2. Review the output showing top 15 stocks to buy
3. Execute buy orders at market open
4. Keep generated CSV files for record-keeping

### For Competition Documentation:
1. Use `FINAL_COMPETITION_STRATEGY.md` as your main reference
2. Reference `seven_week_results_20251017_015939.csv` to show optimization rigor
3. Explain the 2,772 backtests that validated your parameters

---

## Strategy Parameters (Final - Competition Optimized)

- **Momentum Period**: 14 days
- **Rebalance Frequency**: Every 4 trading days
- **Stock Selection**: Top 30% (15 stocks from top 50 S&P 500)
- **Portfolio Value**: £100,000
- **Position Sizing**: Equal weight across selected stocks
- **Execution**: T+2 delay modeled in backtests

---

## Expected Performance (Based on 7-Week Backtests)

- **Average Return**: 9.3% per 7-week period (~54% annualized)
- **Sharpe Ratio**: 3.27 (excellent risk-adjusted returns)
- **Max Drawdown**: 8.0% (moderate downside risk)
- **Consistency Score**: 2.44 (ranked #4 out of 132 combinations)
- **Win Rate**: 85.7% of test periods were profitable

---

## Competition Timeline

- **Start Date**: October 10, 2025
- **End Date**: December 5, 2025
- **Duration**: 8 weeks (56 days)
- **Rebalances**: ~3-4 rebalances during competition period

---

## Notes

- All backtests used T+2 execution delay to model realistic order execution
- Tested on 21 different 7-week periods from April-October 2025 to ensure robustness
- Parameters optimized specifically for 7-8 week holding periods matching competition length
- Strategy avoids overfitting by testing across diverse market conditions
