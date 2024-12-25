
import yfinance as yf
import numpy as np
import pandas as pd

# === FUNZIONI ===

def prepare_data(ticker, period, interval):
    """
    Prepara i dati per il modello utilizzando parametri relativi come '1y' per il periodo
    e '1h' per l'intervallo temporale. Gestisce automaticamente i limiti di Yahoo Finance
    per i dati intraday.
    """
    # Limita automaticamente il periodo in base all'intervallo
    if interval in ['1m', '2m', '5m', '15m', '30m', '1h']:
        # Dati intraday sono disponibili solo per gli ultimi 60 giorni
        if period not in ['1d', '5d', '7d', '1mo', '2mo']:
            period = '7d'  # Limita automaticamente il periodo
            print(f"Periodo modificato a {period} per supportare l'intervallo '{interval}'.")

    # Scarica i dati utilizzando period e interval
    df = yf.download(ticker, period=period, interval=interval)
    if df.empty:
        raise ValueError("Nessun dato disponibile per il ticker richiesto.")

    # Calcoli aggiuntivi per le feature
    df['Returns'] = np.log(df['Close'] / df['Close'].shift(1))
    df['Volatility'] = df['Returns'].rolling(window=10).std()
    df['Momentum'] = df['Close'] / df['Close'].shift(5)
    df['Distance_to_High'] = (df['High'] - df['Close']) / df['High']
    df['Distance_to_Low'] = (df['Close'] - df['Low']) / df['Low']
    df['RSI'] = 100 - (100 / (1 + df['Close'].pct_change().rolling(14).mean() /
                              df['Close'].pct_change().rolling(14).std()))
    df['Target'] = ((df['High'].shift(-10) >= df['High']) |
                    (df['Low'].shift(-10) <= df['Low'])).astype(int)

    print("Dati prima del dropna:", df.shape)
    df = df.dropna()
    print("Dati dopo il dropna:", df.shape)

    # Seleziona le feature e i target
    features = ['Returns', 'Volatility', 'Momentum', 'Distance_to_High', 'Distance_to_Low', 'RSI']
    X = df[features].values
    y = df['Target'].values

    return X, y, df


def get_last_value(ticker, period='1d', interval='1d'):
    """
    Ottieni l'ultimo valore scaricato da Yahoo Finance per un dato ticker.
    
    Args:
        ticker (str): Il simbolo del titolo (es: 'AAPL').
        period (str): Periodo di dati da scaricare (es: '1d', '7d', '1mo').
        interval (str): Intervallo dei dati (es: '1d', '1h', '15m').
    
    Returns:
        dict: Un dizionario contenente la data, l'ultimo prezzo di chiusura, e altre informazioni.
    """
    try:
        # Scarica i dati da Yahoo Finance
        df = yf.download(ticker, period=period, interval=interval)
        if df.empty:
            raise ValueError("Nessun dato disponibile per il ticker richiesto.")

        # Ottieni l'ultimo record
        last_row = df.iloc[-1]
        last_date = df.index[-1]
        last_close = last_row['Close']
        
        # Costruisci un dizionario con le informazioni utili
        result = {
            'Date': last_date,
            'Close': last_close,
            'Open': last_row['Open'],
            'High': last_row['High'],
            'Low': last_row['Low'],
            'Volume': last_row['Volume']
        }
        
        return result
    except Exception as e:
        print(f"Errore: {e}")
        return None

# === ESECUZIONE ===
if __name__ == "__main__":
    try:
        # Input dell'utente
        ticker = input("Inserisci il ticker (es: AAPL): ").strip()
        period = input("Inserisci il periodo relativo (es: 1y, 7d, 1mo): ").strip()
        interval = input("Inserisci l'intervallo temporale (es: 1d, 1h, 15m): ").strip()

        # Prepara i dati
        X, y, df = prepare_data(ticker, period, interval)
        print("Ultimi 5 record del dataset:")
        print(df.tail())

        # Ottieni l'ultimo valore
        last_value = get_last_value(ticker, period=period, interval=interval)
        if last_value:
            print("Ultimo valore scaricato:")
            print(last_value)

    except ValueError as e:
        print(f"Errore: {e}")
