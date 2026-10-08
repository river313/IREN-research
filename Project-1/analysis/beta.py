"""Calculate a stock's beta from matched stock and market closing prices.

CSV format:
date,stock_close,market_close
2026-01-02,10.25,600.15
2026-01-05,10.40,603.20

Example:
    python beta.py prices.csv
"""

import argparse
import csv
from pathlib import Path


def load_prices(csv_path):
    """Read chronological matched closing prices from a CSV file."""
    prices = []
    with open(csv_path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        required_columns = {"date", "stock_close", "market_close"}
        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(
                "CSV must contain these headers: date, stock_close, market_close"
            )
        for row in reader:
            prices.append(
                (row["date"], float(row["stock_close"]), float(row["market_close"]))
            )

    if len(prices) < 3:
        raise ValueError("Provide at least three price observations.")
    return prices


def calculate_beta(prices):
    """Return beta = covariance(stock returns, market returns) / variance(market)."""
    stock_returns = []
    market_returns = []

    for (_, prior_stock, prior_market), (_, stock, market) in zip(prices, prices[1:]):
        if prior_stock == 0 or prior_market == 0:
            raise ValueError("Closing prices cannot be zero.")
        stock_returns.append(stock / prior_stock - 1)
        market_returns.append(market / prior_market - 1)

    mean_stock = sum(stock_returns) / len(stock_returns)
    mean_market = sum(market_returns) / len(market_returns)
    covariance = sum(
        (stock_return - mean_stock) * (market_return - mean_market)
        for stock_return, market_return in zip(stock_returns, market_returns)
    ) / (len(stock_returns) - 1)
    market_variance = sum(
        (market_return - mean_market) ** 2 for market_return in market_returns
    ) / (len(market_returns) - 1)

    if market_variance == 0:
        raise ValueError("Market returns have zero variance, so beta is undefined.")
    return covariance / market_variance, len(stock_returns)


def main():
    parser = argparse.ArgumentParser(description="Calculate beta from closing prices.")
    parser.add_argument("csv_file", type=Path, help="CSV with date,stock_close,market_close")
    args = parser.parse_args()

    prices = load_prices(args.csv_file)
    beta, return_periods = calculate_beta(prices)
    print(f"Observations: {len(prices)} prices / {return_periods} return periods")
    print(f"Beta: {beta:.4f}")


if __name__ == "__main__":
    main()
