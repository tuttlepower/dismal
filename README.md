# Dismal - Economic Dashboard

A lightweight economic dashboard that fetches market data daily from Yahoo Finance, generating a static JSON file that powers a simple visualization page.

**No API keys required.**

## What It Shows

| Metric | Ticker | Description |
|--------|--------|-------------|
| S&P 500 (SPY) | SPY | S&P 500 ETF |
| Bitcoin | BTC-USD | Bitcoin price |
| 10-Year Treasury | ^TNX | Long-term rates |
| 13-Week T-Bill | ^IRX | Short-term rates |
| Gold | GC=F | Gold futures |
| VIX | ^VIX | Volatility/fear index |
| US Dollar Index | DX-Y.NYB | Dollar strength |

Plus a **yield spread** indicator (10Y - 13W) to flag potential inversions.

## Usage

### Local Development

```bash
pip install -r requirements.txt
python dashboard.py
# Open index.html in a browser
```

### GitHub Actions (Automated)

The workflow runs daily at 1 PM UTC and commits updated `data.json` to the repo. No configuration needed - just enable Actions on your fork.

## Using with Claude

The `data.json` file is designed to be easily consumable by LLMs. You can:
- Paste the raw JSON URL into Claude chat
- Ask questions like "Is the yield curve inverted? How has the VIX moved recently?"

## Files

- `dashboard.py` - Fetches data from Yahoo Finance
- `index.html` - Static page with Chart.js visualizations
- `data.json` - Generated output with all metrics and 2 years of history
- `requirements.txt` - Python dependencies (just yfinance)
