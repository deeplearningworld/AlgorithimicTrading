import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- Core Trading Logic Functions ---

def fetch_data(ticker, start, end):
    """
    Fetches historical stock data from Yahoo Finance.
    """
    try:
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            st.error(f"No data found for {ticker}. It might be delisted or the ticker is incorrect.")
            return None
        return data
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")
        return None

def add_moving_averages(data, short_window, long_window):
    """
    Adds short-term and long-term moving averages to the DataFrame.
    """
    data['SMA_Short'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window, min_periods=1).mean()
    return data

def generate_signals(data):
    """
    Generates trading signals based on the moving average crossover strategy.
    """
    signals = pd.DataFrame(index=data.index)
    signals['price'] = data['Close']
    signals['SMA_Short'] = data['SMA_Short']
    signals['SMA_Long'] = data['SMA_Long']
    
    # Generate signal: 1 when short > long, 0 otherwise
    signals['signal'] = 0.0
    signals['signal'] = np.where(signals['SMA_Short'] > signals['SMA_Long'], 1.0, 0.0)   
    
    # Find the exact crossover points
    signals['positions'] = signals['signal'].diff()
    return signals

# --- Streamlit Web App ---

st.set_page_config(page_title="Algorithmic Trading Bot", layout="wide")

st.title('Algorithmic Trading Strategy Visualization')
st.caption('This app visualizes a simple moving average (SMA) crossover trading strategy.')

# --- Sidebar for User Inputs ---
st.sidebar.header('⚙️ Configuration')
ticker = st.sidebar.text_input('Ticker Symbol', 'AAPL').upper()
start_date = st.sidebar.date_input('Start Date', pd.to_datetime('2022-01-01'))
end_date = st.sidebar.date_input('End Date', pd.to_datetime('2023-01-01'))
short_window = st.sidebar.slider('Short SMA Window', 10, 200, 40, 5)
long_window = st.sidebar.slider('Long SMA Window', 10, 200, 100, 5)

# --- Main Application Logic ---

# Validate that the long window is greater than the short window
if long_window <= short_window:
    st.sidebar.error('Error: Long window must be greater than the short window.')
else:
    # 1. Fetch Data
    data = fetch_data(ticker, start_date, end_date)
    
    if data is not None:
        # 2. Add Moving Averages
        data_with_ma = add_moving_averages(data, short_window, long_window)
        
        # 3. Generate Trading Signals
        signals = generate_signals(data_with_ma)
        
        # --- Visualization ---
        st.subheader(f'Price and Trading Signals for {ticker}')
        
        # Create an interactive Plotly chart
        fig = go.Figure()

        # Add Close Price line
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price', line=dict(color='skyblue')))
        
        # Add Moving Averages
        fig.add_trace(go.Scatter(x=signals.index, y=signals['SMA_Short'], mode='lines', name=f'SMA {short_window}', line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=signals.index, y=signals['SMA_Long'], mode='lines', name=f'SMA {long_window}', line=dict(color='purple')))
        
        # Add Buy Signals to the chart
        buy_signals = signals[signals['positions'] == 1.0]
        fig.add_trace(go.Scatter(
            x=buy_signals.index, 
            y=buy_signals['price'], 
            mode='markers', 
            name='Buy Signal', 
            marker=dict(symbol='triangle-up', color='green', size=12, line=dict(width=1, color='DarkSlateGrey'))
        ))
        
        # Add Sell Signals to the chart
        sell_signals = signals[signals['positions'] == -1.0]
        fig.add_trace(go.Scatter(
            x=sell_signals.index, 
            y=sell_signals['price'], 
            mode='markers', 
            name='Sell Signal',
            marker=dict(symbol='triangle-down', color='red', size=12, line=dict(width=1, color='DarkSlateGrey'))
        ))

        # Customize the layout
        fig.update_layout(
            title=f'{ticker} Trading Signals (SMA Crossover)',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            legend_title='Legend',
            template='plotly_dark' # Use a dark theme
        )
        
        st.plotly_chart(fig, use_container_width=True)

        # --- Display Trade Log ---
        st.subheader('Trade Log')
        trade_log = signals[signals['positions'].isin([1.0, -1.0])].copy()
        trade_log['Action'] = trade_log['positions'].apply(lambda x: 'BUY' if x == 1.0 else 'SELL')
        trade_log = trade_log[['price', 'Action']]
        trade_log.rename(columns={'price': 'Price at Signal'}, inplace=True)
        st.dataframe(trade_log)