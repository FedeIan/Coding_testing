import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from datetime import datetime, timedelta
import numpy as np
from statsmodels.tsa.arima.model import ARIMA


def download_stock_data(ticker):
    """Download stock data from Yahoo Finance for the past 5 years."""
    end = datetime.today().strftime('%Y-%m-%d')
    start = (datetime.today() - timedelta(weeks=260)).strftime('%Y-%m-%d')
    data = yf.download(ticker, start=start, end=end)
    return data[['Close', 'High', 'Low']]


def prepare_data_for_prophet(data):
    """Prepare stock data for Prophet model."""
    if data.empty:
        raise ValueError("Error: No stock data available. Check the ticker symbol.")

    # Reset index
    data = data.reset_index()

    # Ensure correct column names
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]

    if 'Date' not in data.columns:
        raise ValueError("Error: 'Date' column not found in dataset. Verify data integrity.")

    if 'Close' not in data.columns:
        raise ValueError("Error: 'Close' column not found! Check ticker validity.")

    # Rename columns for Prophet
    data = data.rename(columns={'Date': 'ds', 'Close': 'y'})

    # Convert 'y' column to numeric
    data['y'] = pd.to_numeric(data['y'], errors='coerce')

    # Drop NaN values
    data = data.dropna()

    return data


def find_support_resistance(data):
    """Identify support and resistance levels using historical price data."""
    data['Support'] = data['Low'].rolling(window=50).min()
    data['Resistance'] = data['High'].rolling(window=50).max()
    return data


def calculate_atr(data):
    """Calculate the Average True Range (ATR)."""
    high_low = data['High'] - data['Low']
    high_close = abs(data['High'] - data['Close'].shift())
    low_close = abs(data['Low'] - data['Close'].shift())

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    data['ATR'] = tr.rolling(window=14).mean()
    return data


def forecast_with_arima(data, periods=60):
    """Train ARIMA model and forecast future stock prices."""
    data = data.set_index('ds')['y']
    model = ARIMA(data, order=(5, 1, 0))  # ARIMA(p,d,q) - (autoregressive, differencing, moving average)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=periods)
    return forecast


def forecast_with_prophet(ticker, periods=60):
    """Train Prophet and ARIMA models and forecast future stock prices."""
    data = download_stock_data(ticker)
    df = prepare_data_for_prophet(data)
    data = find_support_resistance(data)
    data = calculate_atr(data)

    # Prophet Model
    model = Prophet(
        daily_seasonality=False,
        yearly_seasonality=True,
        weekly_seasonality=True,
        interval_width=0.7
    )

    model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    model.fit(df)

    # Create future dataframe
    future = model.make_future_dataframe(periods=periods)
    forecast_prophet = model.predict(future)

    # ARIMA Model
    forecast_arima = forecast_with_arima(df, periods)
    future_dates = pd.date_range(start=df['ds'].iloc[-1], periods=periods + 1, freq='D')[1:]

    # Plot results
    plt.figure(figsize=(12, 6))
    plt.plot(df['ds'], df['y'], label='Historical Data', color='black')
    plt.plot(forecast_prophet['ds'], forecast_prophet['yhat'], label='Prophet Forecast', linestyle='dashed',
             color='blue')
    plt.fill_between(forecast_prophet['ds'], forecast_prophet['yhat_lower'], forecast_prophet['yhat_upper'],
                     color='blue', alpha=0.2, label='Prophet Uncertainty Interval')
    plt.plot(future_dates, forecast_arima, label='ARIMA Forecast', linestyle='dashed', color='orange')
    plt.plot(data.index, data['Support'], label='Support Level', linestyle='dotted', color='green')
    plt.plot(data.index, data['Resistance'], label='Resistance Level', linestyle='dotted', color='red')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title(f'Forecast for {ticker} with Prophet & ARIMA')
    plt.legend()
    plt.show()


# Usage example
if __name__ == "__main__":
    ticker = input("Enter the stock ticker: ").strip().upper()
    forecast_with_prophet(ticker)
