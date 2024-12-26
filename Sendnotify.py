import yfinance as yf
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from datetime import datetime
import time

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

# Calcola i livelli di supporto e resistenza
def calculate_support_resistance(df, window=5):
    """Calcola i livelli di supporto e resistenza usando massimi e minimi locali."""
    resistance = df['High'][df['High'] == df['High'].rolling(window, center=True).max()].dropna()
    support = df['Low'][df['Low'] == df['Low'].rolling(window, center=True).min()].dropna()
    return resistance.values.tolist(), support.values.tolist()

# Monitoraggio di supporti e resistenze
def monitor_stock_with_levels(ticker, interval_minutes=5, window=5):
    print(f"Inizio monitoraggio del titolo {ticker} ogni {interval_minutes} minuti...")
    while True:
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="1d", interval="1m")  # Dati a intervallo di 1 minuto
            if data.empty:
                print("Nessun dato disponibile.")
                continue

            # Calcolo dei livelli
            resistance, support = calculate_support_resistance(data, window)
            current_price = data['Close'].iloc[-1]

            # Notifica per livelli di supporto
            for level in support:
                if abs(current_price - level) / level <= 0.01:  # Tolleranza del 1%
                    send_email(
                        subject=f"Supporto raggiunto: {level:.2f}",
                        body=f"Il prezzo attuale è {current_price:.2f}, vicino al supporto {level:.2f}."
                    )

            # Notifica per livelli di resistenza
            for level in resistance:
                if abs(current_price - level) / level <= 0.01:  # Tolleranza del 1%
                    send_email(
                        subject=f"Resistenza raggiunta: {level:.2f}",
                        body=f"Il prezzo attuale è {current_price:.2f}, vicino alla resistenza {level:.2f}."
                    )

            print(f"Monitoraggio aggiornato alle {datetime.now()}: prezzo attuale {current_price:.2f}")
            time.sleep(interval_minutes * 60)  # Aspetta per il prossimo monitoraggio

        except KeyboardInterrupt:
            print("Monitoraggio interrotto manualmente.")
            break
        except Exception as e:
            print(f"Errore: {e}")
            time.sleep(60)  # Aspetta 1 minuto prima di riprovare in caso di errore

# Esegui il monitoraggio
if __name__ == "__main__":
    ticker = "AAPL"  # Sostituisci con il simbolo del titolo che vuoi monitorare
    monitor_stock_with_levels(ticker=ticker, interval_minutes=5, window=5)