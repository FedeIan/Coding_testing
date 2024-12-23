import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
from matplotlib.dates import DateFormatter


# === FUNZIONI ===

# 1. Prepara i dati
def prepare_data(ticker, period, interval):
    # Scarica i dati
    df = yf.download(ticker, period=period, interval=interval)

    # Verifica se ci sono dati
    if df.empty:
        raise ValueError("Nessun dato disponibile per il ticker richiesto.")

    # Calcola feature tecniche
    df['Returns'] = np.log(df['Close'] / df['Close'].shift(1))
    df['Volatility'] = df['Returns'].rolling(window=10).std()
    df['Momentum'] = df['Close'] / df['Close'].shift(5)
    df['Distance_to_High'] = (df['High'] - df['Close']) / df['High']
    df['Distance_to_Low'] = (df['Close'] - df['Low']) / df['Low']
    df['RSI'] = 100 - (100 / (1 + df['Close'].pct_change().rolling(14).mean() /
                              df['Close'].pct_change().rolling(14).std()))

    # Creazione del target: raggiunto livello massimo o minimo
    df['Target'] = ((df['High'].shift(-10) >= df['High']) |
                    (df['Low'].shift(-10) <= df['Low'])).astype(int)

    # Elimina righe con valori mancanti
    print("Dati prima del dropna:", df.shape)
    df = df.dropna()
    print("Dati dopo il dropna:", df.shape)

    # Verifica se il DataFrame è vuoto dopo la pulizia
    if df.empty:
        raise ValueError("Nessun dato disponibile dopo la pulizia dei dati.")

    # Seleziona feature e target
    features = ['Returns', 'Volatility', 'Momentum', 'Distance_to_High', 'Distance_to_Low', 'RSI']
    X = df[features].values
    y = df['Target'].values

    # Verifica se X è vuoto
    print("Contenuto di X prima della normalizzazione:", X)
    print("Shape di X:", X.shape)

    return X, y, df


# 2. Costruisci il modello MLP
def build_mlp(input_dim):
    model = Sequential()
    model.add(Input(shape=(input_dim,)))  # Definisce l'input
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(1, activation='sigmoid'))  # Output: probabilità
    model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
    return model


# 3. Addestra e valuta il modello
def train_and_evaluate(model, X_train, y_train, X_test, y_test):
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=1)
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Accuracy: {accuracy:.2%}")
    return model


# 4. Genera il grafico con data, ora e fuso orario
def plot_closing_prices(df_test):
    plt.figure(figsize=(12, 6))
    plt.plot(df_test['Date'], df_test['Close'], marker='o', label='Prezzo di chiusura')
    plt.title('Prezzo di chiusura nel tempo')
    plt.xlabel('Data e ora')
    plt.ylabel('Prezzo di chiusura ($)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.legend()

    # Formatta asse X per mostrare data, ora e fuso orario
    date_formatter = DateFormatter('%Y-%m-%d %H:%M:%S%z')
    plt.gca().xaxis.set_major_formatter(date_formatter)

    plt.tight_layout()
    plt.show()


# 5. Input dell'utente
def get_user_input():
    ticker = input("Inserisci il ticker (es: AAPL): ").strip()
    period = input("Inserisci il periodo (es: 3mo, 6mo, 1y): ").strip()
    interval = input("Inserisci l'intervallo (es: 15m, 1h, 1d): ").strip()
    return ticker, period, interval


# === ESECUZIONE ===
if __name__ == "__main__":
    try:
        # Ottieni input dall'utente
        ticker, period, interval = get_user_input()

        # Prepara i dati
        X, y, df = prepare_data(ticker, period, interval)

        # Normalizza i dati
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        # Dividi i dati
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Costruisci e addestra il modello
        print("\n=== Addestramento del modello MLP ===")
        mlp_model = build_mlp(X_train.shape[1])
        mlp_model = train_and_evaluate(mlp_model, X_train, y_train, X_test, y_test)

        # Previsioni e output
        print("\n=== Previsioni ===")
        y_pred = mlp_model.predict(X_test)
        df_test = df.iloc[-len(y_test):].copy()
        df_test['Probability'] = y_pred
        df_test['Signal'] = (y_pred > 0.5).astype(int)

        # Converte l'indice in colonna per il grafico
        df_test['Date'] = df_test.index

        print(df_test[['Date', 'Close', 'High', 'Low', 'Probability', 'Signal']].tail(20))

        # Genera il grafico
        plot_closing_prices(df_test)

    except ValueError as e:
        print(f"Errore: {e}")