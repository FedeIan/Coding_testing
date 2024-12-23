import yfinance as yf
import numpy as np
import random
import pandas as pd


def fetch_market_data(symbol, start_date, end_date):
    # Scarica i dati storici
    data = yf.download(symbol, start=start_date, end=end_date)

    # Verifica se il DataFrame è vuoto
    if data.empty:
        raise ValueError("Nessun dato trovato per il simbolo specificato o intervallo di date.")

    # Calcola gli indicatori tecnici
    try:
        data['Short_MA'] = data['Close'].rolling(window=5).mean()  # Media mobile breve
        data['Long_MA'] = data['Close'].rolling(window=20).mean()  # Media mobile lunga
        data['RSI'] = 100 - (100 / (1 + (data['Close'].diff(1).clip(lower=0).rolling(window=14).mean() /
                                         abs(data['Close'].diff(1)).rolling(window=14).mean())))
    except Exception as e:
        raise ValueError(f"Errore durante il calcolo degli indicatori tecnici: {e}")

    # Controlla la presenza delle colonne create
    required_columns = ['Short_MA', 'Long_MA', 'RSI']
    for col in required_columns:
        if col not in data.columns:
            raise ValueError(f"Colonna mancante nel DataFrame: {col}")

    # Rimuove righe con valori mancanti
    data = data.dropna(subset=required_columns)

    # Verifica finale
    if data.empty:
        raise ValueError("Tutti i dati sono stati rimossi dopo il calcolo degli indicatori tecnici.")

    return data


# Funzione per determinare lo stato del mercato
def get_market_state(row):
    # Estrai i valori scalari dalla riga
    short_ma = row['Short_MA']
    long_ma = row['Long_MA']
    rsi = row['RSI']

    # Controllo e assegnazione dello stato
    if short_ma > long_ma and rsi > 70:
        return 'bull'  # Mercato rialzista
    elif short_ma < long_ma and rsi < 30:
        return 'bear'  # Mercato ribassista
    else:
        return 'neutral'  # Mercato neutrale


# Definizione dell'MDP
states = ["bull", "bear", "neutral"]
actions = ["buy", "sell", "hold"]
rewards = {
    "bull": {"buy": 10, "sell": -5, "hold": 1},
    "bear": {"buy": -10, "sell": 10, "hold": 2},
    "neutral": {"buy": 1, "sell": 1, "hold": 0},
}

transition_matrix = {
    "bull": {"bull": 0.6, "neutral": 0.3, "bear": 0.1},
    "bear": {"bull": 0.2, "neutral": 0.4, "bear": 0.4},
    "neutral": {"bull": 0.4, "neutral": 0.4, "bear": 0.2},
}

# Inizializzazione della Q-Table
q_table = {state: {action: 0 for action in actions} for state in states}
learning_rate = 0.1
discount_factor = 0.9


# Funzione per scegliere un'azione
def choose_action(state, q_table):
    if random.uniform(0, 1) < 0.1:  # Esplorazione
        return random.choice(actions)
    else:  # Sfruttamento
        return max(q_table[state], key=q_table[state].get)


# Simulazione dell'MDP con i dati reali
def train_mdp(data, episodes=1000):
    global q_table
    # Calcola lo stato per ogni riga del DataFrame
    data['State'] = data.apply(get_market_state, axis=1)

    for episode in range(episodes):
        state = random.choice(states)  # Stato iniziale casuale
        for step in range(len(data)):
            # Usa i dati reali per definire il prossimo stato
            row = data.iloc[step]
            current_state = row['State']
            action = choose_action(current_state, q_table)
            reward = rewards[current_state][action]

            # Passaggio allo stato successivo (simulato)
            next_state = np.random.choice(states, p=list(transition_matrix[current_state].values()))

            # Aggiorna la Q-Table
            best_next_action = max(q_table[next_state], key=q_table[next_state].get)
            q_table[current_state][action] += learning_rate * (
                    reward + discount_factor * q_table[next_state][best_next_action] - q_table[current_state][action]
            )
    return q_table


# Test dell'algoritmo
if __name__ == "__main__":
    try:
        # Parametri del test
        symbol = "TSLA"
        start_date = "2020-01-01"
        end_date = "2024-12-31"

        # Scarica e prepara i dati di mercato
        market_data = fetch_market_data(symbol, start_date, end_date)

        # Addestra l'MDP con i dati di mercato
        q_table_trained = train_mdp(market_data)

        # Stampa la Q-Table
        print("Q-Table Finale:")
        for state, actions in q_table_trained.items():
            print(f"{state}: {actions}")
    except ValueError as e:
        print(f"Errore durante l'esecuzione: {e}")