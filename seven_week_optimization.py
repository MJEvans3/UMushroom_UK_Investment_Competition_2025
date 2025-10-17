"""
7-Week Period Parameter Optimization
Tests parameters across ONLY 7-week periods (closest to competition 8 weeks)

Competition: Oct 10, 2025 - Dec 5, 2025 (8 weeks / 56 days)
Testing: Multiple 7-week windows (49 days) from Apr 8 - Oct 16, 2025
"""

import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import linregress
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Top 50 S&P 500 stocks
TOP_50_SP500 = [
    'NVDA','MSFT','AAPL','GOOG','AMZN','META','AVGO','TSLA','BRK-B','ORCL',
    'WMT','JPM','LLY','V','NFLX','MA','XOM','JNJ','PLTR','COST',
    'ABBV','HD','AMD','BAC','PG','UNH','GE','CVX','KO','CSCO',
    'WFC','IBM','MS','TMUS','CAT','PM','GS','CRM','MU','AXP',
    'ABT','MCD','RTX','MRK','PEP','LIN','APP','TMO','DIS','UBER'
]

# Parameter combinations to test
MOMENTUM_PERIODS = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
REBALANCE_DAYS = [2, 3, 4, 5]
TOP_STOCK_PERCENTAGES = [0.1, 0.2, 0.3]

# Initial capital
INITIAL_CAPITAL = 100000

# Test periods - ONLY 7-week windows (49 days / ~35 trading days)
TEST_PERIODS_7WEEKS = [
    ('2025-04-08', '2025-05-27', '7wk: Apr 8 - May 27'),
    ('2025-04-14', '2025-06-02', '7wk: Apr 14 - Jun 2'),
    ('2025-04-21', '2025-06-09', '7wk: Apr 21 - Jun 9'),
    ('2025-04-28', '2025-06-16', '7wk: Apr 28 - Jun 16'),
    ('2025-05-05', '2025-06-23', '7wk: May 5 - Jun 23'),
    ('2025-05-12', '2025-06-30', '7wk: May 12 - Jun 30'),
    ('2025-05-19', '2025-07-07', '7wk: May 19 - Jul 7'),
    ('2025-05-26', '2025-07-14', '7wk: May 26 - Jul 14'),
    ('2025-06-02', '2025-07-21', '7wk: Jun 2 - Jul 21'),
    ('2025-06-09', '2025-07-28', '7wk: Jun 9 - Jul 28'),
    ('2025-06-16', '2025-08-04', '7wk: Jun 16 - Aug 4'),
    ('2025-06-23', '2025-08-11', '7wk: Jun 23 - Aug 11'),
    ('2025-06-30', '2025-08-18', '7wk: Jun 30 - Aug 18'),
    ('2025-07-07', '2025-08-25', '7wk: Jul 7 - Aug 25'),
    ('2025-07-14', '2025-09-01', '7wk: Jul 14 - Sep 1'),
    ('2025-07-21', '2025-09-08', '7wk: Jul 21 - Sep 8'),
    ('2025-07-28', '2025-09-15', '7wk: Jul 28 - Sep 15'),
    ('2025-08-04', '2025-09-22', '7wk: Aug 4 - Sep 22'),
    ('2025-08-11', '2025-09-29', '7wk: Aug 11 - Sep 29'),
    ('2025-08-18', '2025-10-06', '7wk: Aug 18 - Oct 6'),
    ('2025-08-25', '2025-10-13', '7wk: Aug 25 - Oct 13'),
]


def calculate_momentum_score(log_prices):
    """Calculate momentum score using linear regression on log prices."""
    if len(log_prices) < 2:
        return np.nan

    x = np.arange(len(log_prices))

    try:
        beta, _, rvalue, _, _ = linregress(x, log_prices)
        annualized = (1 + beta) ** 252
        momentum_score = annualized * (rvalue ** 2)
        return momentum_score
    except:
        return np.nan


class MomentumBacktester:
    """Backtester with 2-day order execution delay."""

    def __init__(self, momentum_period, rebalance_days, num_top_stocks,
                 price_data, initial_capital=100000):
        self.momentum_period = momentum_period
        self.rebalance_days = rebalance_days
        self.num_top_stocks = num_top_stocks
        self.price_data = price_data
        self.initial_capital = initial_capital

        self.portfolio_value = []
        self.dates = []
        self.holdings = {}
        self.cash = initial_capital
        self.pending_orders = []

    def run(self):
        """Run the backtest."""
        dates = self.price_data.index
        day_counter = 0

        for i, date in enumerate(dates):
            self._execute_pending_orders(date)

            portfolio_val = self._calculate_portfolio_value(date)
            self.portfolio_value.append(portfolio_val)
            self.dates.append(date)

            if day_counter % self.rebalance_days == 0 and i >= self.momentum_period:
                self._generate_rebalance_orders(date, i)

            day_counter += 1

        return self._calculate_metrics()

    def _calculate_portfolio_value(self, date):
        """Calculate total portfolio value."""
        stock_value = 0
        for ticker, shares in self.holdings.items():
            if ticker in self.price_data.columns:
                price = self.price_data.loc[date, ticker]
                if not np.isnan(price):
                    stock_value += shares * price
        return self.cash + stock_value

    def _generate_rebalance_orders(self, current_date, current_idx):
        """Generate rebalancing orders based on momentum scores."""
        momentum_scores = {}

        for ticker in self.price_data.columns:
            prices = self.price_data[ticker].iloc[max(0, current_idx - self.momentum_period + 1):current_idx + 1]

            if len(prices) == self.momentum_period and not prices.isna().any():
                log_prices = np.log(prices.values)
                score = calculate_momentum_score(log_prices)
                if not np.isnan(score):
                    momentum_scores[ticker] = score

        if not momentum_scores:
            return

        ranked = sorted(momentum_scores.items(), key=lambda x: x[1], reverse=True)
        num_to_select = int(np.ceil(len(ranked) * self.num_top_stocks))
        top_tickers = [ticker for ticker, _ in ranked[:num_to_select]]

        execution_idx = current_idx + 2
        if execution_idx >= len(self.price_data):
            return

        execution_date = self.price_data.index[execution_idx]

        target_value_per_stock = self.initial_capital / num_to_select

        orders = {}

        for ticker in self.price_data.columns:
            execution_price = self.price_data.loc[execution_date, ticker]

            if np.isnan(execution_price):
                continue

            if ticker in top_tickers:
                target_shares = int(target_value_per_stock / execution_price)
                orders[ticker] = target_shares
            else:
                orders[ticker] = 0

        self.pending_orders.append((execution_date, orders))

    def _execute_pending_orders(self, current_date):
        """Execute orders scheduled for current_date."""
        executed = []

        for i, (execution_date, orders) in enumerate(self.pending_orders):
            if execution_date == current_date:
                # Sell positions first
                for ticker, target_shares in orders.items():
                    current_shares = self.holdings.get(ticker, 0)

                    if target_shares < current_shares:
                        shares_to_sell = current_shares - target_shares
                        price = self.price_data.loc[current_date, ticker]
                        if not np.isnan(price):
                            self.cash += shares_to_sell * price
                            self.holdings[ticker] = target_shares
                            if target_shares == 0:
                                del self.holdings[ticker]

                # Buy positions second
                for ticker, target_shares in orders.items():
                    current_shares = self.holdings.get(ticker, 0)

                    if target_shares > current_shares:
                        shares_to_buy = target_shares - current_shares
                        price = self.price_data.loc[current_date, ticker]
                        if not np.isnan(price):
                            cost = shares_to_buy * price
                            if cost <= self.cash:
                                self.cash -= cost
                                self.holdings[ticker] = target_shares

                executed.append(i)

        for i in reversed(executed):
            self.pending_orders.pop(i)

    def _calculate_metrics(self):
        """Calculate performance metrics."""
        if len(self.portfolio_value) < 2:
            return {
                'total_return': 0,
                'annualized_return': 0,
                'sharpe_ratio': 0,
                'max_drawdown': 0,
                'final_value': self.initial_capital
            }

        final_value = self.portfolio_value[-1]
        total_return = ((final_value - self.initial_capital) / self.initial_capital) * 100

        portfolio_series = pd.Series(self.portfolio_value, index=self.dates)
        daily_returns = portfolio_series.pct_change().dropna()

        num_days = len(self.portfolio_value)
        annualized_return = ((final_value / self.initial_capital) ** (252 / num_days) - 1) * 100

        if len(daily_returns) > 0 and daily_returns.std() > 0:
            sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * np.sqrt(252)
        else:
            sharpe_ratio = 0

        peak = portfolio_series.expanding().max()
        drawdown = (portfolio_series - peak) / peak
        max_drawdown = drawdown.min() * 100

        return {
            'total_return': total_return,
            'annualized_return': annualized_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': abs(max_drawdown),
            'final_value': final_value
        }


def download_data(tickers, start_date, end_date):
    """Download price data for all tickers."""
    buffer_start = (pd.to_datetime(start_date) - timedelta(days=30)).strftime('%Y-%m-%d')

    all_data = []
    failed = []

    for ticker in tickers:
        try:
            df = yf.download(ticker, start=buffer_start, end=end_date, progress=False)
            if not df.empty and len(df) > 0:
                close_series = df['Close'].copy()
                close_series.name = ticker
                all_data.append(close_series)
            else:
                failed.append(ticker)
        except Exception as e:
            failed.append(ticker)

    if not all_data:
        raise ValueError("No data downloaded for any ticker!")

    price_df = pd.concat(all_data, axis=1)
    price_df = price_df.dropna(how='all')

    return price_df, failed


def run_seven_week_optimization():
    """Test parameters across only 7-week periods."""

    print("=" * 120)
    print("7-WEEK PERIOD PARAMETER OPTIMIZATION")
    print("Testing Only 7-Week Periods (49 days / ~35 trading days)")
    print("=" * 120)
    print()
    print(f"Competition: 8 weeks (Oct 10 - Dec 5, 2025)")
    print(f"Test Windows: Only 7-week periods (closest match to competition)")
    print(f"Total Test Periods: {len(TEST_PERIODS_7WEEKS)}")
    print(f"Parameter Combinations: {len(MOMENTUM_PERIODS) * len(REBALANCE_DAYS) * len(TOP_STOCK_PERCENTAGES)}")
    print()

    # Download all data once
    earliest_start = min([start for start, _, _ in TEST_PERIODS_7WEEKS])
    latest_end = '2025-10-16'

    print(f"Downloading data from {earliest_start} to {latest_end}...")
    print()

    full_price_data, failed = download_data(TOP_50_SP500, earliest_start, latest_end)

    if failed:
        print(f"Failed tickers: {', '.join(failed)}")
        print()

    print(f"Successfully downloaded {len(full_price_data.columns)} tickers")
    print(f"Date range: {full_price_data.index[0].date()} to {full_price_data.index[-1].date()}")
    print()

    all_results = []

    total_tests = len(MOMENTUM_PERIODS) * len(REBALANCE_DAYS) * len(TOP_STOCK_PERCENTAGES)
    test_count = 0

    for momentum_period in MOMENTUM_PERIODS:
        for rebalance_days in REBALANCE_DAYS:
            for top_pct in TOP_STOCK_PERCENTAGES:
                test_count += 1

                period_results = []

                for start_date, end_date, period_name in TEST_PERIODS_7WEEKS:
                    try:
                        if pd.to_datetime(end_date) > full_price_data.index[-1]:
                            continue

                        buffer_start = (pd.to_datetime(start_date) - timedelta(days=30)).strftime('%Y-%m-%d')
                        data_mask = (full_price_data.index >= buffer_start) & (full_price_data.index <= end_date)
                        period_data = full_price_data[data_mask]

                        if len(period_data) < momentum_period + 5:
                            continue

                        backtester = MomentumBacktester(
                            momentum_period=momentum_period,
                            rebalance_days=rebalance_days,
                            num_top_stocks=top_pct,
                            price_data=period_data,
                            initial_capital=INITIAL_CAPITAL
                        )

                        metrics = backtester.run()

                        period_results.append({
                            'period': period_name,
                            'start': start_date,
                            'end': end_date,
                            'annualized_return': metrics['annualized_return'],
                            'sharpe_ratio': metrics['sharpe_ratio'],
                            'max_drawdown': metrics['max_drawdown'],
                            'total_return': metrics['total_return']
                        })

                    except Exception as e:
                        continue

                if len(period_results) > 0:
                    returns = [r['annualized_return'] for r in period_results]
                    sharpes = [r['sharpe_ratio'] for r in period_results]
                    drawdowns = [r['max_drawdown'] for r in period_results]
                    total_returns = [r['total_return'] for r in period_results]

                    all_results.append({
                        'momentum_period': momentum_period,
                        'rebalance_days': rebalance_days,
                        'top_pct': top_pct,
                        'num_stocks': int(np.ceil(len(full_price_data.columns) * top_pct)),
                        'num_periods_tested': len(period_results),
                        'avg_return': np.mean(returns),
                        'std_return': np.std(returns),
                        'min_return': np.min(returns),
                        'max_return': np.max(returns),
                        'avg_7wk_return': np.mean(total_returns),
                        'avg_sharpe': np.mean(sharpes),
                        'std_sharpe': np.std(sharpes),
                        'min_sharpe': np.min(sharpes),
                        'max_sharpe': np.max(sharpes),
                        'avg_drawdown': np.mean(drawdowns),
                        'max_drawdown': np.max(drawdowns),
                        'consistency_score': np.mean(sharpes) - np.std(sharpes)
                    })

                if test_count % 10 == 0:
                    print(f"Completed {test_count}/{total_tests} parameter combinations...")

    print()
    print("=" * 120)
    print("RESULTS - Sorted by Consistency Score")
    print("=" * 120)
    print()

    results_df = pd.DataFrame(all_results)
    results_df_sorted = results_df.sort_values('consistency_score', ascending=False)

    print(f"{'Rank':<6}{'Mom':<6}{'Reb':<6}{'Top%':<8}{'#Stk':<6}{'Tests':<7}"
          f"{'Avg 7wk Ret':<13}{'Avg Ann Ret':<13}{'Avg Sharpe':<12}{'Consistency':<12}")
    print("-" * 120)

    for idx, row in results_df_sorted.head(20).iterrows():
        print(f"{results_df_sorted.index.get_loc(idx)+1:<6}"
              f"{row['momentum_period']:<6.0f}"
              f"{row['rebalance_days']:<6.0f}"
              f"{row['top_pct']:<8.1%}"
              f"{row['num_stocks']:<6.0f}"
              f"{row['num_periods_tested']:<7.0f}"
              f"{row['avg_7wk_return']:>11.1f}%"
              f"{row['avg_return']:>12.1f}%"
              f"{row['avg_sharpe']:>11.2f}"
              f"{row['consistency_score']:>11.2f}")

    print()
    print("=" * 120)
    print("FOCUS: TOP 3 CANDIDATE STRATEGIES")
    print("=" * 120)
    print()

    # Find our three specific strategies
    option_new = results_df[(results_df['momentum_period'] == 14) &
                            (results_df['rebalance_days'] == 4) &
                            (results_df['top_pct'] == 0.3)]

    option1 = results_df[(results_df['momentum_period'] == 14) &
                         (results_df['rebalance_days'] == 4) &
                         (results_df['top_pct'] == 0.2)]

    option2 = results_df[(results_df['momentum_period'] == 12) &
                         (results_df['rebalance_days'] == 3) &
                         (results_df['top_pct'] == 0.3)]

    strategies = []

    if not option_new.empty:
        row = option_new.iloc[0]
        rank = results_df_sorted.index.get_loc(option_new.index[0]) + 1
        print(f"NEW OPTION: 14 days / 4 days / 30% (15 stocks) - RANK #{rank}")
        print(f"  Tested across {row['num_periods_tested']:.0f} periods")
        print(f"  Avg 7-Week Return: {row['avg_7wk_return']:.1f}%")
        print(f"  Avg Annualized Return: {row['avg_return']:.1f}% (±{row['std_return']:.1f}%)")
        print(f"  Avg Sharpe Ratio: {row['avg_sharpe']:.2f} (±{row['std_sharpe']:.2f})")
        print(f"  Consistency Score: {row['consistency_score']:.2f}")
        print()
        strategies.append(('14/4/30% (NEW)', row))

    if not option1.empty:
        row = option1.iloc[0]
        rank = results_df_sorted.index.get_loc(option1.index[0]) + 1
        print(f"OPTION 1: 14 days / 4 days / 20% (10 stocks) - RANK #{rank}")
        print(f"  Tested across {row['num_periods_tested']:.0f} periods")
        print(f"  Avg 7-Week Return: {row['avg_7wk_return']:.1f}%")
        print(f"  Avg Annualized Return: {row['avg_return']:.1f}% (±{row['std_return']:.1f}%)")
        print(f"  Avg Sharpe Ratio: {row['avg_sharpe']:.2f} (±{row['std_sharpe']:.2f})")
        print(f"  Consistency Score: {row['consistency_score']:.2f}")
        print()
        strategies.append(('14/4/20% (Opt 1)', row))

    if not option2.empty:
        row = option2.iloc[0]
        rank = results_df_sorted.index.get_loc(option2.index[0]) + 1
        print(f"OPTION 2: 12 days / 3 days / 30% (15 stocks) - RANK #{rank}")
        print(f"  Tested across {row['num_periods_tested']:.0f} periods")
        print(f"  Avg 7-Week Return: {row['avg_7wk_return']:.1f}%")
        print(f"  Avg Annualized Return: {row['avg_return']:.1f}% (±{row['std_return']:.1f}%)")
        print(f"  Avg Sharpe Ratio: {row['avg_sharpe']:.2f} (±{row['std_sharpe']:.2f})")
        print(f"  Consistency Score: {row['consistency_score']:.2f}")
        print()
        strategies.append(('12/3/30% (Opt 2)', row))

    print("=" * 120)
    print("DETAILED COMPARISON")
    print("=" * 120)
    print()

    if len(strategies) >= 2:
        print(f"{'Metric':<25}", end="")
        for name, _ in strategies:
            print(f"{name:>20}", end="")
        print()
        print("-" * 120)

        metrics = [
            ('7-Week Return', 'avg_7wk_return', '%'),
            ('Annualized Return', 'avg_return', '%'),
            ('Sharpe Ratio', 'avg_sharpe', ''),
            ('Consistency Score', 'consistency_score', ''),
            ('Max Drawdown', 'max_drawdown', '%'),
            ('Std Dev (Return)', 'std_return', '%'),
            ('Std Dev (Sharpe)', 'std_sharpe', ''),
        ]

        for metric_name, metric_key, unit in metrics:
            print(f"{metric_name:<25}", end="")
            values = [row[metric_key] for _, row in strategies]
            best_idx = values.index(max(values)) if metric_key != 'max_drawdown' and metric_key != 'std_return' and metric_key != 'std_sharpe' else values.index(min(values))

            for i, (_, row) in enumerate(strategies):
                value = row[metric_key]
                marker = " 🏆" if i == best_idx else ""
                if unit == '%':
                    print(f"{value:>18.1f}%{marker}", end="")
                else:
                    print(f"{value:>19.2f}{marker}", end="")
            print()

        print()
        print("=" * 120)
        print("RECOMMENDATION")
        print("=" * 120)
        print()

        # Find best by 7-week return
        best_7wk = max(strategies, key=lambda x: x[1]['avg_7wk_return'])
        # Find best by consistency
        best_consistency = max(strategies, key=lambda x: x[1]['consistency_score'])
        # Find best by Sharpe
        best_sharpe = max(strategies, key=lambda x: x[1]['avg_sharpe'])

        print(f"🏆 Best by 7-Week Return: {best_7wk[0]} ({best_7wk[1]['avg_7wk_return']:.1f}%)")
        print(f"🏆 Best by Consistency: {best_consistency[0]} ({best_consistency[1]['consistency_score']:.2f})")
        print(f"🏆 Best by Sharpe Ratio: {best_sharpe[0]} ({best_sharpe[1]['avg_sharpe']:.2f})")
        print()

        if best_consistency[0] == best_sharpe[0]:
            print(f"✅ CLEAR WINNER: {best_consistency[0]}")
            print(f"   - Highest consistency AND highest Sharpe ratio")
            print(f"   - Expected 7-week return: {best_consistency[1]['avg_7wk_return']:.1f}%")
            print(f"   - Most reliable across different market conditions")
        else:
            print(f"⚖️  TRADE-OFF:")
            print(f"   - For maximum return: {best_7wk[0]}")
            print(f"   - For maximum reliability: {best_consistency[0]}")

    # Save to CSV
    filename = f"seven_week_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    results_df_sorted.to_csv(filename, index=False)
    print()
    print(f"📊 Full results saved to: {filename}")
    print()

    return results_df_sorted


if __name__ == "__main__":
    results = run_seven_week_optimization()
