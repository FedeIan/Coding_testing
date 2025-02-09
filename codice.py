import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score
import sys
import termios
import tty
import numpy as np

def wait_for_keypress():
    """Funzione per attendere la pressione di un tasto su macOS/Linux."""
    print("Premi un tasto per chiudere il programma...")
    sys.stdin.read(1)

# Funzione per scaricare i dati
def prepare_data(ticker, period, interval):
    data = yf.download(ticker, period=period, interval=interval)
    if data.empty:
        raise ValueError("Nessun dato disponibile per il ticker specificato.")
    return data

# Funzioni per calcolare indicatori tecnici
def calculate_bollinger_bands(data, window):
    close_column = [col for col in data.columns if 'Close' in col][0]
    sma = data[close_column].rolling(window=window).mean()
    std_dev = data[close_column].rolling(window=window).std()
    data['BB_Upper'] = sma + (std_dev * 2)
    data['BB_Lower'] = sma - (std_dev * 2)
    return data

def calculate_rsi(close_prices, window):
    delta = close_prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=window).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_sma(close_prices, window):
    return close_prices.rolling(window=window).mean()

def calculate_ema(close_prices, window):
    return close_prices.ewm(span=window, adjust=False).mean()

def calculate_atr(data, window=14):
    high_column = [col for col in data.columns if 'High' in col][0]
    low_column = [col for col in data.columns if 'Low' in col][0]
    close_column = [col for col in data.columns if 'Close' in col][0]
    high_low = data[high_column] - data[low_column]
    high_close = abs(data[high_column] - data[close_column].shift())
    low_close = abs(data[low_column] - data[close_column].shift())
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return true_range.rolling(window=window).mean()

def calculate_macd(close_prices, short_window=12, long_window=26, signal_window=9):
    short_ema = close_prices.ewm(span=short_window, adjust=False).mean()
    long_ema = close_prices.ewm(span=long_window, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    return macd, signal

def find_recent_levels(close_prices, lookback=20):
    """Calcola supporti e resistenze basati su minimi/massimi e conferme da medie mobili."""
    support, resistance = [], []
    for i in range(lookback, len(close_prices) - lookback):
        window = close_prices.iloc[i - lookback:i + lookback]
        local_min = float(window.min())
        local_max = float(window.max())
        current_value = float(close_prices.iloc[i])
        if current_value == local_min:
            support.append((close_prices.index[i], local_min))
        if current_value == local_max:
            resistance.append((close_prices.index[i], local_max))
    support_level = np.mean([s[1] for s in support]) if support else close_prices.min()
    resistance_level = np.mean([r[1] for r in resistance]) if resistance else close_prices.max()
    return support_level, resistance_level

def main():
    ticker = input("Inserisci il ticker (es. AAPL, TSLA, BTC-USD): ").strip().upper()
    period = input("Periodo (es. 1y, 6mo, max) [Consigliato: 5y]: ").strip() or "5y"
    interval = input("Intervallo (es. 1d, 1h, 15m) [Consigliato: 1h]: ").strip() or "1h"
    lookback = int(input("Lookback per supporto/resistenza (default 20) [Consigliato: 20]: ") or 20)
    data = prepare_data(ticker, period, interval)
    close_column = [col for col in data.columns if 'Close' in col][0]
    data['RSI'] = calculate_rsi(data[close_column], window=14)
    data['SMA'] = calculate_sma(data[close_column], window=20)
    data['EMA'] = calculate_ema(data[close_column], window=20)
    data['ATR'] = calculate_atr(data)
    data['MACD'], data['Signal'] = calculate_macd(data[close_column])
    data = calculate_bollinger_bands(data, window=20)
    support_level, resistance_level = find_recent_levels(data[close_column], lookback=lookback)
    data['Target'] = (data[close_column].shift(-1) > data[close_column]).astype(int)
    data = data.dropna()
    features = ['RSI', 'SMA', 'EMA', 'ATR', 'MACD', 'Signal', 'BB_Upper', 'BB_Lower']
    X, y = data[features], data['Target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    param_grid = {
        'n_estimators': [100, 200, 500],
        'max_depth': [5, 10, 20],
        'max_features': ['sqrt', 'log2']
    }
    grid_search = GridSearchCV(RandomForestClassifier(class_weight='balanced', random_state=42), param_grid, cv=5, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    model = grid_search.best_estimator_
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred) * 100
    latest_features = X.iloc[-1:]
    latest_prediction = model.predict(latest_features)
    direction = "Salirà" if latest_prediction[0] == 1 else "Scenderà"
    print(f"Previsione: {direction}")
    print(f"Accuratezza del modello: {accuracy:.2f}%")
    print(f"Migliori parametri trovati: {grid_search.best_params_}")
    wait_for_keypress()
    sys.exit()

if __name__ == "__main__":
    main()
