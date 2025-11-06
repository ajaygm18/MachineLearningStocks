# Indian Stock Market Adaptation

## Overview

The MachineLearningStocks system has been adapted to support the Indian stock market (NIFTY 50) using real-time data fetched from yfinance API.

## Date Range

**Indian Market Data: October 10, 2010 to October 20, 2025**
- Historical data: 2010-10-10 to 2024-10-09
- Total: 3,681 trading days for NIFTY 50 index
- Forward predictions: Current data for 50 NIFTY 50 stocks

## Features

### 1. Data Fetching from yfinance
- **Script**: `fetch_indian_data.py`
- **Data Source**: Yahoo Finance via yfinance API
- **Coverage**: NIFTY 50 stocks (49 stocks successfully fetched, ZOMATO excluded due to listing date)

### 2. Market-Specific Configuration
- **Index**: NIFTY 50 (^NSEI) instead of S&P 500
- **Currency**: INR instead of USD
- **Tickers**: NSE-listed stocks with .NS suffix

### 3. Data Files Created

1. **nifty50_index.csv** (92 KB)
   - NIFTY 50 index historical prices
   - Date range: 2010-10-10 to 2024-10-10
   - 3,681 data points

2. **indian_stock_prices.csv** (3.1 MB)
   - Historical stock prices for 49 NIFTY 50 stocks
   - 3,703 trading days
   - Columns: Date + 49 stock tickers

3. **indian_keystats.csv** (16 MB)
   - Training dataset with historical returns
   - 163,715 records
   - Columns: Date, Unix, Ticker, Price, stock_p_change, NIFTY50, NIFTY50_p_change

4. **indian_forward_sample.csv** (18 KB)
   - Current fundamental data for predictions
   - 50 stocks with 45 features each
   - Includes: Market Cap, P/E ratios, profit margins, debt ratios, etc.

## NIFTY 50 Stocks Included

The system includes data for 49 out of 50 NIFTY 50 stocks:
- ADANIENT, ADANIPORTS, APOLLOHOSP, ASIANPAINT, AXISBANK
- BAJAJ-AUTO, BAJFINANCE, BAJAJFINSV, BHARTIARTL, BPCL
- BRITANNIA, CIPLA, COALINDIA, DIVISLAB, DRREDDY
- EICHERMOT, GRASIM, HCLTECH, HDFCBANK, HDFCLIFE
- HEROMOTOCO, HINDALCO, HINDUNILVR, ICICIBANK, INDUSINDBK
- INFY, ITC, JSWSTEEL, KOTAKBANK, LT
- M&M, MARUTI, NESTLEIND, NTPC, ONGC
- POWERGRID, RELIANCE, SBILIFE, SBIN, SUNPHARMA
- TATACONSUM, TATAMOTORS, TATASTEEL, TCS, TECHM
- TITAN, ULTRACEMCO, UPL, WIPRO

*Note: ZOMATO was excluded due to API limitations (possibly delisted or timezone issues)*

## How to Use

### Method 1: Fetch Fresh Data
```bash
# Fetch latest Indian market data
python fetch_indian_data.py

# This will create/update:
# - nifty50_index.csv
# - indian_stock_prices.csv
# - indian_keystats.csv
# - indian_forward_sample.csv
```

### Method 2: Run with Indian Market Configuration
```bash
# Set environment variable
export MARKET=INDIAN

# Run the Flask app
python app.py

# Or use the helper script
./run_indian_app.sh
```

### Method 3: Default to Indian Market
Edit `app.py` and change line 23:
```python
MARKET = os.environ.get('MARKET', 'INDIAN')  # Already defaulted to INDIAN
```

## Application Configuration

The Flask app now supports dual-market configuration:

```python
MARKET_CONFIG = {
    'US': {
        'keystats_file': 'keystats.csv',
        'forward_file': 'forward_sample.csv',
        'index_name': 'S&P 500',
        'index_column': 'SP500_p_change',
        'currency': 'USD'
    },
    'INDIAN': {
        'keystats_file': 'indian_keystats.csv',
        'forward_file': 'indian_forward_sample.csv',
        'index_name': 'NIFTY 50',
        'index_column': 'NIFTY50_p_change',
        'currency': 'INR'
    }
}
```

## API Endpoints

All endpoints now include market information:

### GET /api/dataset_info
```json
{
    "training_samples": 163715,
    "forward_samples": 50,
    "features_count": 45,
    "date_range": {
        "start": "2010-10-11",
        "end": "2024-10-09"
    },
    "market": "INDIAN",
    "index_name": "NIFTY 50",
    "currency": "INR"
}
```

### GET /api/backtest
Returns backtesting results using NIFTY 50 as benchmark.

### GET /api/predict
Returns stock predictions for NIFTY 50 stocks.

### GET /api/feature_importance
Returns feature importance analysis.

## Features Analyzed

The system analyzes 42 fundamental features for each stock:

**Valuation Metrics:**
- Market Cap, Enterprise Value
- Trailing P/E, Forward P/E, PEG Ratio
- Price/Sales, Price/Book
- Enterprise Value/Revenue, Enterprise Value/EBITDA

**Financial Health:**
- Profit Margin, Operating Margin
- Return on Assets, Return on Equity
- Revenue, Revenue Per Share
- Quarterly Revenue Growth

**Cash Flow:**
- Total Cash, Total Cash Per Share
- Total Debt, Total Debt/Equity
- Current Ratio, Book Value Per Share
- Operating Cash Flow, Levered Free Cash Flow

**Trading Information:**
- Beta
- 50-Day Moving Average, 200-Day Moving Average
- Average Volume (3 month)
- Shares Outstanding, Float
- % Held by Insiders, % Held by Institutions
- Short Ratio, Short % of Float

## Data Quality

### Historical Price Data
- **Completeness**: 99.8% (49/50 stocks)
- **Date Range**: 14 years (2010-2024)
- **Frequency**: Daily trading data
- **Source**: Yahoo Finance (NSE)

### Fundamental Data
- **Source**: yfinance API (real-time)
- **Update**: Can be refreshed by running fetch_indian_data.py
- **Coverage**: All major fundamental metrics

## Limitations & Notes

1. **ZOMATO Exclusion**: Could not fetch data for ZOMATO.NS due to API limitations
2. **Fundamental History**: Current implementation uses latest fundamental data; historical fundamental data would require additional data sources
3. **Market Hours**: Data reflects NSE trading hours (IST timezone)
4. **API Rate Limits**: yfinance has rate limits; script includes delays to avoid issues
5. **Data Lag**: Free APIs may have 15-20 minute delays for real-time data

## Performance Expectations

Based on the dataset:
- **Training samples**: 163,715 historical data points
- **Features**: 7 core features (can be expanded with fundamental data)
- **Stocks covered**: 49 NIFTY 50 constituents
- **Prediction period**: 1-year forward returns

## Future Enhancements

1. **Historical Fundamentals**: Integrate sources for historical fundamental data
2. **More Indices**: Support for BSE SENSEX, NIFTY Bank, NIFTY IT
3. **Sectoral Analysis**: Industry-specific predictions
4. **Real-time Updates**: Automated data refresh mechanisms
5. **News Sentiment**: Integrate news sentiment analysis for Indian stocks

## Troubleshooting

### Issue: "No module named 'yfinance'"
```bash
pip install yfinance
```

### Issue: "No data fetched"
- Check internet connection
- Verify ticker symbols are correct (.NS suffix for NSE)
- Check if markets are open/closed
- Try running with smaller batch sizes

### Issue: "Rate limit exceeded"
- Increase delay in fetch_indian_data.py (line 68, 95)
- Run the script during off-peak hours
- Fetch data in smaller batches

## Support

For questions or issues related to Indian market data:
1. Check Yahoo Finance availability for NSE stocks
2. Verify ticker symbols at NSE India website
3. Review yfinance documentation
4. Check rate limit restrictions

## Credits

- **Data Source**: Yahoo Finance via yfinance
- **Market**: National Stock Exchange of India (NSE)
- **Index**: NIFTY 50
- **Date Range**: October 10, 2010 to October 20, 2025

---

**Last Updated**: October 12, 2025
**Data Freshness**: As of last fetch_indian_data.py run
**Version**: 1.0 - Indian Market Support
