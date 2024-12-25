import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam


# === FUNZIONI ===

def calculate_rsi(data, window=14):
    """
    Calcola l'RSI per una finestra temporale specifica.
    """
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_support_resistance(df, window=5):
    """
    Calcola i livelli di supporto e resistenza utilizzando massimi e minimi locali.
    """
    # Massimi e minimi locali
    resistance = df['High'][df['High'] == df['High'].rolling(window, center=True).max()].dropna()
    support = df['Low'][df['Low'] == df['Low'].rolling(window, center=True).min()].dropna()

    # Converti in liste piatte
    return resistance.values.flatten().tolist(), support.values.flatten().tolist()
def calculate_probability_for_levels(model, scaler, df, current_price, support, resistance):
    """
    Calcola la probabilità di raggiungere ciascun livello di supporto e resistenza.

    Args:
        model: Modello allenato.
        scaler: Scaler utilizzato per normalizzare i dati.
        df (pd.DataFrame): DataFrame con i dati di mercato.
        current_price (float): Prezzo attuale.
        support (list): Livelli di supporto.
        resistance (list): Livelli di resistenza.

    Returns:
        dict: Probabilità per supporti e resistenze.
    """
    # Ottieni l'ultima riga di dati come input per il modello
    last_data = df.iloc[-1][['Returns', 'Volatility', 'Momentum', 'Distance_to_High', 'Distance_to_Low', 'RSI']].values
    last_data_scaled = scaler.transform([last_data])

    # Prevedi la probabilità di un movimento significativo
    future_prob = model.predict(last_data_scaled)[0][0]

    # Calcola la probabilità relativa per ogni livello
    probabilities = {"support": [], "resistance": []}
    total_probability = 0  # Per calcolare la somma di tutte le probabilità

    for level in support:
        distance = abs(level - current_price)
        prob = future_prob * (1 / (1 + distance))  # Peso inverso alla distanza
        probabilities["support"].append({"level": level, "probability": prob})
        total_probability += prob

    for level in resistance:
        distance = abs(level - current_price)
        prob = future_prob * (1 / (1 + distance))  # Peso inverso alla distanza
        probabilities["resistance"].append({"level": level, "probability": prob})
        total_probability += prob

    # Normalizza le probabilità in modo che la somma sia 1 (100%)
    for category in ["support", "resistance"]:
        for prob_dict in probabilities[category]:
            prob_dict["probability"] /= total_probability

    return probabilities
def group_levels(levels, threshold=0.01):
    """
    Raggruppa livelli di supporto/resistenza vicini tra loro.
    """
    levels = sorted(levels)  # Ordina i livelli
    grouped = []
    current_group = [levels[0]]

    for level in levels[1:]:
        if abs(level - current_group[-1]) / level <= threshold:
            current_group.append(level)
        else:
            grouped.append(np.mean(current_group))
            current_group = [level]

    grouped.append(np.mean(current_group))  # Aggiungi l'ultimo gruppo
    return grouped


def find_nearest_levels(price, levels):
    """
    Trova i livelli di supporto/resistenza più vicini al prezzo attuale.

    Args:
        price (float): Prezzo attuale.
        levels (list): Lista di livelli di supporto o resistenza.

    Returns:
        list: Livelli ordinati per distanza dal prezzo.
    """
    if isinstance(price, pd.Series):  # Assicurati che il prezzo sia scalare
        price = price.item()
    return sorted(levels, key=lambda x: abs(x - price))


def prepare_data_with_support_resistance(ticker, period, interval, rsi_window=7, window=5):
    """
    Prepara i dati per il modello, calcolando RSI e supporti/resistenze.
    """
    if interval in ['1m', '5m', '15m', '30m', '1h']:
        if period not in ['1d', '5d', '7d', '1mo']:
            period = '7d'
            print(f"Periodo modificato a '{period}' per supportare l'intervallo '{interval}'.")

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

    print("Dati prima del dropna:", df.shape)
    df = df.dropna()  # Rimuove valori NaN
    if df.empty:
        raise ValueError("Dopo il preprocessing, il dataset è vuoto. Prova con un altro periodo o intervallo.")
    print("Dati dopo il dropna:", df.shape)

    features = ['Returns', 'Volatility', 'Momentum', 'Distance_to_High', 'Distance_to_Low', 'RSI']
    X = df[features].values
    y = df['Target'].values

    return X, y, df, support, resistance


def build_mlp(input_dim):
    """
    Costruisce un modello MLP per la classificazione binaria.
    """
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


def predict_future_price(model, df, scaler):
    """
    Prevede il livello massimo e minimo per i prossimi 30 minuti.
    """
    last_data = df.iloc[-1][['Returns', 'Volatility', 'Momentum', 'Distance_to_High', 'Distance_to_Low', 'RSI']].values
    last_data_scaled = scaler.transform([last_data])
    future_prob = model.predict(last_data_scaled)[0][0]
    current_close = df['Close'].iloc[-1].item()
    max_future_price = current_close * (1 + future_prob)
    min_future_price = current_close * (1 - future_prob)
    print(f"Probabilità di nuovo massimo/minimo: {future_prob:.2%}")
    print(f"Livello massimo stimato: {max_future_price:.2f} USD")
    print(f"Livello minimo stimato: {min_future_price:.2f} USD")
    return max_future_price, min_future_price


# === ESECUZIONE ===
if __name__ == "__main__":
    try:
        ticker = input("Inserisci il ticker (es: AAPL): ").strip()
        period = input("Inserisci il periodo (es: '1mo', '7d'): ").strip()
        interval = input("Inserisci l'intervallo (es: '15m', '1h', '1d'): ").strip()
        window = int(input("Inserisci la finestra per supporti e resistenze (es: 5): ").strip())

        X, y, df, support, resistance = prepare_data_with_support_resistance(ticker, period, interval, window=window)

        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        print("\n=== Addestramento del modello ===")
        mlp_model = build_mlp(X_train.shape[1])
        mlp_model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=1)

        print("\n=== Previsioni ===")
        predict_future_price(mlp_model, df, scaler)

        grouped_support = group_levels(support, threshold=0.01)
        grouped_resistance = group_levels(resistance, threshold=0.01)

        print("\n=== Supporti e Resistenze Raggruppati ===")
        print("Supporti:", grouped_support)
        print("Resistenze:", grouped_resistance)

        current_price = df['Close'].iloc[-1].item()  # Converte in un valore scalare float
        # Calcola i livelli più vicini
        nearest_support = find_nearest_levels(current_price, grouped_support)
        nearest_resistance = find_nearest_levels(current_price, grouped_resistance)

        print("\n=== Livelli Più Vicini al Prezzo Attuale ===")
        print("Prezzo Attuale:", current_price)
        print("Supporti Più Vicini:", nearest_support[:3])
        print("Resistenze Più Vicine:", nearest_resistance[:3])
        # Calcola le probabilità per ciascun livello
        probabilities = calculate_probability_for_levels(mlp_model, scaler, df, current_price, grouped_support,
                                                         grouped_resistance)
        print("\n=== Probabilità di Raggiungere Livelli Ordinati ===")

        # Ordina i supporti in base alla probabilità in ordine decrescente

        sorted_support = sorted(probabilities["support"], key=lambda x: x["probability"], reverse=True)
        print("Supporti:")
        for s in sorted_support:
            level = float(s['level'])
            probability = float(s['probability'])
            print(f"Livello: {level:.2f}, Probabilità: {probability:.2%}")

        # Ordina le resistenze in base alla probabilità in ordine decrescente
        sorted_resistance = sorted(probabilities["resistance"], key=lambda x: x["probability"], reverse=True)
        print("\nResistenze:")
        for r in sorted_resistance:
            level = float(r['level'])
            probability = float(r['probability'])
            print(f"Livello: {level:.2f}, Probabilità: {probability:.2%}")
    except ValueError as e:
            print(f"Errore: {e}")