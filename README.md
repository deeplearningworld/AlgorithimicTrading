# AlgorithimicTrading


# Algorithmic Trading Bot & Visualization
This project is a simple algorithmic trading bot that implements a moving average crossover strategy. It comes with both a command-line script for simulation and a Streamlit web application for interactive visualization. It is intended for educational purposes to demonstrate the basic components of an algorithmic trading system.

->Disclaimer: This is not financial advice. Trading financial markets involves significant risk. This bot is for educational purposes only and should not be used for live trading without extensive backtesting and understanding of the risks involved.

# Features
1.Fetches historical price data for a specified ticker symbol using yfinance.

2.Implements a simple moving average (SMA) crossover trading strategy.

3.Generates buy and sell signals based on the crossover of two SMAs.

4.Simulates placing trades and logs them to the console (main.py).

5.Provides an interactive web-based visualization of the strategy using Streamlit (app.py).

# Strategy
The bot uses a moving average crossover strategy:

Buy Signal: When the short-term moving average crosses above the long-term moving average, it indicates a potential upward trend, generating a "buy" signal.

Sell Signal: When the short-term moving average crosses below the long-term moving average, it indicates a potential downward trend, generating a "sell" signal.

# Tech Stack:

-Python 
