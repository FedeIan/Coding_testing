import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam


# === FUNZIONI PER INDICATORI ===

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def calculate_macd(df):
    short_ema = df['Close'].ewm(span=12, adjust=False).mean()
    long_ema = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = short_ema - long_ema
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()


def calculate_bollinger_bands(df, window=20):
    rolling_mean = df['Close'].rolling(window=window).mean()
    rolling_std = df['Close'].rolling(window=window).std()
    df['Upper_Band'] = rolling_mean + 2 * rolling_std
    df['Lower_Band'] = rolling_mean - 2 * rolling_std


def calculate_stochastic_oscillator(df, window=14):
    df['%K'] = 100 * ((df['Close'] - df['Low'].rolling(window).min()) /
                      (df['High'].rolling(window).max() - df['Low'].rolling(window).min()))
    df['%D'] = df['%K'].rolling(3).mean()


def calculate_atr(df, window=14):
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift(1))
    low_close = np.abs(df['Low'] - df['Close'].shift(1))
    tr = high_low.combine(high_close, max).combine(low_close, max)
    df['ATR'] = tr.rolling(window=window).mean()


def calculate_moving_averages(df):
    df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()


# === FUNZIONE PRINCIPALE PER PREPARARE I DATI ===

def prepare_data_with_advanced_indicators(ticker, period, interval):
    df = yf.download(ticker, period=period, interval=interval)

    if df.empty:
        raise ValueError("Nessun dato disponibile per il ticker richiesto.")

    # Calcolo degli indicatori
    df['RSI'] = calculate_rsi(df['Close'])
    calculate_macd(df)
    calculate_bollinger_bands(df)
    calculate_stochastic_oscillator(df)
    calculate_atr(df)
    calculate_moving_averages(df)

    # Altri indicatori e feature
    df['Returns'] = np.log(df['Close'] / df['Close'].shift(1))
    df['Volatility'] = df['Returns'].rolling(window=10).std()
    df['Momentum'] = df['Close'] / df['Close'].shift(5)
    df['Distance_to_High'] = (df['High'] - df['Close']) / df['High']
    df['Distance_to_Low'] = (df['Close'] - df['Low']) / df['Low']
    df['Target'] = ((df['High'].shift(-10) >= df['High']) |
                    (df['Low'].shift(-10) <= df['Low'])).astype(int)

    print("Dati prima del dropna:", df.shape)
    df = df.dropna()  # Rimuove valori NaN
    if df.empty:
        raise ValueError("Dopo il preprocessing, il dataset è vuoto. Prova con un altro periodo o intervallo.")
    print("Dati dopo il dropna:", df.shape)

    features = ['RSI', 'MACD', 'Signal', 'Upper_Band', 'Lower_Band', '%K', '%D', 'ATR', 'EMA_20', 'SMA_50',
                'Returns', 'Volatility', 'Momentum', 'Distance_to_High', 'Distance_to_Low']
    X = df[features].values
    y = df['Target'].values

    return X, y, df


# === ESECUZIONE ===

if __name__ == "__main__":
    ticker = "AAPL"  # Sostituisci con il tuo simbolo
    period = "1mo"
    interval = "1h"

    # Prepara i dati con gli indicatori avanzati
    X, y, df = prepare_data_with_advanced_indicators(ticker, period, interval)

    # Normalizza i dati
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Split dei dati
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Costruzione del modello
    model = Sequential([
        Input(shape=(X_train.shape[1],)),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dropout(0.3),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

    print("=== Addestramento del modello ===")
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=1)

    print("=== Previsioni ===")
    last_data = df.iloc[-1][['RSI', 'MACD', 'Signal', 'Upper_Band', 'Lower_Band', '%K', '%D', 'ATR', 'EMA_20',
                             'SMA_50', 'Returns', 'Volatility', 'Momentum', 'Distance_to_High', 'Distance_to_Low']].values
    last_data_scaled = scaler.transform([last_data])
    future_prob = model.predict(last_data_scaled)[0][0]

    print(f"Probabilità di movimento significativo: {future_prob:.2%}")