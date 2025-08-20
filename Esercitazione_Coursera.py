# -*- coding: utf-8 -*-
"""
Stagionalità per giorno dell'anno (DOY) da dati reali Yahoo Finance.
- Calcola per ogni (mese, giorno) la media, deviazione standard, N, P10, P90.
- Asse X = DOY (1..366). Niente anni "fittizi" nel grafico: solo un indice di calendario.
- Sovrappone uno o più anni specifici (Close) mappati su DOY.
- Salva sempre un PNG; opzionalmente salva un CSV con le statistiche.

Dipendenze: yfinance, pandas, matplotlib
"""

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import os
from typing import Iterable, Optional, List

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


# ---------- UTIL ----------

def _doy_from_md(month_series, day_series) -> pd.Series:
    """Calcola il Day-Of-Year (1..366) da (mese, giorno) usando il calendario 2000 (bisestile).
    Serve solo per mappare (mese, giorno) -> posizione nell'anno; i dati restano reali."""
    dates = pd.to_datetime(
        [f"2000-{int(m):02d}-{int(d):02d}" for m, d in zip(month_series, day_series)],
        errors="coerce"
    )
    # DatetimeIndex ha .dayofyear, Series richiede .dt.dayofyear
    if isinstance(dates, pd.DatetimeIndex):
        return pd.Series(dates.dayofyear, index=getattr(month_series, "index", None))
    return dates.dt.dayofyear


def _safe_close_series(df: pd.DataFrame) -> Optional[pd.Series]:
    """Ritorna una Series 1D dei prezzi di chiusura, robusta a differenze tra dataset."""
    if df is None or df.empty:
        return None
    close = df.get("Close", None)
    if close is None:
        close = df.get("Adj Close", None)
    if close is None:
        return None
    if isinstance(close, pd.DataFrame):  # es. multi-colonna
        if close.shape[1] == 0:
            return None
        close = close.iloc[:, 0]
    return pd.Series(close, index=df.index)


# ---------- CALCOLI ----------

def calcola_statistiche_stagionali(ticker: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """
    Scarica i dati e calcola statistiche per ogni (mese, giorno):
      - 'Prezzo Medio di Chiusura', 'STD', 'N', 'P10', 'P90', più 'DOY' (1..366) per il plot.
    Ritorna un DataFrame ordinato per DOY.
    """
    try:
        df = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)
        if df.empty:
            print(f"Non sono stati trovati dati per il ticker '{ticker}'.")
            return None

        df = df.copy()
        df["Mese"] = df.index.month
        df["Giorno"] = df.index.day

        grp = df.groupby(["Mese", "Giorno"])["Close"]
        stats = grp.apply(lambda s: pd.Series({
            "Prezzo Medio di Chiusura": float(s.mean()),
            "STD": float(s.std()) if len(s) > 1 else 0.0,
            "N": int(s.size),
            "P10": float(s.quantile(0.10)),
            "P90": float(s.quantile(0.90)),
        }))

        stats = stats.reset_index()  # Mese, Giorno tornano colonne
        stats["DOY"] = _doy_from_md(stats["Mese"], stats["Giorno"])
        stats = stats.dropna(subset=["DOY"]).astype({"DOY": "int32"}).sort_values("DOY").reset_index(drop=True)
        return stats

    except Exception as e:
        print(f"Si è verificato un errore: {e}")
        return None


def estrai_anno_su_doy(ticker: str, anno: int) -> Optional[pd.DataFrame]:
    """
    Scarica i Close dell'anno indicato e li mappa su DOY (1..366).
    Ritorna un DataFrame con colonne: 'DOY', f'Close_{anno}'.
    """
    start = f"{anno}-01-01"
    end = f"{anno+1}-01-01"
    df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
    if df.empty:
        return None

    close = _safe_close_series(df)
    if close is None or close.empty:
        return None

    mesi = df.index.month
    giorni = df.index.day
    doy = _doy_from_md(mesi, giorni)

    out = pd.DataFrame({"DOY": doy, f"Close_{anno}": close.values})
    out = out.dropna(subset=["DOY"]).astype({"DOY": "int32"}).sort_values("DOY").reset_index(drop=True)

    # In caso di più barre nello stesso DOY (raro), teniamo l'ultimo valore
    out = out.groupby("DOY", as_index=False).last()
    return out


# ---------- PLOT ----------

def plot_stagionalita(
    stats_df: pd.DataFrame,
    ticker: str,
    anni_overlay: Optional[Iterable[int]] = None,
    save_path: Optional[str] = None,
    show: bool = True,
    plot_bande: bool = True,
    usa_percentili: bool = True,
) -> str:
    """
    Plotta la stagionalità (asse X = DOY 1..366), con bande (P10–P90 o ±STD).
    Sovrappone opzionalmente uno o più anni (Close) mappati su DOY.
    Ritorna il percorso assoluto del PNG salvato.
    """
    if stats_df is None or stats_df.empty:
        raise ValueError("DataFrame delle statistiche vuoto: nulla da plottare.")

    x = stats_df["DOY"].to_numpy()
    y_mean = stats_df["Prezzo Medio di Chiusura"].to_numpy()

    if save_path is None:
        safe_ticker = str(ticker).replace("^", "").replace(".", "_").replace("/", "_")
        save_path = f"stagionalita_DOY_{safe_ticker}.png"

    fig = plt.figure()
    ax = fig.add_subplot(111)

    # Curva media
    ax.plot(x, y_mean, label="Media stagionale")

    # Bande
    if plot_bande:
        if usa_percentili and {"P10", "P90"}.issubset(stats_df.columns):
            ax.fill_between(x, stats_df["P10"].to_numpy(), stats_df["P90"].to_numpy(),
                            alpha=0.25, label="Banda 10°–90°")
        elif not usa_percentili and "STD" in stats_df.columns:
            upper = y_mean + stats_df["STD"].to_numpy()
            lower = y_mean - stats_df["STD"].to_numpy()
            ax.fill_between(x, lower, upper, alpha=0.25, label="Media ± 1 STD")

    # Overlay anni (se presenti)
    if anni_overlay:
        for anno in anni_overlay:
            overlay_df = estrai_anno_su_doy(ticker, anno)
            if overlay_df is None or overlay_df.empty:
                print(f"Nessun dato overlay per l'anno {anno} (skip).")
                continue
            col = f"Close_{anno}"
            overlay_series = overlay_df.set_index("DOY")[col]
            # Riallinea sui DOY della stagionalità
            y_overlay = pd.Series(index=stats_df["DOY"], dtype="float64")
            y_overlay.loc[overlay_series.index] = overlay_series.values
            ax.plot(x, y_overlay.to_numpy(), label=f"Close {anno}")

    # Tacche per inizio mese (calcolate su calendario 2000, solo per etichette)
    month_starts = pd.to_datetime([f"2000-{m:02d}-01" for m in range(1, 13)]).dayofyear.to_list()
    month_labels = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
    ax.set_xticks(month_starts)
    ax.set_xticklabels(month_labels, rotation=0)

    ax.set_title(f"{ticker} — Stagionalità (asse X = DOY 1..366)")
    ax.set_xlabel("Giorno dell'anno (DOY)")
    ax.set_ylabel("Prezzo")
    ax.grid(True, which="both", linestyle="--", alpha=0.35)
    ax.legend()
    fig.tight_layout()

    fig.savefig(save_path, dpi=150)
    abs_path = os.path.abspath(save_path)
    print(f"Grafico salvato in: {abs_path}")

    if show:
        try:
            plt.show(block=True)
        except Exception as e:
            print(f"Impossibile mostrare il grafico (verrà solo salvato). Errore: {e}")
    plt.close(fig)
    return abs_path


# ---------- MAIN ----------

if __name__ == "__main__":
    # Parametri
    ticker_simbolo = "BCH"      # esempi: '^GSPC', 'AAPL', 'FTSEMIB.MI', 'QUBT'
    data_inizio = "2019-01-01"
    data_fine = "2025-08-19"

    # Anni da sovrapporre (Close). Metti [] o None per nessun overlay.
    anni_overlay: List[int] = [2025]  # es. [2023, 2024, 2025]

    # Salvataggio CSV con le statistiche? (True/False)
    salva_csv = True
    csv_path = f"stagionalita_stats_{ticker_simbolo.replace('^','').replace('.','_').replace('/','_')}.csv"

    # Calcolo
    stats = calcola_statistiche_stagionali(ticker_simbolo, data_inizio, data_fine)

    if stats is not None:
        print(f"Righe calcolate: {len(stats)}")  # ~365/366

        # Salva CSV se richiesto
        if salva_csv:
            stats.to_csv(csv_path, index=False)
            print(f"Statistiche salvate in: {os.path.abspath(csv_path)}")

        # Plot
        plot_stagionalita(
            stats,
            ticker=ticker_simbolo,
            anni_overlay=anni_overlay,
            save_path=None,   # oppure un percorso personalizzato
            show=True,
            plot_bande=True,
            usa_percentili=True
        )
    else:
        print("Nessun dato da plottare.")
