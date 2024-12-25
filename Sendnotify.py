import yfinance as yf
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import time
from datetime import datetime

# Configura l'email
def send_email(subject, body):
    sender_email = "luifederico84@gmail.com"  # Sostituisci con il tuo indirizzo Gmail
    sender_password = "zmcy kyqg jeme hfyi"  # Sostituisci con la password per app generata
    recipient_email = "luifederico84@gmail.com"  # Email destinatario


    # Creazione del messaggio
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f"Email inviata con successo alle {datetime.now()}!")
    except Exception as e:
        print(f"Errore nell'invio dell'email: {e}")

# Leggi i dati da Yahoo Finance
def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="1m")  # Dati a intervallo di 1 minuto
        latest_data = data.tail(1)  # Prendi l'ultima riga
        last_close = latest_data['Close'].iloc[0]
        timestamp = latest_data.index[-1]
        return f"Dati per {ticker}:\nUltima chiusura: {last_close:.2f}\nTimestamp: {timestamp}"
    except Exception as e:
        return f"Errore durante il fetch dei dati: {e}"

# Monitoraggio e invio email ogni 5 minuti
def monitor_stock(ticker, interval_minutes=5):
    print(f"Inizio monitoraggio del titolo {ticker} ogni {interval_minutes} minuti...")
    while True:
        try:
            stock_data = fetch_stock_data(ticker)
            send_email(subject=f"Dati aggiornati per {ticker}", body=stock_data)
            print(f"Dati inviati alle {datetime.now()}:\n{stock_data}")
            time.sleep(interval_minutes * 60)  # Converti minuti in secondi
        except KeyboardInterrupt:
            print("Monitoraggio interrotto manualmente.")
            break
        except Exception as e:
            print(f"Errore: {e}")
            time.sleep(60)  # Aspetta 1 minuto prima di riprovare in caso di errore

# Esegui il monitoraggio
if __name__ == "__main__":
    ticker = "AAPL"  # Sostituisci con il simbolo del titolo che vuoi monitorare
    monitor_stock(ticker=ticker, interval_minutes=5)
