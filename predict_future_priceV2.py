import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam


# === FUNZIONI PER SUPPORTI, RESISTENZE E INDICATORI ===

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def calculate_support_resistance(df, window=5):
    """
    Calcola i livelli di supporto e resistenza utilizzando massimi e minimi locali.
    """
    # Calcola i massimi e minimi locali
    rolling_max = df['High'].rolling(window, center=True).max()
    rolling_min = df['Low'].rolling(window, center=True).min()

    # Filtra i valori che corrispondono ai massimi e minimi locali
    resistance = df['High'][df['High'] == rolling_max].dropna()
    support = df['Low'][df['Low'] == rolling_min].dropna()


    # Appiattisci i risultati prima di convertirli in liste
    return resistance.values.flatten().tolist(), support.values.flatten().tolist()

def prepare_data_with_support_resistance(ticker, period, interval, rsi_window=7, window=5):
    df = yf.download(ticker, period=period, interval=interval)
    if df.empty:
        raise ValueError("Nessun dato disponibile per il ticker richiesto.")

    df['RSI'] = calculate_rsi(df['Close'], window=rsi_window)
    df['Returns'] = np.log(df['Close'] / df['Close'].shift(1))
    df['Volatility'] = df['Returns'].rolling(window=10).std()
    df['Momentum'] = df['Close'] / df['Close'].shift(5)
    df['Distance_to_High'] = (df['High'] - df['Close']) / df['High']
    df['Distance_to_Low'] = (df['Close'] - df['Low']) / df['Low']

    df['Target'] = ((df['High'].shift(-10) >= df['High']) |
                    (df['Low'].shift(-10) <= df['Low'])).astype(int)

    resistance, support = calculate_support_resistance(df, window=window)
    df = df.dropna()

    features = ['Returns', 'Volatility', 'Momentum', 'Distance_to_High', 'Distance_to_Low', 'RSI']
    X = df[features].values
    y = df['Target'].values

    return X, y, df, support, resistance


def build_mlp(input_dim):
    model = Sequential([
        Input(shape=(input_dim,)),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dropout(0.3),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
    return model






# === ESECUZIONE ===

if __name__ == "__main__":
    try:
        ticker = input("Inserisci il ticker (es: AAPL): ").strip()
        period = input("Inserisci il periodo (es: '1mo', '7d'): ").strip()
        interval = input("Inserisci l'intervallo (es: '15m', '1h', '1d'): ").strip()
        window = int(input("Inserisci la finestra per supporti e resistenze (es: 5): ").strip())

        # Prepara i dati
        X, y, df, support, resistance = prepare_data_with_support_resistance(ticker, period, interval, window=window)

        # Normalizza i dati
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        # Split dei dati
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Costruzione del modello
        model = build_mlp(X_train.shape[1])
        model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=1)

        # Prezzo attuale e livelli
        current_price = df['Close'].iloc[-1]
        grouped_support = calculate_support_resistance(df, window=5)[1]
        grouped_resistance = calculate_support_resistance(df, window=5)[0]

        print("\n=== Livelli ===")
        print("Supporti:", grouped_support)
        print("Resistenze:", grouped_resistance)

        # Calcolo probabilità
        probabilities = {
            "support": [{"level": level, "probability": 0.8} for level in grouped_support],
            "resistance": [{"level": level, "probability": 0.9} for level in grouped_resistance]
        }

    except Exception as e:
        print(f"Errore: {e}")