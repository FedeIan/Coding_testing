import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from datetime import datetime, timedelta
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import xgboost as xgb
from sklearn.model_selection import train_test_split


def download_stock_data(ticker):
    """Download stock data from Yahoo Finance for the past 5 years."""
    end = datetime.today().strftime('%Y-%m-%d')
    start = (datetime.today() - timedelta(weeks=260)).strftime('%Y-%m-%d')
    data = yf.download(ticker, start=start, end=end)
    return data[['Close', 'High', 'Low']]


def prepare_data_for_xgboost(data):
    """Prepare data for XGBoost."""
    data['Return'] = data['Close'].pct_change()
    data['SMA_10'] = data['Close'].rolling(window=10).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['ATR'] = (data['High'] - data['Low']).rolling(window=14).mean()
    data = data.dropna()

    X = data[['Return', 'SMA_10', 'SMA_50', 'ATR']]
    y = data['Close'].shift(-1).dropna()
    X = X.iloc[:-1]
    return X, y


def train_xgboost_model(X, y):
    """Train XGBoost model."""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mape = mean_absolute_percentage_error(y_test, y_pred) * 100
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"XGBoost MAPE: {mape:.2f}%, RMSE: {rmse:.2f}")

    return model


def forecast_with_xgboost(model, X, periods=60):
    """Generate forecast using trained XGBoost model."""
    future_predictions = []
    last_features = X.iloc[-1].values.reshape(1, -1)

    for _ in range(periods):
        next_pred = model.predict(last_features)[0]
        future_predictions.append(next_pred)
        last_features = np.roll(last_features, -1)
        last_features[0, 0] = next_pred

    return future_predictions


def forecast_with_prophet_arima_xgboost(ticker, periods=60):
    """Train Prophet, ARIMA, and XGBoost models and forecast future stock prices."""
    data = download_stock_data(ticker)
    X, y = prepare_data_for_xgboost(data)
    xgb_model = train_xgboost_model(X, y)
    xgb_forecast = forecast_with_xgboost(xgb_model, X, periods)

    future_dates = pd.date_range(start=data.index[-1], periods=periods + 1, freq='D')[1:]

    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label='Historical Data', color='black')
    plt.plot(future_dates, xgb_forecast, label='XGBoost Forecast', linestyle='dashed', color='purple')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.title(f'Forecast for {ticker} with XGBoost')
    plt.legend()
    plt.show()


# Usage example
if __name__ == "__main__":
    ticker = input("Enter the stock ticker: ").strip().upper()
    forecast_with_prophet_arima_xgboost(ticker)