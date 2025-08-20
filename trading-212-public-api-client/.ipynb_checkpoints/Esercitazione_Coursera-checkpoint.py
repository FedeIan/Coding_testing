import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import ipywidgets as widgets
from IPython.display import display
import datetime

# === STEP 1: Scarica dati storici ===
def get_data(ticker="AAPL", start="2022-01-01", end="2024-01-01"):
    print(f"Scarico dati storici per il ticker: {ticker}...")
    try:
        start_date_obj = datetime.datetime.strptime(start, '%Y-%m-%d').date()
        end_date_obj = datetime.datetime.strptime(end, '%Y-%m-%d').date()
        df = yf.download(ticker, start=start_date_obj, end=end_date_obj, auto_adjust=True, progress=False)
        if df.empty:
            print(f"Errore: Nessun dato trovato per il ticker {ticker}.")
            return None
        print("Dati scaricati con successo.")
        return df["Close"]
    except Exception as e:
        print(f"Errore durante lo scaricamento dei dati: {e}")
        return None

# === STEP 2: Applica FFT ===
def apply_fft(prices, keep_components=10):
    n = len(prices)
    if n < 2:
        print("Errore FFT: servono almeno 2 dati.")
        return None, None, None

    fft_vals = np.fft.fft(prices.values)
    fft_freqs = np.fft.fftfreq(n)
    fft_filtered = np.copy(fft_vals)

    magnitudes = np.abs(fft_vals)
    sorted_indices_positive_freqs = np.argsort(magnitudes[1:n//2+1])[::-1] + 1

    indices_to_zero = set(range(1, n))
    if n % 2 == 0:
        indices_to_zero.discard(n//2)

    for i in range(min(keep_components, len(sorted_indices_positive_freqs))):
        idx = sorted_indices_positive_freqs[i]
        indices_to_zero.discard(idx)
        sym_idx = n - idx
        if sym_idx in indices_to_zero:
            indices_to_zero.discard(sym_idx)

    fft_filtered[list(indices_to_zero)] = 0
    reconstructed = np.fft.ifft(fft_filtered).real
    return reconstructed, fft_vals, fft_filtered

# === STEP 3: Previsione ===
def forecast(prices, fft_filtered, days_ahead=30):
    n = len(prices)
    n_extended = n + days_ahead
    fft_extended_filtered = np.zeros(n_extended, dtype=complex)

    original_n = len(fft_filtered)
    for i in range(original_n):
        if fft_filtered[i] != 0:
            fft_extended_filtered[i] = fft_filtered[i]
            sym_idx_extended = n_extended - i
            if i != 0 and sym_idx_extended < n_extended and sym_idx_extended >= 0:
                fft_extended_filtered[sym_idx_extended] = fft_filtered[original_n - i]

    projected_signal = np.fft.ifft(fft_extended_filtered).real
    return projected_signal

# === MAIN ===
def run_fft_forecast(ticker, start_date="2022-01-01", end_date="2024-01-01",
                     num_components=10, forecast_days=30):
    close_prices = get_data(ticker, start=start_date, end=end_date)
    if close_prices is None or close_prices.empty:
        print("Impossibile procedere.")
        return

    print(f"Dati caricati: {len(close_prices)} giorni da {close_prices.index.min().strftime('%Y-%m-%d')} a {close_prices.index.max().strftime('%Y-%m-%d')}")
    reconstructed_full, fft_vals, fft_filtered = apply_fft(close_prices, keep_components=num_components)
    if reconstructed_full is None:
        print("Errore durante la ricostruzione.")
        return

    projected_full = forecast(close_prices, fft_filtered, days_ahead=forecast_days)
    if projected_full is None:
        print("Errore durante la previsione.")
        return

    # === Ricostruisci l'indice temporale ===
    projected_full = np.asarray(projected_full).flatten()
    full_dates_index = pd.date_range(start=close_prices.index[0], periods=len(projected_full), freq='D')
    projected_full_series = pd.Series(data=projected_full, index=full_dates_index)

    # === Sottoserie per plot ===
    historical_end = close_prices.index[-1]
    historical_reconstruction = projected_full_series.loc[close_prices.index]
    forecast_dates_index = projected_full_series.loc[historical_end + pd.Timedelta(days=1):].index
    forecast_series = projected_full_series.loc[forecast_dates_index]

    # === Plot ===
    plt.figure(figsize=(14, 7))
    plt.plot(close_prices.index, close_prices.values, label="Prezzo Originale", alpha=0.8)
    plt.plot(historical_reconstruction.index, historical_reconstruction.values,
             label="Ricostruzione FFT", linestyle='--', color='green')
    plt.plot(forecast_series.index, forecast_series.values,
             label="Previsione FFT", linestyle='--', color='red')
    plt.axvline(x=historical_end, color='gray', linestyle=':', label='Fine Dati Storici')
    plt.title(f"Previsione Prezzi {ticker} con FFT")
    plt.xlabel("Data")
    plt.ylabel("Prezzo di Chiusura")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# === WIDGET INTERATTIVO ===
ticker_input = widgets.Text(value='AAPL', placeholder='Ticker (es. AAPL)', description='Ticker:')
start_date_input = widgets.Text(value='2022-01-01', description='Data Inizio:')
end_date_input = widgets.Text(value='2024-01-01', description='Data Fine:')
num_components_input = widgets.IntSlider(value=16, min=1, max=50, description='Componenti FFT:')
forecast_days_input = widgets.IntSlider(value=30, min=1, max=180, description='Giorni Previsione:')
run_button = widgets.Button(description="Esegui Previsione FFT")

def on_button_click(b):
    try:
        run_fft_forecast(
            ticker_input.value.upper(),
            start_date_input.value,
            end_date_input.value,
            num_components_input.value,
            forecast_days_input.value
        )
    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")

run_button.on_click(on_button_click)

# Mostra i widget
print("Inserisci i parametri per la previsione FFT:")
display(ticker_input, start_date_input, end_date_input, num_components_input, forecast_days_input, run_button)
