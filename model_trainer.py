# Importazioni necessarie
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Bidirectional, Dense, Dropout, Input
import tensorflow as tf
import random
import os


class StockPricePredictor:
    def __init__(self, ticker, start_date, end_date=None, lookback=60):
        """
        Inizializza il modello con i parametri di configurazione.

        :param ticker: Simbolo del ticker (es. "TSLA").
        :param start_date: Data di inizio (formato "YYYY-MM-DD").
        :param end_date: Data di fine (formato "YYYY-MM-DD", opzionale).
        :param lookback: Finestra temporale per il modello (default: 60).
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date if end_date else datetime.today().strftime('%Y-%m-%d')
        self.lookback = lookback
        self.data = None
        self.scaler = None
        self.model = None
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

    def fetch_data(self):
        """Scarica i dati da Yahoo Finance."""
        self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        if self.data.empty:
            raise ValueError(f"Nessun dato trovato per il ticker {self.ticker} tra {self.start_date} e {self.end_date}")
        print(f"Dati scaricati:\n{self.data.head()}")
        self.data = self.calculate_technical_indicators(self.data)

    def calculate_technical_indicators(self, data):
        """Calcola indicatori tecnici."""
        data['SMA_20'] = data['Adj Close'].rolling(window=20).mean()
        data['EMA_20'] = data['Adj Close'].ewm(span=20, adjust=False).mean()
        # RSI
        delta = data['Adj Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
        return data

    def prepare_data(self):
        """Prepara i dati per il modello LSTM."""
        if self.data is None:
            raise ValueError("I dati non sono stati scaricati. Chiama fetch_data() prima di prepare_data().")

        # Normalizza i dati con MinMaxScaler
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = self.scaler.fit_transform(self.data[['Adj Close']])

        # Creazione di input (X) e output (y)
        X, y = [], []
        for i in range(self.lookback, len(scaled_data)):
            X.append(scaled_data[i - self.lookback:i, 0])  # Finestra temporale
            y.append(scaled_data[i, 0])  # Valore target

        X = np.array(X)
        y = np.array(y)

        # Ridimensiona X per adattarlo al formato richiesto da LSTM
        X = X.reshape((X.shape[0], X.shape[1], 1))

        # Dividi i dati in training e test (80%-20%)
        train_size = int(len(X) * 0.8)
        self.X_train, self.X_test = X[:train_size], X[train_size:]
        self.y_train, self.y_test = y[:train_size], y[train_size:]

        print(f"Dati preparati: {len(self.X_train)} per il training, {len(self.X_test)} per il test.")

    def build_model(self, lstm_units=50, lstm_layers=2, dropout_rate=0.2, learning_rate=0.001):
        """Costruisce un modello LSTM."""
        self.model = Sequential()
        self.model.add(Input(shape=(self.X_train.shape[1], self.X_train.shape[2])))

        for _ in range(lstm_layers):
            self.model.add(Bidirectional(LSTM(units=lstm_units, return_sequences=True)))
            self.model.add(Dropout(rate=dropout_rate))

        self.model.add(Bidirectional(LSTM(units=lstm_units)))
        self.model.add(Dense(units=1))

        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        self.model.compile(optimizer=optimizer, loss='mean_squared_error')
        print("Modello costruito.")

    def train_until_threshold(self, max_epochs=50, batch_size=32, threshold=0.2):
        """Addestra il modello fino a raggiungere la soglia."""
        self.model.fit(self.X_train, self.y_train, epochs=max_epochs, batch_size=batch_size,
                       validation_data=(self.X_test, self.y_test), verbose=1)


# Metodo Monte Carlo
def monte_carlo_simulation(ticker, start_date, end_date, num_simulations=50):
    """
    Simulazione Monte Carlo per trovare i migliori parametri.
    """
    best_params = None
    best_error = float('inf')
    best_model = None

    for simulation in range(num_simulations):
        # Genera parametri casuali
        lstm_units = random.randint(32, 256)
        lstm_layers = random.randint(1, 3)
        dropout_rate = random.uniform(0.1, 0.5)
        lookback = random.randint(30, 120)
        learning_rate = random.uniform(0.0001, 0.01)
        batch_size = random.choice([32, 64, 128])

        print(f"\nSimulazione {simulation + 1}/{num_simulations} con LSTM Units: {lstm_units}, Layers: {lstm_layers}, Dropout: {dropout_rate}, Lookback: {lookback}, Learning Rate: {learning_rate}, Batch Size: {batch_size}")

        predictor = StockPricePredictor(ticker, start_date, end_date, lookback)
        try:
            predictor.fetch_data()
            predictor.prepare_data()
            predictor.build_model(lstm_units, lstm_layers, dropout_rate, learning_rate)
            predictor.train_until_threshold(max_epochs=50, batch_size=batch_size)

            # Calcolo dell'errore
            predictions = predictor.model.predict(predictor.X_test)
            predictions = predictor.scaler.inverse_transform(predictions)
            true_prices = predictor.scaler.inverse_transform(predictor.y_test.reshape(-1, 1))
            error = np.mean(np.abs((true_prices - predictions) / true_prices)) * 100

            if error < best_error:
                best_error = error
                best_params = {
                    'lstm_units': lstm_units,
                    'lstm_layers': lstm_layers,
                    'dropout_rate': dropout_rate,
                    'lookback': lookback,
                    'learning_rate': learning_rate,
                    'batch_size': batch_size
                }
                best_model = predictor.model
        except Exception as e:
            print(f"Errore durante la simulazione: {e}")

    print(f"Miglior Errore: {best_error}, Parametri: {best_params}")
    return best_params, best_model


if __name__ == "__main__":
    ticker = "SOFI"
    start_date = "2015-01-01"
    end_date = "2024-12-01"
    monte_carlo_simulation(ticker, start_date, end_date, num_simulations=10)
    # Esegui la simulazione Monte Carlo
    best_params, best_model = monte_carlo_simulation(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        num_simulations=50
    )