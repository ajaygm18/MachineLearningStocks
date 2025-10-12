"""
Fetch Indian Stock Market Data using yfinance
Downloads NIFTY 50 stocks data from NSE for the period 10/10/2010 to 20/10/2025
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
from tqdm import tqdm
import time

# NIFTY 50 stocks (as of 2024) with NSE suffixes
NIFTY_50_STOCKS = [
    'ADANIENT.NS', 'ADANIPORTS.NS', 'APOLLOHOSP.NS', 'ASIANPAINT.NS', 'AXISBANK.NS',
    'BAJAJ-AUTO.NS', 'BAJFINANCE.NS', 'BAJAJFINSV.NS', 'BHARTIARTL.NS', 'BPCL.NS',
    'BRITANNIA.NS', 'CIPLA.NS', 'COALINDIA.NS', 'DIVISLAB.NS', 'DRREDDY.NS',
    'EICHERMOT.NS', 'GRASIM.NS', 'HCLTECH.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS',
    'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'INDUSINDBK.NS',
    'INFY.NS', 'ITC.NS', 'JSWSTEEL.NS', 'KOTAKBANK.NS', 'LT.NS',
    'M&M.NS', 'MARUTI.NS', 'NESTLEIND.NS', 'NTPC.NS', 'ONGC.NS',
    'POWERGRID.NS', 'RELIANCE.NS', 'SBILIFE.NS', 'SBIN.NS', 'SUNPHARMA.NS',
    'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS',
    'TITAN.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'WIPRO.NS', 'ZOMATO.NS'
]

# Date range: 10/10/2010 to 20/10/2025
START_DATE = '2010-10-10'
END_DATE = '2025-10-20'  # Will fetch up to current date

def fetch_nifty_index():
    """Fetch NIFTY 50 index data"""
    print("Fetching NIFTY 50 index data...")
    try:
        nifty = yf.download('^NSEI', start=START_DATE, end=END_DATE, progress=False)
        nifty = nifty[['Close']].copy()
        nifty.columns = ['NIFTY50']
        nifty.index.name = 'Date'
        return nifty
    except Exception as e:
        print(f"Error fetching NIFTY 50 data: {e}")
        return None

def fetch_stock_prices():
    """Fetch historical price data for all NIFTY 50 stocks"""
    print(f"Fetching price data for {len(NIFTY_50_STOCKS)} stocks...")
    
    all_prices = pd.DataFrame()
    
    for ticker in tqdm(NIFTY_50_STOCKS, desc="Downloading stocks"):
        try:
            # Download stock data
            stock = yf.download(ticker, start=START_DATE, end=END_DATE, progress=False)
            
            if not stock.empty:
                # Extract close price
                stock_close = stock[['Close']].copy()
                # Remove .NS suffix for cleaner ticker names
                clean_ticker = ticker.replace('.NS', '')
                stock_close.columns = [clean_ticker]
                
                if all_prices.empty:
                    all_prices = stock_close
                else:
                    all_prices = all_prices.join(stock_close, how='outer')
            
            time.sleep(0.1)  # Rate limiting
            
        except Exception as e:
            print(f"\nError fetching {ticker}: {e}")
            continue
    
    all_prices.index.name = 'Date'
    return all_prices

def fetch_stock_info():
    """Fetch fundamental data for stocks using yfinance"""
    print(f"Fetching fundamental data for {len(NIFTY_50_STOCKS)} stocks...")
    
    fundamental_data = []
    
    for ticker in tqdm(NIFTY_50_STOCKS, desc="Fetching fundamentals"):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            clean_ticker = ticker.replace('.NS', '')
            
            # Extract key fundamental metrics
            data_point = {
                'Ticker': clean_ticker,
                'Date': datetime.now().strftime('%Y-%m-%d'),
                'Unix': int(datetime.now().timestamp()),
                'Price': info.get('currentPrice', np.nan),
                'Market Cap': info.get('marketCap', np.nan),
                'Enterprise Value': info.get('enterpriseValue', np.nan),
                'Trailing P/E': info.get('trailingPE', np.nan),
                'Forward P/E': info.get('forwardPE', np.nan),
                'PEG Ratio': info.get('pegRatio', np.nan),
                'Price/Sales': info.get('priceToSalesTrailing12Months', np.nan),
                'Price/Book': info.get('priceToBook', np.nan),
                'Enterprise Value/Revenue': info.get('enterpriseToRevenue', np.nan),
                'Enterprise Value/EBITDA': info.get('enterpriseToEbitda', np.nan),
                'Profit Margin': info.get('profitMargins', np.nan),
                'Operating Margin': info.get('operatingMargins', np.nan),
                'Return on Assets': info.get('returnOnAssets', np.nan),
                'Return on Equity': info.get('returnOnEquity', np.nan),
                'Revenue': info.get('totalRevenue', np.nan),
                'Revenue Per Share': info.get('revenuePerShare', np.nan),
                'Quarterly Revenue Growth': info.get('revenueGrowth', np.nan),
                'Gross Profit': info.get('grossProfits', np.nan),
                'EBITDA': info.get('ebitda', np.nan),
                'Diluted EPS': info.get('trailingEps', np.nan),
                'Quarterly Earnings Growth': info.get('earningsGrowth', np.nan),
                'Total Cash': info.get('totalCash', np.nan),
                'Total Cash Per Share': info.get('totalCashPerShare', np.nan),
                'Total Debt': info.get('totalDebt', np.nan),
                'Total Debt/Equity': info.get('debtToEquity', np.nan),
                'Current Ratio': info.get('currentRatio', np.nan),
                'Book Value Per Share': info.get('bookValue', np.nan),
                'Operating Cash Flow': info.get('operatingCashflow', np.nan),
                'Levered Free Cash Flow': info.get('freeCashflow', np.nan),
                'Beta': info.get('beta', np.nan),
                '50-Day Moving Average': info.get('fiftyDayAverage', np.nan),
                '200-Day Moving Average': info.get('twoHundredDayAverage', np.nan),
                'Avg Vol (3 month)': info.get('averageVolume', np.nan),
                'Shares Outstanding': info.get('sharesOutstanding', np.nan),
                'Float': info.get('floatShares', np.nan),
                '% Held by Insiders': info.get('heldPercentInsiders', np.nan),
                '% Held by Institutions': info.get('heldPercentInstitutions', np.nan),
                'Short Ratio': info.get('shortRatio', np.nan),
                'Short % of Float': info.get('shortPercentOfFloat', np.nan),
            }
            
            fundamental_data.append(data_point)
            time.sleep(0.2)  # Rate limiting
            
        except Exception as e:
            print(f"\nError fetching fundamentals for {ticker}: {e}")
            continue
    
    return pd.DataFrame(fundamental_data)

def calculate_returns(prices_df, index_df):
    """Calculate 1-year forward returns for stocks and index"""
    returns_data = []
    
    for date in prices_df.index[:-252]:  # Skip last year for forward returns
        try:
            future_date_idx = prices_df.index.get_loc(date) + 252  # ~1 year ahead
            if future_date_idx < len(prices_df):
                future_date = prices_df.index[future_date_idx]
                
                for ticker in prices_df.columns:
                    current_price = prices_df.loc[date, ticker]
                    future_price = prices_df.loc[future_date, ticker]
                    
                    if pd.notna(current_price) and pd.notna(future_price):
                        stock_return = ((future_price - current_price) / current_price) * 100
                        
                        # Get NIFTY return
                        if date in index_df.index and future_date in index_df.index:
                            index_current = index_df.loc[date, 'NIFTY50']
                            index_future = index_df.loc[future_date, 'NIFTY50']
                            index_return = ((index_future - index_current) / index_current) * 100
                            
                            returns_data.append({
                                'Date': date.strftime('%Y-%m-%d'),
                                'Unix': int(date.timestamp()),
                                'Ticker': ticker,
                                'Price': current_price,
                                'stock_p_change': stock_return,
                                'NIFTY50': index_current,
                                'NIFTY50_p_change': index_return
                            })
        except:
            continue
    
    return pd.DataFrame(returns_data)

def main():
    """Main function to fetch and prepare Indian stock data"""
    print("="*80)
    print("Fetching Indian Stock Market Data (NIFTY 50)")
    print(f"Date Range: {START_DATE} to {END_DATE}")
    print("="*80)
    
    # Fetch NIFTY 50 index
    nifty_df = fetch_nifty_index()
    if nifty_df is not None:
        nifty_df.to_csv('nifty50_index.csv')
        print(f"✅ NIFTY 50 index saved: {len(nifty_df)} data points")
    
    # Fetch stock prices
    prices_df = fetch_stock_prices()
    if not prices_df.empty:
        prices_df.to_csv('indian_stock_prices.csv')
        print(f"✅ Stock prices saved: {len(prices_df)} dates, {len(prices_df.columns)} stocks")
    
    # Fetch current fundamental data
    fundamentals_df = fetch_stock_info()
    if not fundamentals_df.empty:
        # Add NIFTY50 and NIFTY50_p_change columns (zeros for current data)
        fundamentals_df['NIFTY50'] = np.nan
        fundamentals_df['NIFTY50_p_change'] = np.nan
        fundamentals_df['stock_p_change'] = np.nan
        
        fundamentals_df.to_csv('indian_forward_sample.csv', index=False)
        print(f"✅ Forward sample saved: {len(fundamentals_df)} stocks")
    
    # Calculate historical returns and create training dataset
    if nifty_df is not None and not prices_df.empty:
        print("\nCalculating historical returns for training data...")
        returns_df = calculate_returns(prices_df, nifty_df)
        
        if not returns_df.empty:
            # Merge with fundamental data (simplified - using current fundamentals)
            # In production, you'd want historical fundamental data
            keystats_df = returns_df.copy()
            keystats_df.to_csv('indian_keystats.csv', index=False)
            print(f"✅ Training data saved: {len(keystats_df)} records")
    
    print("\n" + "="*80)
    print("✅ Data fetching complete!")
    print("="*80)
    print("\nFiles created:")
    print("  - nifty50_index.csv")
    print("  - indian_stock_prices.csv") 
    print("  - indian_forward_sample.csv")
    print("  - indian_keystats.csv")
    print("\nNote: To use this data, update app.py to load these files instead of the US data.")

if __name__ == "__main__":
    main()
