import yfinance as yf
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
from scipy.stats import norm

# === CONFIGURAZIONE ===
TICKER = "SIDU"  # Ticker del mercato
INTERVAL = "30m"  # Intervallo di 15 minuti
PERIOD = "5d"  # Periodo massimo per dati intraday a 15 minuti

# === FUNZIONI ===

# 1. Ottenere dati di mercato da Yahoo Finance
def get_market_data(ticker, period="5d", interval="30m"):
    try:
        df = yf.download(ticker, period=period, interval=interval)

        # Appiattire le colonne se multi-indice
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]

        # Gestione dati mancanti
        df = df.dropna()
        return df
    except Exception as e:
        print(f"Errore nel download dei dati: {e}")
        return pd.DataFrame()

# 2. Identificare i livelli di supporto e resistenza
def calculate_levels(df):
    if len(df) < 2:
        raise ValueError("Dati insufficienti per calcolare i livelli.")

    highs = df['High'].values
    lows = df['Low'].values

    peaks, _ = find_peaks(highs, distance=2)  # Resistenze
    valleys, _ = find_peaks(-lows, distance=2)  # Supporti

    resistenze = df['High'].iloc[peaks]
    supporti = df['Low'].iloc[valleys]

    return resistenze, supporti

# 3. Calcolo della probabilità con analisi statistica
def calculate_probability(df, livello):
    prezzi = df['Close']
    ultimo_prezzo = prezzi.iloc[-1]
    rendimenti = np.log(prezzi / prezzi.shift(1)).dropna()
    volatilita = rendimenti.std()

    distanza = np.log(livello / ultimo_prezzo)
    probabilita = 1 - norm.cdf(distanza, loc=0, scale=volatilita)
    return probabilita

# 4. Controllare i livelli e stampare notifiche
def check_price_levels(df, resistenze, supporti):
    prezzo_corrente = df['Close'].iloc[-1]
    for res in resistenze:
        probabilita = calculate_probability(df, res)
        if probabilita > 0.5:
            print(f"🔔 ATTENZIONE: Il prezzo ({prezzo_corrente:.2f}) ha una probabilità del {probabilita:.2%} di raggiungere la resistenza ({res:.2f})!")
    for sup in supporti:
        probabilita = calculate_probability(df, sup)
        if probabilita > 0.5:
            print(f"🔔 ATTENZIONE: Il prezzo ({prezzo_corrente:.2f}) ha una probabilità del {probabilita:.2%} di raggiungere il supporto ({sup:.2f})!")

# 5. Loop principale
def monitor_market():
    try:
        df = get_market_data(TICKER, period=PERIOD, interval=INTERVAL)
        if df.empty:
            print("Nessun dato disponibile per il ticker richiesto.")
            return
        resistenze, supporti = calculate_levels(df)
        check_price_levels(df, resistenze, supporti)
    except Exception as e:
        print(f"Errore: {e}")

# Avvia monitoraggio
if __name__ == "__main__":
    import time
    while True:
        monitor_market()
        time.sleep(60)  # Controlla ogni minuto