# Dismal - Economic Dashboard

A lightweight economic dashboard that fetches market and macroeconomic data daily, generating a static JSON file that powers a simple visualization page.

## What It Shows

| Metric | Source | Update Frequency |
|--------|--------|------------------|
| S&P 500 (SPY) | Yahoo Finance | Daily |
| Bitcoin (BTC-USD) | Yahoo Finance | Daily |
| 10-Year Treasury Yield | FRED | Daily |
| 2-Year Treasury Yield | FRED | Daily |
| CPI Inflation | FRED | Monthly |
| Unemployment Rate | FRED | Monthly |
| Job Openings (JOLTS) | FRED | Monthly |

Plus a **yield curve spread** indicator (10Y - 2Y) to flag potential inversions.

## Usage

### Local Development

1. Get a free FRED API key from https://fred.stlouisfed.org/docs/api/api_key.html
2. Set the environment variable:
   ```bash
   export FRED_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the dashboard script:
   ```bash
   python dashboard.py
   ```
5. Open `index.html` in a browser to view the charts.

### GitHub Actions (Automated)

The workflow runs daily at 1 PM UTC and commits updated `data.json` to the repo.

To enable it:
1. Go to your repo's Settings > Secrets and variables > Actions
2. Add a new secret named `FRED_API_KEY` with your API key

## Using with Claude

The `data.json` file is designed to be easily consumable by LLMs. You can:
- Paste the raw JSON URL into Claude chat
- Ask questions like "Is the yield curve inverted? What does the jobs data suggest?"

## Files

- `dashboard.py` - Fetches data from Yahoo Finance and FRED
- `index.html` - Static page with Chart.js visualizations
- `data.json` - Generated output with all metrics and historical data
- `requirements.txt` - Python dependencies
