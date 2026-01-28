"""
Stock Price Data Fetcher

Download historical stock price data using yfinance for the defined stock universe.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def fetch_stock_data(tickers, period='1y', interval='1d'):
    """
    Fetch historical stock price data
    
    Args:
        tickers: List of stock ticker symbols
        period: Data period (e.g., '1y', '2y', '6mo')
        interval: Data interval (e.g., '1d', '1h')
    
    Returns:
        Dictionary of DataFrames, one per ticker
    """
    stock_data = {}
    
    print(f"Fetching stock data for: {tickers}")
    
    for ticker in tickers:
        print(f"Downloading {ticker}...")
        
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            
            # Add ticker column
            df['Ticker'] = ticker
            
            # Calculate daily returns
            df['Return'] = df['Close'].pct_change()
            
            # Binary target: next-day direction (1 = up, 0 = down)
            df['Next_Day_Return'] = df['Return'].shift(-1)
            df['Target'] = (df['Next_Day_Return'] > 0).astype(int)
            
            stock_data[ticker] = df
            print(f"  ✓ {ticker}: {len(df)} rows")
            
        except Exception as e:
            print(f"  ✗ Error fetching {ticker}: {e}")
    
    return stock_data


def save_stock_data(stock_data, output_dir='data/raw'):
    """Save stock data to CSV files"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save individual ticker files
    for ticker, df in stock_data.items():
        filename = f'{output_dir}/{ticker}_prices_{timestamp}.csv'
        df.to_csv(filename)
        print(f"Saved {ticker} to: {filename}")
    
    # Combine all tickers into one file
    combined_df = pd.concat(stock_data.values(), ignore_index=False)
    combined_filename = f'{output_dir}/all_stock_prices_{timestamp}.csv'
    combined_df.to_csv(combined_filename)
    print(f"\nCombined data saved to: {combined_filename}")
    
    return combined_filename


def main():
    """Main execution function"""
    # Stock universe
    tickers = ['GME', 'AMC', 'TSLA', 'NVDA', 'SPY']
    
    # Fetch 2 years of daily data
    stock_data = fetch_stock_data(tickers, period='2y', interval='1d')
    
    # Save to files
    save_stock_data(stock_data)
    
    # Print summary statistics
    print("\n" + "="*50)
    print("Summary Statistics")
    print("="*50)
    
    for ticker, df in stock_data.items():
        print(f"\n{ticker}:")
        print(f"  Date Range: {df.index.min()} to {df.index.max()}")
        print(f"  Average Daily Return: {df['Return'].mean():.4%}")
        print(f"  Volatility (Std Dev): {df['Return'].std():.4%}")
        print(f"  Up Days: {df['Target'].sum()} ({df['Target'].mean():.2%})")
    
    print("\n✓ Stock data collection complete!")


if __name__ == "__main__":
    main()
