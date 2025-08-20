import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Ticker da analizzare (puoi cambiarlo es. TSLA, AAPL, ecc.)
ticker = "TSLA"

# Date degli earning (in formato stringa)
earnings_dates_str = [
    "2025-04-22", "2025-01-29", "2024-10-23", "2024-07-23", "2024-04-23",
    "2024-01-24", "2023-10-18", "2023-07-19", "2023-04-19", "2023-01-25",
    "2022-10-19", "2022-07-20", "2022-04-20", "2022-01-26", "2021-10-20",
    "2021-07-26", "2021-04-26", "2021-01-27", "2020-10-21", "2020-07-22",
    "2020-04-29", "2020-01-29", "2019-10-23", "2019-06-24", "2019-04-24",
    "2019-01-30", "2018-10-24", "2018-08-01", "2018-05-02", "2018-02-07",
    "2017-11-01", "2017-08-02", "2017-05-03", "2017-02-22"
]

# Converto in oggetti datetime
earnings_dates = [datetime.strptime(d, "%Y-%m-%d") for d in earnings_dates_str]

# Funzione per ottenere la candela di apertura del giorno post-earning
def get_post_earning_candle(ticker, earnings_dates):
    results = []

    for date in earnings_dates:
        post_date = date + timedelta(days=1)
        start = post_date.strftime('%Y-%m-%d')
        end = (post_date + timedelta(days=1)).strftime('%Y-%m-%d')

        # Scarica dati a 30 minuti
        try:
            data = yf.download(ticker, start=start, end=end, interval="30m", progress=False)
            data = data.between_time("09:30", "16:00")  # orario USA

            if not data.empty:
                first_candle = data.iloc[0]
                direction = "Positiva" if first_candle['Close'] > first_candle['Open'] else "Negativa"
                results.append({
                    "Data post-earning": post_date.strftime('%Y-%m-%d'),
                    "Ora": data.index[0].strftime('%H:%M'),
                    "Open": round(first_candle['Open'], 2),
                    "Close": round(first_candle['Close'], 2),
                    "Risultato": direction
                })
            else:
                results.append({
                    "Data post-earning": post_date.strftime('%Y-%m-%d'),
                    "Ora": "N/D",
                    "Open": "N/A",
                    "Close": "N/A",
                    "Risultato": "Dati mancanti"
                })

        except Exception as e:
            results.append({
                "Data post-earning": post_date.strftime('%Y-%m-%d'),
                "Errore": str(e)
            })

    return pd.DataFrame(results)

# Esecuzione
df_result = get_post_earning_candle(ticker, earnings_dates)

# Salva i risultati in un file Excel (opzionale)
df_result.to_excel(f"post_earnings_backtest_{ticker}.xlsx", index=False)

# Mostra il risultato
print(df_result)