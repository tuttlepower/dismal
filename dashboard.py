#!/usr/bin/env python3
"""
Economic Dashboard - Fetches market data for visualization.

All data sourced from Yahoo Finance via yfinance (no API key required).
"""

import json
from datetime import datetime, timezone

import yfinance as yf

OUTPUT_FILE = "data.json"
HISTORY_PERIOD = "2y"  # 2 years of history

# All data from Yahoo Finance - no API keys needed
TICKERS = {
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
    "treasury_10y": {
        "ticker": "^TNX",
        "name": "10-Year Treasury Yield",
        "unit": "%",
        "description": "CBOE 10-Year Treasury Note Yield Index"
    },
    "treasury_2y": {
        "ticker": "^IRX",
        "name": "13-Week Treasury Bill",
        "unit": "%",
        "description": "CBOE 13-Week Treasury Bill Index (proxy for short-term rates)"
    },
    "gold": {
        "ticker": "GC=F",
        "name": "Gold",
        "unit": "USD",
        "description": "Gold Futures"
    },
    "vix": {
        "ticker": "^VIX",
        "name": "VIX (Volatility Index)",
        "unit": "Index",
        "description": "CBOE Volatility Index - market fear gauge"
    },
    "dxy": {
        "ticker": "DX-Y.NYB",
        "name": "US Dollar Index",
        "unit": "Index",
        "description": "US Dollar Index - dollar strength"
    },
}


def fetch_ticker_data(config):
    """Fetch historical data from Yahoo Finance."""
    ticker = yf.Ticker(config["ticker"])
    hist = ticker.history(period=HISTORY_PERIOD)

    if hist.empty:
        raise ValueError(f"No data returned for {config['ticker']}")

    # Convert to list of [timestamp_ms, close_price]
    data = []
    for date, row in hist.iterrows():
        timestamp_ms = int(date.timestamp() * 1000)
        value = row["Close"]
        # Treasury yields from Yahoo are already in percentage points
        data.append([timestamp_ms, round(float(value), 2)])

    # Calculate changes
    latest = data[-1][1] if data else None
    change_1d = None
    change_1w = None
    change_1m = None

    if len(data) >= 2:
        prev = data[-2][1]
        change_1d = round(((latest - prev) / prev) * 100, 2) if prev else None

    if len(data) >= 6:  # ~1 week of trading days
        prev_week = data[-6][1]
        change_1w = round(((latest - prev_week) / prev_week) * 100, 2) if prev_week else None

    if len(data) >= 22:  # ~1 month of trading days
        prev_month = data[-22][1]
        change_1m = round(((latest - prev_month) / prev_month) * 100, 2) if prev_month else None

    return {
        "name": config["name"],
        "unit": config["unit"],
        "description": config["description"],
        "ticker": config["ticker"],
        "data": data,
        "latest": latest,
        "change_1d_pct": change_1d,
        "change_1w_pct": change_1w,
        "change_1m_pct": change_1m,
    }


def calculate_yield_spread(metrics):
    """Calculate 10Y-13W Treasury spread (yield curve indicator)."""
    t10 = metrics.get("treasury_10y", {}).get("latest")
    t2 = metrics.get("treasury_2y", {}).get("latest")

    if t10 is not None and t2 is not None:
        spread = round(t10 - t2, 2)
        return {
            "spread": spread,
            "inverted": spread < 0,
            "description": "10Y minus 13W Treasury yield. Negative = inverted yield curve (recession signal)"
        }
    return None


def main():
    metrics = {}
    errors = []

    # Fetch all ticker data from Yahoo Finance
    for key, config in TICKERS.items():
        try:
            print(f"Fetching {config['name']}...")
            metrics[key] = fetch_ticker_data(config)
            print(f"  Latest: {metrics[key]['latest']} {config['unit']}")
        except Exception as e:
            errors.append({"source": key, "ticker": config["ticker"], "error": str(e)})
            print(f"  Error: {e}")

    # Calculate derived metrics
    yield_spread = calculate_yield_spread(metrics)

    # Build output
    output = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "metrics": metrics,
        "summary": {
            "yield_spread": yield_spread,
        },
        "errors": errors if errors else None,
    }

    # Write JSON
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nData written to {OUTPUT_FILE}")
    print(f"Generated at: {output['generated']}")
    if yield_spread:
        status = "INVERTED" if yield_spread["inverted"] else "normal"
        print(f"Yield spread (10Y-13W): {yield_spread['spread']}% ({status})")


if __name__ == "__main__":
    main()
