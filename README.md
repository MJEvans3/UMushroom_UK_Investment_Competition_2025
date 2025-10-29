# Portfolio Strategy - UMushroom UK Investment Competition 2025

**Competition:** £100,000 virtual portfolio | October 10 - December 5, 2025 (8 weeks)
**Strategy:** 65% Systematic Momentum + 35% Tactical Event-Driven
**Target:** Top 3 finish via alpha diversification

---

## Portfolio Allocation

| Strategy | Allocation | Approach | Rebalancing | Folder |
|----------|------------|----------|-------------|--------|
| **Momentum** | **65%** (£65k) | Systematic momentum | Every 4 days | `momentum_strategy/` |
| **Tactical** | **35%** (£35k) | Event-driven discretionary | Daily monitoring | `tactical_strategy/` |

---

## Strategy 1: Systematic Momentum (65%)

**Objective:** Capture intermediate-term price trends in large-cap US equities

**Approach:**
- Regression-based momentum scoring (14-day lookback, R² weighted)
- Top 15 stocks from S&P 500's largest 50 names
- Equal-weight allocation, rebalanced every 4 trading days
- T+2 execution delay modeled

**Expected Performance:**
- **7-Week Return:** 9.3% (median case)
- **Sharpe Ratio:** 3.27
- **Win Rate:** 95% (validated across 21 test periods)
- **Max Drawdown:** 8.0%

**Validation:** 2,772 backtests across 132 parameter combinations

**Implementation:** `python calculate_momentum_signals.py` (run every 4 days)

---

## Strategy 2: Tactical Event-Driven (35%)

**Objective:** Opportunistic alpha from earnings surprises, M&A, and catalyst-driven moves

**Approach:**
- Daily monitoring of earnings calendar, corporate actions, sector rotations
- Discretionary position sizing based on catalyst strength
- Rapid entry/exit on defined events
- Complements momentum with uncorrelated return stream

**Execution:** Daily review of `TACTICAL_STRATEGY.md` for trade ideas

---

## Rationale for Split Allocation

| Factor | Momentum (65%) | Tactical (35%) | Combined Benefit |
|--------|----------------|----------------|------------------|
| **Return Source** | Trend persistence | Event catalysts | Diversified alpha |
| **Correlation** | Market beta 0.7-0.8 | Event-specific | Reduced portfolio vol |
| **Frequency** | 4-day rebalance | Daily opportunities | Consistent activity |
| **Risk Type** | Momentum crash | Idiosyncratic events | Balanced exposure |
| **Skill Edge** | Quant optimization | Event interpretation | Two skill sets |

**Key Advantage:** Momentum provides systematic base returns; tactical captures short-term mispricings momentum can't exploit

---

## Expected Portfolio Performance

**Conservative Case (25th percentile):**
- Momentum: 6% × 65% = 3.9%
- Tactical: 4% × 35% = 1.4%
- **Total: ~5.3%** (£105,300)

**Base Case (median):**
- Momentum: 9% × 65% = 5.9%
- Tactical: 8% × 35% = 2.8%
- **Total: ~8.7%** (£108,700)

**Aggressive Case (75th percentile):**
- Momentum: 12% × 65% = 7.8%
- Tactical: 12% × 35% = 4.2%
- **Total: ~12%** (£112,000)

---

## Risk Management

**Portfolio-Level:**
- Two uncorrelated alpha sources reduce single-strategy risk
- Tactical allocation acts as diversifier during momentum drawdowns
- Combined max drawdown target: <10%

**Momentum-Specific:**
- Equal weighting limits single-stock exposure (6.67%)
- 4-day rebalancing enables rapid exits
- R² filtering reduces false signals

**Tactical-Specific:**
- Position limits prevent overconcentration
- Stop losses on discretionary trades
- Event risk contained to 35% of capital

---

## File Structure

```
CompetitionStrategy/
├── README.md                          # This file (portfolio overview)
│
├── momentum_strategy/
│   ├── calculate_momentum_signals.py  # Signal generator (run every 4 days)
│   ├── seven_week_optimization.py     # Backtesting framework
│   └── MOMENTUM_STRATEGY.md           # Complete technical documentation
│
├── tactical_strategy/
│   └── TACTICAL_STRATEGY.md           # Daily event-driven trade tracker
│
├── STRATEGY_FOR_INVESTORS.md          # Executive summary (6 pages)
└── CLAUDE.md                          # Codebase instructions
```

---

## Daily Workflow

**Every Day:**
1. Review `TACTICAL_STRATEGY.md` for event opportunities
2. Monitor momentum portfolio performance

**Every 4 Trading Days:**
1. Run `python calculate_momentum_signals.py`
2. Execute rebalance orders (sell exits, buy entries)
3. Update position tracking

**Competition Schedule:**
- **Start:** October 10, 2025
- **Momentum Rebalances:** ~8 times total (Oct 17, 23, 29, Nov 4, 10, 14, 20, 26, Dec 2)
- **Tactical Trades:** Ongoing as opportunities arise
- **End:** December 5, 2025

---

## Quick Reference

**For Momentum Strategy Details:** See `MOMENTUM_STRATEGY.md` (652 lines, complete methodology)
**For Investor Pitch:** See `STRATEGY_FOR_INVESTORS.md` (277 lines, executive summary)
**For Tactical Trades:** See `tactical_strategy/TACTICAL_STRATEGY.md` (daily updates)

---

## Competitive Edge

1. **Dual Alpha Sources:** Systematic + discretionary = uncorrelated returns
2. **Rigorous Validation:** 2,772 backtests prevent overfitting
3. **Institutional Execution:** T+2 delays, transaction costs modeled
4. **Risk-Adjusted Focus:** Optimized for Sharpe ratio, not raw returns
5. **Tactical Flexibility:** 35% allocation adapts to market events momentum can't capture

---

**Strategy Status:** Live deployment starting October 17, 2025
**Expected Competition Finish:** Top 3 (target >10% return over 8 weeks)

**Document Version:** 1.0
**Last Updated:** October 2025
