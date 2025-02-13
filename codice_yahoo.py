import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBClassifier
import talib as ta
from sklearn.metrics import accuracy_score

# 📌 Richiede input all'utente per Ticker, Periodo e Intervallo
ticker = input("Inserisci il ticker dell'azione (es. NEE): ").strip().upper()
period = input("Inserisci il periodo (es. 1y, 2y, 6mo, 5d): ").strip()
interval = input("Inserisci l'intervallo (es. 1h, 1d, 5m, 15m): ").strip()

# 📌 Scarica dati finanziari
def get_data(ticker, period, interval):
    try:
        data = yf.download(ticker, period=period, interval=interval)
        if data.empty:
            raise ValueError(f"Nessun dato disponibile per il ticker {ticker}.")
        return data
    except Exception as e:
        print(f"Errore nel download dei dati: {e}")
        return None

# 📌 Aggiunta indicatori tecnici
def add_indicators(data):
    data = data.dropna()

    # 📌 Assicuriamoci che i dati siano monodimensionali e numerici
    close_values = data["Close"].dropna().astype(float).values.ravel()
    high_values = data["High"].dropna().astype(float).values.ravel()
    low_values = data["Low"].dropna().astype(float).values.ravel()

    # 📌 Calcolo degli indicatori tecnici con input corretti
    data["RSI"] = ta.RSI(close_values, timeperiod=14)

    data["CCI"] = ta.CCI(high_values, low_values, close_values, timeperiod=14)

    data["VWAP"] = (data["Close"] * data["Volume"]).cumsum() / data["Volume"].cumsum()

    stoch_k, stoch_d = ta.STOCH(high_values, low_values, close_values)
    data["Stoch_K"], data["Stoch_D"] = stoch_k, stoch_d

    data["Williams_R"] = ta.WILLR(high_values, low_values, close_values, timeperiod=14)

    data["ADX"] = ta.ADX(high_values, low_values, close_values, timeperiod=14)

    data["ROC"] = ta.ROC(close_values, timeperiod=10)

    data["ATR"] = ta.ATR(high_values, low_values, close_values, timeperiod=14)

    macd, macd_signal, _ = ta.MACD(close_values)
    data["MACD"], data["MACD_signal"] = macd, macd_signal

    # 📌 Aggiunta di nuove feature per trend rialzisti
    data["SMA_50"] = ta.SMA(close_values, timeperiod=50)
    data["SMA_200"] = ta.SMA(close_values, timeperiod=200)
    data["Momentum"] = ta.MOM(close_values, timeperiod=10)

    # 📌 Aggiunta di Supporti e Resistenze
    data["Support"] = data["Low"].rolling(window=20).min()
    data["Resistance"] = data["High"].rolling(window=20).max()

    return data.dropna()


# 📌 Creazione etichetta target (0 = scenderà, 1 = salirà)
def create_target(data):
    data["Target"] = (data["Close"].shift(-1) > data["Close"]).astype(int)
    return data.dropna()

# 📌 Carica i dati e prepara il dataset
data = get_data(ticker, period, interval)

if data is not None:
    data = add_indicators(data)
    data = create_target(data)

    # 📌 Controllo bilanciamento classi
    print("🔍 Bilanciamento classi Target:")
    print(data["Target"].value_counts())

    # 📌 Selezione delle feature e target
    feature_cols = ["RSI", "CCI", "VWAP", "Stoch_K", "Stoch_D", "Williams_R", "ADX", "ROC", "ATR", "MACD", "Support", "Resistance", "SMA_50", "SMA_200", "Momentum"]
    X = data[feature_cols]
    y = data["Target"]

    # 📌 Split dei dati in training e test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 📌 Parametri da ottimizzare con GridSearchCV
    param_grid = {
        'n_estimators': [300, 500, 800, 1000],  # Aumentiamo il numero di alberi
        'max_depth': [3, 6, 10, 15],  # Testiamo modelli più profondi
        'learning_rate': [0.001, 0.005, 0.01, 0.03, 0.05, 0.1],  # Raffiniamo il learning rate
        'scale_pos_weight': [1, 2, 3, 5, 10]  # Aggiungiamo un valore più alto per gestire squilibri nelle classi
    }

    model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    grid_search = GridSearchCV(model, param_grid, cv=5, scoring="accuracy", verbose=1, n_jobs=-1)

    print("🔍 Ottimizzazione dei parametri in corso...")
    grid_search.fit(X_train, y_train)

    print(f"✅ Accuratezza migliorata: {accuracy_score(y_test, grid_search.best_estimator_.predict(X_test)) * 100:.2f}%")
