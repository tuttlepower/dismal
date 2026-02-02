#!/usr/bin/env python3
"""
Economic Dashboard - Fetches market and economic data for visualization.

Data Sources:
- Yahoo Finance (via yfinance): SPY, BTC-USD
- FRED API: CPI, Unemployment, Job Openings, Treasury Yields

Requires FRED_API_KEY environment variable (free from https://fred.stlouisfed.org/docs/api/api_key.html)
"""

import json
import os
from datetime import datetime, timezone

import yfinance as yf
from fredapi import Fred

OUTPUT_FILE = "data.json"
HISTORY_PERIOD = "2y"  # 2 years of history for market data

# FRED series IDs
FRED_SERIES = {
    "cpi": {
        "id": "CPIAUCSL",
        "name": "CPI (Consumer Price Index)",
        "unit": "Index",
        "description": "Consumer Price Index for All Urban Consumers"
    },
    "unemployment": {
        "id": "UNRATE",
        "name": "Unemployment Rate",
        "unit": "%",
        "description": "Civilian Unemployment Rate"
    },
    "job_openings": {
        "id": "JTSJOL",
        "name": "Job Openings (JOLTS)",
        "unit": "Thousands",
        "description": "Job Openings: Total Nonfarm"
    },
    "treasury_10y": {
        "id": "DGS10",
        "name": "10-Year Treasury Yield",
        "unit": "%",
        "description": "Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity"
    },
    "treasury_2y": {
        "id": "DGS2",
        "name": "2-Year Treasury Yield",
        "unit": "%",
        "description": "Market Yield on U.S. Treasury Securities at 2-Year Constant Maturity"
    },
}

# Yahoo Finance tickers
MARKET_TICKERS = {
    "spy": {
        "ticker": "SPY",
        "name": "S&P 500 ETF (SPY)",
        "unit": "USD",
        "description": "SPDR S&P 500 ETF Trust"
    },
    "btc": {
        "ticker": "BTC-USD",
        "name": "Bitcoin",
        "unit": "USD",
        "description": "Bitcoin USD"
    },
}


def fetch_market_data(ticker_config):
    """Fetch historical market data from Yahoo Finance."""
    ticker = yf.Ticker(ticker_config["ticker"])
    hist = ticker.history(period=HISTORY_PERIOD)

    # Convert to list of [timestamp_ms, close_price]
    data = []
    for date, row in hist.iterrows():
        timestamp_ms = int(date.timestamp() * 1000)
        data.append([timestamp_ms, round(row["Close"], 2)])

    # Calculate changes
    if len(data) >= 2:
        latest = data[-1][1]
        prev = data[-2][1]
        change_1d = round(((latest - prev) / prev) * 100, 2)
    else:
        change_1d = None

    return {
        "name": ticker_config["name"],
        "unit": ticker_config["unit"],
        "description": ticker_config["description"],
        "data": data,
        "latest": data[-1][1] if data else None,
        "change_1d_pct": change_1d,
    }


def fetch_fred_series(fred, series_config):
    """Fetch historical data from FRED."""
    series = fred.get_series(series_config["id"])

    # Convert to list of [timestamp_ms, value], dropping NaN values
    data = []
    for date, value in series.items():
        if not pd.isna(value):
            timestamp_ms = int(date.timestamp() * 1000)
            data.append([timestamp_ms, round(float(value), 2)])

    # Get latest value
    latest = data[-1][1] if data else None

    return {
        "name": series_config["name"],
        "unit": series_config["unit"],
        "description": series_config["description"],
        "fred_id": series_config["id"],
        "data": data,
        "latest": latest,
    }


def calculate_yield_curve_spread(metrics):
    """Calculate 10Y-2Y Treasury spread (yield curve indicator)."""
    t10 = metrics.get("treasury_10y", {}).get("latest")
    t2 = metrics.get("treasury_2y", {}).get("latest")

    if t10 is not None and t2 is not None:
        spread = round(t10 - t2, 2)
        return {
            "spread": spread,
            "inverted": spread < 0,
            "description": "10Y minus 2Y Treasury yield. Negative = inverted yield curve (recession signal)"
        }
    return None


def main():
    # Check for FRED API key
    fred_api_key = os.environ.get("FRED_API_KEY")
    if not fred_api_key:
        raise ValueError(
            "FRED_API_KEY environment variable not set. "
            "Get a free API key at https://fred.stlouisfed.org/docs/api/api_key.html"
        )

    fred = Fred(api_key=fred_api_key)

    # Import pandas here (fredapi uses it)
    global pd
    import pandas as pd

    metrics = {}
    errors = []

    # Fetch market data from Yahoo Finance
    for key, config in MARKET_TICKERS.items():
        try:
            print(f"Fetching {config['name']}...")
            metrics[key] = fetch_market_data(config)
        except Exception as e:
            errors.append({"source": key, "error": str(e)})
            print(f"  Error: {e}")

    # Fetch economic data from FRED
    for key, config in FRED_SERIES.items():
        try:
            print(f"Fetching {config['name']}...")
            metrics[key] = fetch_fred_series(fred, config)
        except Exception as e:
            errors.append({"source": key, "error": str(e)})
            print(f"  Error: {e}")

    # Calculate derived metrics
    yield_curve = calculate_yield_curve_spread(metrics)

    # Build output
    output = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "metrics": metrics,
        "summary": {
            "yield_curve": yield_curve,
        },
        "errors": errors if errors else None,
    }

    # Write JSON
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nData written to {OUTPUT_FILE}")
    print(f"Generated at: {output['generated']}")
    if yield_curve:
        status = "INVERTED" if yield_curve["inverted"] else "normal"
        print(f"Yield curve: {yield_curve['spread']}% ({status})")


if __name__ == "__main__":
    main()
