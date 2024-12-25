import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Bidirectional, Input
from datetime import datetime
import matplotlib.pyplot as plt


class StockPricePredictorWithFeatures:
    def __init__(self, ticker, start_date, end_date=None, lookback=60):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date if end_date else datetime.today().strftime('%Y-%m-%d')
        self.lookback = lookback
        self.data = None
        self.scaler = None
        self.model = None

    def fetch_data(self):
        # Scarica i dati da Yahoo Finance
        data = yf.download(self.ticker, start=self.start_date, end=self.end_date)

        # Calcola la media mobile semplice (SMA) e altre feature
        data['SMA_20'] = data['Adj Close'].rolling(window=20).mean().squeeze()
        data['EMA_20'] = data['Adj Close'].ewm(span=20, adjust=False).mean().squeeze()
        data['RSI'] = self.calculate_rsi(data['Adj Close'])

        # Calcolo robusto delle Bande di Bollinger
        rolling_std = data['Adj Close'].rolling(window=20).std().squeeze()
        data['Bollinger_Upper'] = data['SMA_20'] + 2 * rolling_std
        data['Bollinger_Lower'] = data['SMA_20'] - 2 * rolling_std

        # Altre feature
        data['Spread'] = data['High'] - data['Low']
        data['Momentum'] = data['Adj Close'] - data['Adj Close'].shift(10)
        data['Volatility'] = rolling_std
        data['OBV'] = self.calculate_obv(data['Adj Close'], data['Volume'])
        data['Day_of_Week'] = data.index.dayofweek
        data['Month'] = data.index.month

        # Debug: stampa i risultati intermedi
        print(f"Calcolo SMA_20:\n{data['SMA_20'].head()}")
        print(f"Calcolo rolling_std:\n{rolling_std.head()}")
        print(f"Bollinger Upper:\n{data['Bollinger_Upper'].head()}")

        # Rimuove eventuali valori NaN
        self.data = data.dropna()
        print(f"Dati scaricati e arricchiti:\n{self.data.head()}")

    def calculate_rsi(self, series, period=14):
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def calculate_obv(self, close, volume):
        obv = (np.sign(close.diff()) * volume).fillna(0).cumsum()
        return obv

    def prepare_data(self):
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = self.scaler.fit_transform(self.data)
        X, y = [], []
        for i in range(self.lookback, len(scaled_data)):
            X.append(scaled_data[i - self.lookback:i, :])
            y.append(scaled_data[i, 0])  # 'Adj Close' come output target
        X = np.array(X)
        y = np.array(y)
        train_size = int(len(X) * 0.8)
        self.X_train, self.X_test = X[:train_size], X[train_size:]
        self.y_train, self.y_test = y[:train_size], y[train_size:]
        print("Dati preparati per il modello.")

    def build_model(self):
        self.model = Sequential()
        self.model.add(Input(shape=(self.X_train.shape[1], self.X_train.shape[2])))
        self.model.add(Bidirectional(LSTM(units=50, return_sequences=True)))
        self.model.add(Bidirectional(LSTM(units=50)))
        self.model.add(Dense(units=1))
        self.model.compile(optimizer='adam', loss='mean_squared_error')
        print("Modello costruito.")

    def train_model(self, epochs=20, batch_size=32):
        self.model.fit(self.X_train, self.y_train, epochs=epochs, batch_size=batch_size,
                       validation_data=(self.X_test, self.y_test), verbose=1)
        print("Modello addestrato.")

    def evaluate_model(self):
        # Previsione dei prezzi
        predictions = self.model.predict(self.X_test)
        predictions = self.scaler.inverse_transform(
            np.hstack([predictions, np.zeros((len(predictions), self.X_test.shape[2] - 1))])
        )[:, 0]
        true_prices = self.scaler.inverse_transform(
            np.hstack([self.y_test.reshape(-1, 1), np.zeros((len(self.y_test), self.X_test.shape[2] - 1))])
        )[:, 0]
        test_dates = self.data.index[self.lookback + len(self.X_train):]

        # Ultimo prezzo di chiusura
        last_close_price = float(self.data['Adj Close'].iloc[-1])

        # Creazione del grafico
        plt.figure(figsize=(12, 6))
        plt.plot(test_dates, true_prices, color='blue', label='True Prices')
        plt.plot(test_dates, predictions, color='red', label='Predicted Prices')
        plt.axhline(last_close_price, color='green', linestyle='--', label=f'Last Close: {last_close_price:.2f}')
        plt.text(test_dates[-1], last_close_price, f'{last_close_price:.2f}', color='green', fontsize=10, va='center')

        # Titoli e legende
        plt.title(f'True vs Predicted Prices for {self.ticker}')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    ticker = input("Inserisci il ticker dell'azione (es. TSLA, NVDA): ").strip().upper()
    try:
        epochs = int(input("Inserisci il numero di epoch per l'addestramento: ").strip())
    except ValueError:
        print("Input non valido. Impostazione predefinita: 20 epoch.")
        epochs = 20

    # Inizializza il predittore
    predictor = StockPricePredictorWithFeatures(ticker=ticker, start_date="2015-01-01")
    predictor.fetch_data()
    predictor.prepare_data()
    predictor.build_model()
    predictor.train_model(epochs=epochs, batch_size=32)
    predictor.evaluate_model()
