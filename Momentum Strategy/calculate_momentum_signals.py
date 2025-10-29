"""
Live Momentum Strategy Signal Generator
Calculates momentum scores for top 50 S&P 500 stocks and generates buy signals
"""

import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import linregress
from datetime import datetime, timedelta

# Strategy parameters (FINAL - Competition-Optimized for 7-8 week periods)
# Tested: 2,772 backtests (132 combos × 21 seven-week periods) Apr-Oct 2025
# Best for 7-week competition: 9.3% avg return, 3.27 Sharpe, 2.44 consistency (Rank #4)
MOMENTUM_PERIOD = 14  # Optimal: 14 days
NUM_TOP_STOCKS = 0.3  # Top 30% (15 stocks) - best risk-adjusted returns
TOTAL_PORTFOLIO = 100000  # £100k total portfolio
TARGET_ALLOCATION = 0.65  # Allocate 65% of portfolio (£65k)
REBALANCE_FREQUENCY = 4  # Rebalance every 4 trading days

# Top 50 S&P 500 stocks by market cap (as of 2024)
TOP_50_SP500 = [
    'NVDA','MSFT','AAPL','GOOG','AMZN','META','AVGO','TSLA','BRK-B','ORCL',
    'WMT','JPM','LLY','V','NFLX','MA','XOM','JNJ','PLTR','COST',
    'ABBV','HD','AMD','BAC','PG','UNH','GE','CVX','KO','CSCO',
    'WFC','IBM','MS','TMUS','CAT','PM','GS','CRM','MU','AXP',
    'ABT','MCD','RTX','MRK','PEP','LIN','APP','TMO','DIS','UBER'
]

def calculate_momentum_score(prices):
    """
    Calculate momentum score using the same formula as the backtest strategy.

    Parameters:
    -----------
    prices : array-like
        Price series for the stock

    Returns:
    --------
    float : momentum score
    """
    if len(prices) < MOMENTUM_PERIOD:
        return np.nan

    # Get log prices
    log_prices = np.log(prices[-MOMENTUM_PERIOD:])

    # Time index
    x = np.arange(len(log_prices))

    # Check for sufficient data
    if len(x) < 2:
        return np.nan

    # Linear regression
    beta, _, rvalue, _, _ = linregress(x, log_prices)

    # Annualize (252 trading days)
    annualized = (1 + beta) ** 252

    # Weight by R-squared
    momentum_score = annualized * (rvalue ** 2)

    return momentum_score

def get_current_momentum_signals():
    """
    Download current market data and calculate momentum signals.
    """
    print("=" * 80)
    print("MOMENTUM STRATEGY SIGNAL GENERATOR")
    print("=" * 80)
    print(f"Total Portfolio: £{TOTAL_PORTFOLIO:,.2f}")
    print(f"Target Allocation: {TARGET_ALLOCATION:.0%} (£{TOTAL_PORTFOLIO * TARGET_ALLOCATION:,.2f})")
    print(f"Momentum Period: {MOMENTUM_PERIOD} days")
    print(f"Stock Universe: Top 50 S&P 500")
    print(f"Selection: Top {int(NUM_TOP_STOCKS * 100)}%")
    print("=" * 80)
    print()

    # Get USD/GBP exchange rate
    print("Fetching USD/GBP exchange rate...")
    try:
        fx = yf.Ticker("GBPUSD=X")
        fx_data = fx.history(period="1d")
        if fx_data.empty:
            raise ValueError("No exchange rate data available")
        gbp_usd_rate = fx_data['Close'].iloc[-1]  # GBP to USD rate
        usd_gbp_rate = 1 / gbp_usd_rate  # USD to GBP rate
        print(f"Exchange Rate: 1 USD = £{usd_gbp_rate:.4f} GBP (1 GBP = ${gbp_usd_rate:.4f} USD)")
        print()
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        print("Using fallback rate of 1 USD = £0.80 GBP")
        usd_gbp_rate = 0.80
        print()

    # Download data for all stocks
    # Need MOMENTUM_PERIOD + buffer for calculation
    end_date = datetime.today()
    start_date = end_date - timedelta(days=MOMENTUM_PERIOD + 10)  # Extra days for weekends

    print(f"Downloading data from {start_date.date()} to {end_date.date()}...")
    print()

    momentum_scores = {}
    current_prices_usd = {}
    current_prices_gbp = {}
    failed_tickers = []

    for ticker in TOP_50_SP500:
        try:
            # Download stock data
            stock = yf.Ticker(ticker)
            df = stock.history(start=start_date, end=end_date)

            if df.empty or len(df) < MOMENTUM_PERIOD:
                print(f"⚠️  {ticker}: Insufficient data (only {len(df)} days)")
                failed_tickers.append(ticker)
                continue

            # Get closing prices
            prices = df['Close'].values
            current_price_usd = prices[-1]
            current_price_gbp = current_price_usd * usd_gbp_rate

            # Calculate momentum score
            score = calculate_momentum_score(prices)

            if not np.isnan(score):
                momentum_scores[ticker] = score
                current_prices_usd[ticker] = current_price_usd
                current_prices_gbp[ticker] = current_price_gbp
                print(f"✓ {ticker}: Score = {score:.4f}, Price = ${current_price_usd:.2f} (£{current_price_gbp:.2f})")
            else:
                print(f"⚠️  {ticker}: Invalid momentum score")
                failed_tickers.append(ticker)

        except Exception as e:
            print(f"✗ {ticker}: Error - {str(e)}")
            failed_tickers.append(ticker)

    print()
    print("=" * 80)

    if not momentum_scores:
        print("ERROR: No valid momentum scores calculated!")
        return

    # Rank stocks by momentum
    ranked_stocks = sorted(momentum_scores.items(), key=lambda x: x[1], reverse=True)

    # Select top N%
    num_stocks = len(ranked_stocks)
    num_to_select = int(np.ceil(num_stocks * NUM_TOP_STOCKS))
    selected_stocks = ranked_stocks[:num_to_select]

    # Calculate position sizes (each stock gets equal weight of the target allocation)
    allocation_per_stock = (TOTAL_PORTFOLIO * TARGET_ALLOCATION) / num_to_select
    weight_per_stock = (TARGET_ALLOCATION / num_to_select) * 100  # As percentage of total portfolio

    print(f"MOMENTUM RANKINGS (Top {num_to_select} of {num_stocks} stocks)")
    print("=" * 80)
    print()

    # Show all rankings
    print("Full Rankings:")
    print("-" * 80)
    for rank, (ticker, score) in enumerate(ranked_stocks, 1):
        price_usd = current_prices_usd[ticker]
        price_gbp = current_prices_gbp[ticker]
        selected = ">>> BUY <<<" if rank <= num_to_select else ""
        print(f"{rank:2d}. {ticker:6s} | Score: {score:8.4f} | Price: ${price_usd:8.2f} (£{price_gbp:6.2f}) {selected}")

    print()
    print("=" * 80)
    print(f"BUY ORDERS FOR MARKET OPEN - {(end_date + timedelta(days=1)).strftime('%B %d, %Y')}")
    print("=" * 80)
    print()

    total_allocation = 0

    import math

    shares_to_buy_list = []
    allocations_list = []

    for rank, (ticker, score) in enumerate(selected_stocks, 1):
        price_usd = current_prices_usd[ticker]
        price_gbp = current_prices_gbp[ticker]
        # Calculate shares based on GBP price (max 2 decimal places, round down)
        shares = math.floor((allocation_per_stock / price_gbp) * 100) / 100
        actual_allocation_gbp = shares * price_gbp  # Actual cost of shares in GBP
        actual_allocation_usd = shares * price_usd  # Actual cost in USD for reference
        weight = (actual_allocation_gbp / TOTAL_PORTFOLIO) * 100  # Weight as % of total portfolio
        total_allocation += actual_allocation_gbp

        shares_to_buy_list.append(shares)
        allocations_list.append(actual_allocation_gbp)

        print(f"{rank}. {ticker}")
        print(f"   Momentum Score: {score:.4f}")
        print(f"   Current Price:  ${price_usd:.2f} (£{price_gbp:.2f})")
        print(f"   Target Amount:  £{allocation_per_stock:,.2f} ({weight_per_stock:.2f}% of portfolio)")
        print(f"   Shares to Buy:  {shares:,.2f}")
        print(f"   Actual Cost:    £{actual_allocation_gbp:,.2f} (${actual_allocation_usd:,.2f}) - {weight:.2f}% of portfolio")
        print()

    print("=" * 80)
    target_amount = TOTAL_PORTFOLIO * TARGET_ALLOCATION
    allocation_pct = (total_allocation / TOTAL_PORTFOLIO) * 100
    print(f"TOTAL ALLOCATION: £{total_allocation:,.2f} / £{target_amount:,.2f} target ({allocation_pct:.2f}% of portfolio)")
    print(f"CASH REMAINING:   £{TOTAL_PORTFOLIO - total_allocation:,.2f} ({(1 - total_allocation/TOTAL_PORTFOLIO)*100:.2f}% of portfolio)")
    print("=" * 80)
    print()

    # Export to CSV
    output_df = pd.DataFrame({
        'Rank': range(1, len(selected_stocks) + 1),
        'Ticker': [t for t, _ in selected_stocks],
        'Momentum_Score': [s for _, s in selected_stocks],
        'Price_USD': [current_prices_usd[t] for t, _ in selected_stocks],
        'Price_GBP': [current_prices_gbp[t] for t, _ in selected_stocks],
        'Shares_to_Buy': shares_to_buy_list,
        'Allocation_GBP': allocations_list,
        'Weight_Pct': [(a / TOTAL_PORTFOLIO) * 100 for a in allocations_list]
    })

    filename = f"momentum_signals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    output_df.to_csv(filename, index=False)
    print(f"📊 Signals exported to: {filename}")
    print()

    if failed_tickers:
        print("⚠️  Failed tickers:", ", ".join(failed_tickers))

    return selected_stocks, current_prices_usd, current_prices_gbp, usd_gbp_rate

if __name__ == "__main__":
    get_current_momentum_signals()
