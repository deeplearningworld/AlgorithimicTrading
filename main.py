import yfinance as yf
import pandas as pd
import numpy as np

# -- Configuration --
TICKER = 'AAPL'         # Ticker symbol for the stock (e.g., Apple)
START_DATE = '2022-01-01' # Start date for historical data
END_DATE = '2023-01-01'   # End date for historical data
SHORT_WINDOW = 40         # Short-term moving average window
LONG_WINDOW = 100         # Long-term moving average window

def fetch_data(ticker, start, end):
    """
    Fetches historical stock data from Yahoo Finance.
    
    Args:
        ticker (str): The stock ticker symbol.
        start (str): The start date in 'YYYY-MM-DD' format.
        end (str): The end date in 'YYYY-MM-DD' format.
        
    Returns:
        pandas.DataFrame: A DataFrame containing the historical data,
                          or None if data fetching fails.
    """
    print(f"Fetching data for {ticker} from {start} to {end}...")
    try:
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            print(f"No data found for {ticker}. It might be delisted or the ticker is incorrect.")
            return None
        print("Data fetched successfully.")
        return data
    except Exception as e:
        print(f"An error occurred while fetching data: {e}")
        return None

def add_moving_averages(data, short_window, long_window):
    """
    Adds short-term and long-term moving averages to the DataFrame.
    
    Args:
        data (pandas.DataFrame): The DataFrame with price data.
        short_window (int): The window size for the short-term SMA.
        long_window (int): The window size for the long-term SMA.
        
    Returns:
        pandas.DataFrame: The DataFrame with 'SMA_Short' and 'SMA_Long' columns.
    """
    print(f"Calculating moving averages (Short: {short_window}, Long: {long_window})...")
    data['SMA_Short'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    print("Moving averages calculated.")
    return data

def generate_signals(data):
    """
    Generates trading signals based on the moving average crossover strategy.
    
    Args:
        data (pandas.DataFrame): DataFrame with price data and moving averages.
        
    Returns:
        pandas.DataFrame: The DataFrame with a 'Signal' column.
    """
    print("Generating trading signals...")
    # Create a new DataFrame for signals
    signals = pd.DataFrame(index=data.index)
    signals['price'] = data['Close']
    signals['SMA_Short'] = data['SMA_Short']
    signals['SMA_Long'] = data['SMA_Long']
    
    # Generate signal when short SMA crosses long SMA
    # np.where is used for conditional logic
    signals['signal'] = 0.0
    signals['signal'] = np.where(signals['SMA_Short'] > signals['SMA_Long'], 1.0, 0.0)   
    
    # Take the difference of the signals column to generate actual trading orders
    signals['positions'] = signals['signal'].diff()
    print("Signals generated.")
    return signals

def execute_trades(signals):
    """
    Simulates the execution of trades based on the generated signals.
    
    Args:
        signals (pandas.DataFrame): DataFrame with trading signals and positions.
    """
    print("\n-- Executing Trades --")
    # A 'position' of 1 represents a buy signal, -1 represents a sell signal
    for index, row in signals.iterrows():
        if row['positions'] == 1.0:
            print(f"{index.date()}: BUY signal at price ${row['price']:.2f}")
            # In a real application, you would place a buy order here
        elif row['positions'] == -1.0:
            print(f"{index.date()}: SELL signal at price ${row['price']:.2f}")
            # In a real application, you would place a sell order here
    print("\n-- Trade simulation complete --\n")


def run_strategy():
    """
    Main function to run the entire trading strategy.
    """
    # 1. Fetch Data
    price_data = fetch_data(TICKER, START_DATE, END_DATE)
    
    if price_data is None:
        return
        
    # 2. Add Moving Averages
    price_data_with_ma = add_moving_averages(price_data, SHORT_WINDOW, LONG_WINDOW)
    
    # 3. Generate Trading Signals
    trading_signals = generate_signals(price_data_with_ma)
    
    # 4. Execute Trades (Simulation)
    execute_trades(trading_signals)
    
    # Optional: Display the first few rows of the signals DataFrame
    print("--- Sample of Generated Signals ---")
    print(trading_signals.head(10))
    print("\n--- Sample of Trades ---")
    print(trading_signals[trading_signals['positions'] != 0].head())


if __name__ == "__main__":
    # Entry point of the script
    run_strategy()