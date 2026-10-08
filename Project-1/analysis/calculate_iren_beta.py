"""Calculate IREN's historical beta versus the SPY market proxy.

This uses daily closing prices from Nasdaq's public historical-data endpoint.
SPY is used as a practical proxy for the S&P 500.  The result is a price-return
beta; it does not include SPY cash dividends.

Example:
    ..\\Python-3.13.15\\python.exe .\\analysis\\calculate_iren_beta.py
"""

import json
from datetime import date, timedelta
from urllib.parse import urlencode
from urllib.request import Request, urlopen


LOOKBACK_DAYS = 730  # approximately two years


def get_closing_prices(symbol, asset_class, start_date, end_date):
    """Download date-to-close data from Nasdaq and return it oldest first."""
    parameters = urlencode(
        {
            "assetclass": asset_class,
            "fromdate": start_date.isoformat(),
            "todate": end_date.isoformat(),
            "limit": 5000,
        }
    )
    url = f"https://api.nasdaq.com/api/quote/{symbol}/historical?{parameters}"
    request = Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})

    with urlopen(request, timeout=30) as response:
        payload = json.load(response)

    rows = payload.get("data", {}).get("tradesTable", {}).get("rows", [])
    if not rows:
        raise ValueError(f"Nasdaq returned no price data for {symbol}.")

    prices = {}
    for row in rows:
        close = row["close"].replace("$", "").replace(",", "")
        prices[row["date"]] = float(close)
    return prices


def calculate_beta(stock_prices, market_prices):
    """Calculate beta from matched daily simple returns."""
    def parse_date(value):
        if "-" in value:
            return date.fromisoformat(value)
        month, day, year = value.split("/")
        return date(int(year), int(month), int(day))

    dates = sorted(set(stock_prices) & set(market_prices), key=parse_date)
    if len(dates) < 3:
        raise ValueError("Not enough matched price observations.")

    stock_returns = []
    market_returns = []
    for previous_date, current_date in zip(dates, dates[1:]):
        stock_returns.append(stock_prices[current_date] / stock_prices[previous_date] - 1)
        market_returns.append(market_prices[current_date] / market_prices[previous_date] - 1)

    average_stock_return = sum(stock_returns) / len(stock_returns)
    average_market_return = sum(market_returns) / len(market_returns)
    covariance = sum(
        (stock_return - average_stock_return) * (market_return - average_market_return)
        for stock_return, market_return in zip(stock_returns, market_returns)
    ) / (len(stock_returns) - 1)
    market_variance = sum(
        (market_return - average_market_return) ** 2 for market_return in market_returns
    ) / (len(market_returns) - 1)

    return covariance / market_variance, dates, len(stock_returns)


def main():
    end_date = date.today()
    start_date = end_date - timedelta(days=LOOKBACK_DAYS)
    iren_prices = get_closing_prices("IREN", "stocks", start_date, end_date)
    spy_prices = get_closing_prices("SPY", "etf", start_date, end_date)
    beta, dates, return_periods = calculate_beta(iren_prices, spy_prices)

    print("IREN historical beta calculation")
    print("Market proxy: SPY (S&P 500 ETF)")
    print(f"Matched price dates: {dates[0]} through {dates[-1]}")
    print(f"Price observations: {len(dates)}")
    print(f"Daily return periods: {return_periods}")
    print("Formula: covariance(IREN daily returns, SPY daily returns) / variance(SPY daily returns)")
    print(f"IREN beta: {beta:.4f}")


if __name__ == "__main__":
    main()
