import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Bidirectional, LSTM
import matplotlib.pyplot as plt


# 1. Scarica i dati storici del titolo
def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

ticker = 'RGTI'
start_date = '2020-01-01'
end_date = '2024-11-28'
data = get_stock_data(ticker, start_date, end_date)

# 2. Preprocessing dei dati
close_prices = data['Close'].values.reshape(-1, 1)

# Normalizza i dati
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(close_prices)

# Definisci i parametri per le sequenze
sequence_length = 60  # Numero di giorni da utilizzare per prevedere il giorno successivo
X = []
y = []

# Crea le sequenze temporali
for i in range(sequence_length, len(scaled_data)):
    X.append(scaled_data[i-sequence_length:i, 0])
    y.append(scaled_data[i, 0])

# Converti in array numpy e ridimensiona per LSTM
X = np.array(X)
y = np.array(y)
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# 3. Costruzione del modello LSTM bidirezionale
model = Sequential()
model.add(Bidirectional(LSTM(units=50, return_sequences=True), input_shape=(X.shape[1], 1)))
model.add(Bidirectional(LSTM(units=50)))
model.add(Dense(1))

# Compilazione del modello
model.compile(optimizer='adam', loss='mean_squared_error')

# 4. Addestramento del modello
model.fit(X, y, epochs=50, batch_size=32)

# 5. Previsione dei valori futuri
def predict_future(model, last_sequence, scaler, days_to_predict=30):
    predictions = []
    sequence = last_sequence

    for _ in range(days_to_predict):
        pred = model.predict(sequence.reshape(1, sequence.shape[0], 1))
        predictions.append(pred[0, 0])
        sequence = np.append(sequence[1:], pred, axis=0)

    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    return predictions

# Prepara l'ultima sequenza dai dati di training
last_sequence = X[-1]
future_predictions = predict_future(model, last_sequence, scaler, days_to_predict=30)

# 6. Visualizzazione dei risultati
plt.figure(figsize=(12, 6))
plt.plot(data.index[-len(y):], scaler.inverse_transform(y.reshape(-1, 1)), label="Dati storici", color="blue")
future_dates = [data.index[-1] + pd.Timedelta(days=i) for i in range(1, 31)]
plt.plot(future_dates, future_predictions, label="Previsioni future", color="orange")
plt.legend()
plt.title(f"Previsioni dei prezzi per {ticker}")
plt.xlabel("Date")
plt.ylabel("Prezzo")
plt.show()
