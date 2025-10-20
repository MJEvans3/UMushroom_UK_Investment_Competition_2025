# Tactical Diversifier Strategy

## Executive Investment Summary

**Prepared for:** Hedge Fund Managers & Tactical Allocation Teams
**Strategy Type:** Multi-Asset, Event-Driven Tactical Diversifier
**Target Horizon:** 7 Weeks (Oct 20 – Dec 5, 2025)
**Objective:** Positive absolute return with low equity correlation
**Instruments:** Liquid, non-leveraged ETFs (DBMF, GLD/SGLN.L, KMLM, VIXY, UUP, DBC, TLT)
**Risk Profile:** Defensive / Volatility-Responsive

---

## Executive Summary

This tactical allocation sleeve provides an uncorrelated, liquid diversifier to a U.S. equity momentum core. It is structured around **macro event-driven triggers**—not forecasts—executed systematically around scheduled catalysts (CPI, FOMC, NFP, PCE).
The portfolio dynamically adjusts exposures across **managed futures, gold, volatility, dollar, commodities, and bonds** based on data-dependent signals.
Designed for **UK-based implementation**, the plan accounts for time zone shifts, T+1/T+2 settlement, and institutional execution standards.

### Initial Portfolio Allocation (Oct 20, 2025)

| ETF          | Asset Class       | Weight | Rationale                   |
| ------------ | ----------------- | ------ | --------------------------- |
| DBMF         | Managed Futures   | 10%    | Core volatility harvesting  |
| GLD / SGLN.L | Gold (GBP Hedged) | 8%     | Inflation hedge, FX-neutral |
| KMLM         | Systematic Trend  | 7%     | Cross-asset diversification |
| VIXY         | Equity Volatility | 3%     | Tail-risk hedge             |
| Cash         | Cash Reserve      | 7%     | Tactical flexibility        |

**Target Outcome:** Positive return over 7 weeks with ≤0.3 correlation to S&P 500; drawdowns capped below 5%.

---

## Investment Thesis

### Purpose of the Tactical Sleeve

While the core momentum strategy thrives in trending equity markets, this tactical sleeve is designed to **monetize volatility, policy shifts, and macro dislocations**, thereby smoothing equity returns.

### Key Design Principles

* **Trigger-based, not predictive:** All actions tied to data releases or objective thresholds (e.g., CPI >0.4%, DXY <98).
* **High liquidity:** ETFs with AUM >$1B, no leverage or derivatives.
* **Event sequencing:** Structured around CPI (Oct 24, Nov 13), FOMC (Oct 29), and NFP (Nov 7).
* **Execution realism:** Every order aligned with settlement cycles and UK/US daylight saving changes.

---

## Methodology

### Core Instruments and Roles

| Asset        | ETF                      | Role                              |
| ------------ | ------------------------ | --------------------------------- |
| DBMF         | iMGP DBi Managed Futures | Trend/volatility capture          |
| KMLM         | KFA Mount Lucas Index    | Systematic macro diversification  |
| GLD / SGLN.L | Physical Gold            | Inflation & dollar hedge          |
| VIXY         | Short-Term VIX Futures   | Volatility spike monetization     |
| UUP          | US Dollar Index ETF      | USD strength exposure             |
| DBC          | Broad Commodities        | Oil/inflation beta                |
| TLT          | 20+ Year Treasury        | Recession hedge / duration kicker |

### Trigger Framework

Each position is scaled using **quantitative trigger rules**:

| Macro Event | Key Trigger                | Action                              |
| ----------- | -------------------------- | ----------------------------------- |
| CPI         | MoM >0.4% or YoY >3.0%     | Scale GLD & KMLM                    |
| FOMC        | Hawkish dot plot / VIX >30 | Exit VIXY, add UUP                  |
| NFP         | <100k jobs                 | Add TLT, reduce UUP                 |
| Oil         | WTI >$85 for 2 days        | Add DBC                             |
| DXY         | Drop >1% or <98            | Scale GLD                           |
| VIX         | <16 (pre-event)            | Add VIXY for upcoming volatility    |
| VIX         | >30                        | Exit all VIXY positions immediately |

These rules ensure a **mechanical, unemotional** execution cycle driven by macro data rather than discretionary opinion.

---

## Implementation Calendar (Oct–Dec 2025)

### Week 1: Setup (Oct 20–25)

* Establish base positions (DBMF, GLD, KMLM, VIXY)
* Monitor first CPI (Oct 24)
* Execute scaling based on CPI and DXY reaction

### Week 2: FOMC Volatility (Oct 27–31)

* Pre-position for FOMC (Oct 29)
* VIXY profit-taking upon spikes >30%
* PCE inflation data (Oct 31) triggers DBMF/GLD scaling

### Week 3: Trend Realignment (Nov 3–9)

* Recycle VIXY profits into DBMF/KMLM
* NFP triggers (Nov 7) drive defensive or dollar rotation
* Optional DBC entry on oil strength

### Week 4: CPI Volatility (Nov 10–16)

* Rebuild VIXY ahead of Nov 13 CPI
* Execute GLD/KMLM scaling post-CPI based on inflation surprise
* Prepare for portfolio wind-down into final weeks

### Weeks 5–7: Final Consolidation (Nov 17–Dec 5)

* Lock in volatility-driven gains
* Rotate to higher cash/defensive positioning before Dec 5
* No new exposures post-Dec 1

---

## Expected Behavior & Correlation

| Regime            | Equity Correlation | Expected Impact                      |
| ----------------- | ------------------ | ------------------------------------ |
| Equity Uptrend    | 0.2–0.3            | Slightly drag due to defensive bias  |
| Equity Correction | -0.2 to -0.5       | Positive alpha from VIXY, GLD, DBMF  |
| Macro Volatility  | -0.4               | Strongest contribution               |
| Calm Markets      | 0.1                | Small positive carry from trend ETFs |

**Target Return:** 3–5% over 7 weeks
**Target Volatility:** 4–6%
**Expected Sharpe (7-week basis):** 1.2–1.5
**Max Drawdown:** ≤5%

---

## Risk Management

### Structural Controls

* **VIX Hard Stop:** VIX >30 → immediate VIXY exit
* **Cash Reserve:** Maintained between 5–12% for redeployment
* **Event Deadlines:** Orders placed before 8:30 PM GMT for next-day execution
* **Currency Hedging:** GLD replaced by SGLN.L for GBP investors

### Diversification

* Balanced across **trend**, **volatility**, **commodity**, and **inflation** risk premia
* No single ETF >12% allocation post-rebalancing
* Cross-asset triggers prevent overexposure to any single regime

---

## Portfolio Role

**Intended Use:**

* **Diversifier Sleeve (35%)** complementing core 65% equity momentum allocation
* Enhances risk-adjusted returns through crisis convexity
* Preserves capital in volatility clusters and macro shocks

**Liquidity:** All ETFs >$1B AUM, intraday execution possible
**Holding Period:** 7 weeks (Oct 20 – Dec 5, 2025)
**Execution Venue:** UK brokerage (IBKR, Fidelity, or equivalent)

---

## Key Advantages

1. **Event-Driven Discipline:** Trades based only on objective triggers
2. **Crisis Alpha Capture:** VIXY and DBMF monetize volatility surges
3. **Macro Flexibility:** Responds to inflation, Fed policy, and oil dynamics
4. **FX-Neutral Design:** GBP implementation avoids USD conversion drag
5. **Operational Clarity:** Pre-specified execution windows, deadlines, and order templates

---

## Conclusion

The Tactical Diversifier Strategy provides a **transparent, rules-based macro sleeve** engineered for hedge fund managers seeking:

* Low correlation to equities
* Positive convexity in volatile regimes
* Systematic execution through predefined macro triggers
* Institutional realism (time zones, settlement, liquidity)

This 7-week playbook transforms macro volatility into a predictable, repeatable source of alpha—**bridging the gap between systematic discipline and tactical adaptability.**

---

**Document Version:** 1.0 (Condensed Executive Summary)
**Date:** October 2025

---
