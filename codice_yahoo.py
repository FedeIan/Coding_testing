import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score
import sys
import numpy as np


def wait_for_keypress():
    print("Premi un tasto per chiudere il programma...")
    sys.stdin.read(1)


def prepare_data(ticker, period, interval):
    data = yf.download(ticker, period=period, interval=interval)
    if data.empty:
        raise ValueError("Nessun dato disponibile per il ticker specificato.")
    return data


def calculate_rsi(close_prices, window=14):
    delta = close_prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=window).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def calculate_stochastic(data, k_window=14, d_window=3):
    high_column = data['High']
    low_column = data['Low']
    close_column = data['Close']
    lowest_low = low_column.rolling(window=k_window).min()
    highest_high = high_column.rolling(window=k_window).max()
    k_percent = 100 * (close_column - lowest_low) / (highest_high - lowest_low)
    d_percent = k_percent.rolling(window=d_window).mean()
    return k_percent, d_percent


def calculate_williams_r(data, window=14):
    high_column = data['High']
    low_column = data['Low']
    close_column = data['Close']
    highest_high = high_column.rolling(window=window).max()
    lowest_low = low_column.rolling(window=window).min()
    return -100 * (highest_high - close_column) / (highest_high - lowest_low)


def calculate_cci(data, window=20):
    tp = (data['High'] + data['Low'] + data['Close']) / 3
    sma = tp.rolling(window=window).mean()
    mad = (tp - sma).abs().rolling(window=window).mean()
    return (tp - sma) / (0.015 * mad)


def calculate_adx(data, window=14):
    high, low, close = data['High'], data['Low'], data['Close']
    plus_dm = high.diff()
    minus_dm = low.diff()

    plus_dm = np.where((plus_dm > minus_dm) & (plus_dm > 0), plus_dm, 0)
    minus_dm = np.where((minus_dm > plus_dm) & (minus_dm > 0), minus_dm, 0)

    tr = pd.concat([high - low, abs(high - close.shift()), abs(low - close.shift())], axis=1).max(axis=1)
    atr = tr.rolling(window=window).mean()

    plus_di = 100 * pd.Series(plus_dm.flatten(), index=data.index).rolling(window=window).mean() / atr
    minus_di = 100 * pd.Series(minus_dm.flatten(), index=data.index).rolling(window=window).mean() / atr

    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
    adx = dx.rolling(window=window).mean()

    return adx


def calculate_vwap(data):
    return (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()


def main():
    ticker = input("Inserisci il ticker: ").strip().upper()
    period = input("Periodo [Consigliato: 5y]: ").strip() or "5y"
    interval = input("Intervallo [Consigliato: 1h]: ").strip() or "1d"

    data = prepare_data(ticker, period, interval)
    print("Dati scaricati:", data.shape)  # Debugging

    if data.empty:
        print("Errore: Nessun dato disponibile.")
        sys.exit(1)

    data['RSI'] = calculate_rsi(data['Close'])
    data['Stoch_K'], data['Stoch_D'] = calculate_stochastic(data)
    data['Williams_R'] = calculate_williams_r(data)
    data['CCI'] = calculate_cci(data)
    data['ADX'] = calculate_adx(data)
    data['VWAP'] = calculate_vwap(data)

    data.dropna(inplace=True)
    print("Dati dopo il dropna:", data.shape)  # Debugging

    if data.empty:
        print("Errore: Nessun dato dopo la pulizia.")
        sys.exit(1)

    data['Target'] = (data['Close'].shift(-1) > data['Close']).astype(int)

    features = ['RSI', 'Stoch_K', 'Stoch_D', 'Williams_R', 'CCI', 'ADX', 'VWAP']
    X, y = data[features], data['Target']

    if X.empty or y.empty:
        print("Errore: Dataset vuoto dopo il pre-processing.")
        sys.exit(1)

    if len(y) < 2:
        print("Errore: Troppi pochi dati per il training.")
        sys.exit(1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    param_dist = {
        'n_estimators': [100, 200, 300, 500, 1000],
        'max_depth': [3, 5, 10, 20, None],
        'max_features': ['sqrt', 'log2', None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 5, 10],
        'bootstrap': [True, False]
    }

    random_search = RandomizedSearchCV(
        RandomForestClassifier(class_weight='balanced', random_state=42),
        param_distributions=param_dist,
        n_iter=20,
        cv=5,
        n_jobs=-1,
        random_state=42
    )

    random_search.fit(X_train, y_train)
    model = random_search.best_estimator_
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred) * 100

    latest_features = X.iloc[-1:]
    latest_prediction = model.predict(latest_features)
    direction = "Salirà" if latest_prediction[0] == 1 else "Scenderà"

    print(f"Previsione: {direction}")
    print(f"Accuratezza del modello: {accuracy:.2f}%")
    print(f"Migliori parametri trovati: {random_search.best_params_}")

    wait_for_keypress()
    sys.exit()


if __name__ == "__main__":
    main()
