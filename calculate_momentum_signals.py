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
PORTFOLIO_VALUE = 100000  # £100k
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
    print(f"Portfolio Value: £{PORTFOLIO_VALUE:,.2f}")
    print(f"Momentum Period: {MOMENTUM_PERIOD} days")
    print(f"Stock Universe: Top 50 S&P 500")
    print(f"Selection: Top {int(NUM_TOP_STOCKS * 100)}%")
    print("=" * 80)
    print()

    # Download data for all stocks
    # Need MOMENTUM_PERIOD + buffer for calculation
    end_date = datetime.now()
    start_date = end_date - timedelta(days=MOMENTUM_PERIOD + 10)  # Extra days for weekends

    print(f"Downloading data from {start_date.date()} to {end_date.date()}...")
    print()

    momentum_scores = {}
    current_prices = {}
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
            current_price = prices[-1]

            # Calculate momentum score
            score = calculate_momentum_score(prices)

            if not np.isnan(score):
                momentum_scores[ticker] = score
                current_prices[ticker] = current_price
                print(f"✓ {ticker}: Score = {score:.4f}, Price = ${current_price:.2f}")
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

    # Calculate position sizes
    allocation_per_stock = PORTFOLIO_VALUE / num_to_select

    print(f"MOMENTUM RANKINGS (Top {num_to_select} of {num_stocks} stocks)")
    print("=" * 80)
    print()

    # Show all rankings
    print("Full Rankings:")
    print("-" * 80)
    for rank, (ticker, score) in enumerate(ranked_stocks, 1):
        price = current_prices[ticker]
        selected = ">>> BUY <<<" if rank <= num_to_select else ""
        print(f"{rank:2d}. {ticker:6s} | Score: {score:8.4f} | Price: ${price:8.2f} {selected}")

    print()
    print("=" * 80)
    print(f"BUY ORDERS FOR MARKET OPEN - {(end_date + timedelta(days=1)).strftime('%B %d, %Y')}")
    print("=" * 80)
    print()

    total_allocation = 0

    for rank, (ticker, score) in enumerate(selected_stocks, 1):
        price = current_prices[ticker]
        shares = int(allocation_per_stock / price)
        actual_allocation = shares * price
        weight = (actual_allocation / PORTFOLIO_VALUE) * 100
        total_allocation += actual_allocation

        print(f"{rank}. {ticker}")
        print(f"   Momentum Score: {score:.4f}")
        print(f"   Current Price:  ${price:.2f}")
        print(f"   Target Amount:  £{allocation_per_stock:,.2f}")
        print(f"   Shares to Buy:  {shares:,}")
        print(f"   Actual Cost:    £{actual_allocation:,.2f} ({weight:.1f}%)")
        print()

    print("=" * 80)
    print(f"TOTAL ALLOCATION: £{total_allocation:,.2f} / £{PORTFOLIO_VALUE:,.2f}")
    print(f"CASH REMAINING:   £{PORTFOLIO_VALUE - total_allocation:,.2f}")
    print("=" * 80)
    print()

    # Export to CSV
    output_df = pd.DataFrame({
        'Rank': range(1, len(selected_stocks) + 1),
        'Ticker': [t for t, _ in selected_stocks],
        'Momentum_Score': [s for _, s in selected_stocks],
        'Current_Price': [current_prices[t] for t, _ in selected_stocks],
        'Shares_to_Buy': [int(allocation_per_stock / current_prices[t]) for t, _ in selected_stocks],
        'Allocation': [int(allocation_per_stock / current_prices[t]) * current_prices[t] for t, _ in selected_stocks]
    })

    filename = f"momentum_signals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    output_df.to_csv(filename, index=False)
    print(f"📊 Signals exported to: {filename}")
    print()

    if failed_tickers:
        print("⚠️  Failed tickers:", ", ".join(failed_tickers))

    return selected_stocks, current_prices

if __name__ == "__main__":
    get_current_momentum_signals()
