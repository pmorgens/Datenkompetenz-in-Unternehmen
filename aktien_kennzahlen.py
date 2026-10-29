"""
Holt Fundamentalkennzahlen für 5 Unternehmen von Yahoo Finance (über yfinance).

Installation:
    pip install yfinance pandas openpyxl

Nutzung:
    1. TICKERS unten anpassen (Yahoo-Ticker, z. B. "SAP.DE" für Frankfurt/Xetra).
    2. python aktien_kennzahlen.py
"""

import pandas as pd
import yfinance as yf

# --------------------------------------------------------------------------
# Hier deine 5 Unternehmen eintragen (Beispiele, bitte ersetzen)
# --------------------------------------------------------------------------
TICKERS = ["AAPL", "MSFT", "SAP", "NVDA", "KO"]

# Anzeigename -> Feldname in yfinance (Ticker.info)
KENNZAHLEN = {
    "Forward P/E (erw. KGV)":          "forwardPE",
    "PEG Ratio":                       "trailingPegRatio",   # Fallback: pegRatio
    "EV/EBITDA":                       "enterpriseToEbitda",
    "Price/Book (KBV)":                "priceToBook",
    "Price/Sales (KUV)":               "priceToSalesTrailing12Months",
    "Profit Margin":                   "profitMargins",
    "Operating Margin":                "operatingMargins",
    "ROE (Return on Equity)":          "returnOnEquity",
    "ROA (Return on Assets)":          "returnOnAssets",
    "Quarterly Revenue Growth (YoY)":  "revenueGrowth",
    "Quarterly Earnings Growth (YoY)": "earningsQuarterlyGrowth",
    "Total Debt/Equity (in %)":        "debtToEquity",
    "Current Ratio":                   "currentRatio",
    "Free Cashflow (Näherung Levered FCF)": "freeCashflow",
    "Dividend Yield":                  "dividendYield",
    "Payout Ratio":                    "payoutRatio",
    "Beta":                            "beta",
    "Analyst Price Target (Mittel)":    "targetMeanPrice",
}

# Fallback-Felder, falls das Hauptfeld bei Yahoo leer ist
FALLBACKS = {
    "trailingPegRatio": "pegRatio",
    "earningsQuarterlyGrowth": "earningsGrowth",
}


def hole_kennzahlen(ticker: str) -> dict:
    """Gibt ein Dict mit allen Kennzahlen für einen Ticker zurück."""
    try:
        info = yf.Ticker(ticker).info
    except Exception as e:  # Netzwerk, Rate-Limit, unbekannter Ticker ...
        print(f"[Fehler] {ticker}: {e}")
        return {name: None for name in KENNZAHLEN}

    zeile = {}
    for name, feld in KENNZAHLEN.items():
        wert = info.get(feld)
        if wert is None and feld in FALLBACKS:
            wert = info.get(FALLBACKS[feld])
        zeile[name] = wert
    return zeile


def main() -> None:
    daten = {t: hole_kennzahlen(t) for t in TICKERS}
    df = pd.DataFrame(daten)  # Zeilen = Kennzahlen, Spalten = Unternehmen

    pd.set_option("display.width", 200)
    pd.set_option("display.float_format", lambda x: f"{x:,.4f}")
    print(df)

    df.to_csv("aktien_kennzahlen.csv", encoding="utf-8-sig")
    df.to_excel("aktien_kennzahlen.xlsx")
    print("\nGespeichert: aktien_kennzahlen.csv und aktien_kennzahlen.xlsx")


if __name__ == "__main__":
    main()
