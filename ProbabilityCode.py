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
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import os

# === FUNZIONI ===

# 1. Prepara i dati
def prepare_data(ticker, period, interval):
    df = yf.download(ticker, period=period, interval=interval)
    if df.empty:
        raise ValueError("Nessun dato disponibile per il ticker richiesto.")

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

    features = ['Returns', 'Volatility', 'Momentum', 'Distance_to_High', 'Distance_to_Low', 'RSI']
    X = df[features].values
    y = df['Target'].values

    return X, y, df

# 2. Costruisci il modello MLP
def build_mlp(input_dim):
    model = Sequential()
    model.add(Input(shape=(input_dim,)))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
    return model

# 3. Addestra e valuta il modello
def train_and_evaluate(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=1)
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Accuracy: {accuracy:.2%}")
    return model

# 4. Genera grafico e salva in file
def plot_closing_prices(df_test, ticker):
    graph_path = f"{ticker}_price_chart.png"
    plt.figure(figsize=(12, 6))
    plt.plot(df_test['Date'], df_test['Close'], marker='o', label='Prezzo di chiusura')
    plt.title(f'Prezzo di chiusura per {ticker}')
    plt.xlabel('Data e ora')
    plt.ylabel('Prezzo di chiusura ($)')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.legend()

    date_formatter = DateFormatter('%Y-%m-%d %H:%M:%S%z')
    plt.gca().xaxis.set_major_formatter(date_formatter)

    plt.tight_layout()
    plt.savefig(graph_path)
    plt.close()
    return graph_path

# 5. Prepara il corpo dell'email con i dati disponibili
def prepare_email_body(df_test, ticker):
    # Debug: Stampa le colonne disponibili
    print("Colonne disponibili in df_test:", df_test.columns)

    # Prepara il corpo dell'email basandosi sulle colonne esistenti
    required_columns = ['Date', 'Close', 'Probability', 'Signal']
    available_columns = [col for col in required_columns if col in df_test.columns]

    if available_columns:
        email_body = f"Previsioni per {ticker}:\n{df_test[available_columns].tail(5)}"
    else:
        print("Le colonne richieste non sono presenti. Utilizzo tutte le colonne disponibili.")
        email_body = f"Previsioni per {ticker}:\n{df_test.tail(5)}"

    return email_body
# 6. Invia email con allegati
def send_email(subject, body, attachment_paths=[]):
    sender_email = "luifederico84@gmail.com"
    sender_password = "zmcy kyqg jeme hfyi"
    recipient_email = "luifederico84@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    for attachment_path in attachment_paths:
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.basename(attachment_path)}",
            )
            msg.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print("Email inviata con successo!")
    except Exception as e:
        print(f"Errore nell'invio dell'email: {e}")

# 7. Input dell'utente
def get_user_input():
    ticker = input("Inserisci il ticker (es: AAPL): ").strip()
    period = input("Inserisci il periodo (es: 3mo, 6mo, 1y): ").strip()
    interval = input("Inserisci l'intervallo (es: 15m, 1h, 1d): ").strip()
    return ticker, period, interval

# === ESECUZIONE ===
if __name__ == "__main__":
    try:
        ticker, period, interval = get_user_input()
        X, y, df = prepare_data(ticker, period, interval)

        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        print("\n=== Addestramento del modello MLP ===")
        mlp_model = build_mlp(X_train.shape[1])
        mlp_model = train_and_evaluate(mlp_model, X_train, y_train, X_test, y_test)

        print("\n=== Previsioni ===")
        y_pred = mlp_model.predict(X_test)
        df_test = df.iloc[-len(y_test):].copy()
        df_test['Probability'] = y_pred
        df_test['Signal'] = (y_pred > 0.5).astype(int)
        df_test['Date'] = df_test.index

        print(df_test[['Date', 'Close', 'High', 'Low', 'Probability', 'Signal']].tail(20))

        graph_path = plot_closing_prices(df_test, ticker)

        email_body = f"Previsioni per {ticker}:\n{df_test[['Date', 'Close', 'Probability', 'Signal']].tail(5)}"

    except ValueError as e:
        print(f"Errore: {e}")