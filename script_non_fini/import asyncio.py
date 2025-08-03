import requests
from bs4 import BeautifulSoup
import yfinance as yf
from datetime import datetime
import re

def get_next_fomc_date():
    """
    Scrap la prochaine date de meeting FOMC sur Investing.com (bandeau Next FOMC Meeting)
    """
    url = "https://www.investing.com/central-banks/fed-rate-monitor"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    # Cherche le bandeau contenant la date
    # Exemple : <div ...>Next FOMC Meeting: Jul 31, 2024</div>
    for div in soup.find_all("div"):
        if div.text and "Next FOMC Meeting" in div.text:
            txt = div.text.strip()
            match = re.search(r"Next FOMC Meeting: ([A-Za-z]{3} \d{2}, \d{4})", txt)
            if match:
                date_str = match.group(1)
                return datetime.strptime(date_str, "%b %d, %Y").date()
    raise Exception("Impossible de trouver la prochaine date FOMC sur Investing.com (bandeau)")


def get_fedfunds_future_symbol(meeting_date):
    """
    Génère le symbole Yahoo Finance du future ZQ du mois du meeting
    """
    year = meeting_date.year
    month = meeting_date.month
    month_codes = "FGHJKMNQUVXZ"
    month_code = month_codes[month-1]
    year_code = str(year)[-2:]
    return f"ZQ{month_code}{year_code}.CBT"

def get_fedfunds_future_price(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="5d")
    if len(hist) == 0:
        raise Exception(f"Aucune donnée trouvée pour {symbol}")
    price = hist['Close'][-1]
    return price

def get_fed_rate_from_future(price):
    # Le future ZQ cote : prix = 100 - taux attendu
    return 100 - price

def get_current_fed_rate():
    """
    Récupère le taux cible FOMC actuel sur Investing.com
    """
    url = "https://www.investing.com/central-banks/fed-rate-monitor"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    # Cherche le taux dans l'encart principal (généralement .top bold)
    span = soup.find("span", class_="top bold")
    if span:
        txt = span.text
        val = re.findall(r"\d+\.\d+", txt)
        if val:
            return float(val[0])
    # Si structure change, fallback: hardcode ou lève une erreur
    raise Exception("Taux actuel introuvable sur Investing.com")

def calc_proba_move(future_rate, current_rate, move_size=0.25):
    # Proba de hausse ou baisse de 25bp, formule CME
    return (future_rate - current_rate) / move_size

def main():
    print("Recherche automatique de la prochaine réunion FOMC...")
    meeting_date = get_next_fomc_date()
    print(f"Prochaine date FOMC : {meeting_date}")

    symbol = get_fedfunds_future_symbol(meeting_date)
    print(f"Symbole du contrat future à utiliser (Yahoo) : {symbol}")

    price = get_fedfunds_future_price(symbol)
    future_rate = get_fed_rate_from_future(price)
    current_rate = get_current_fed_rate()

    print(f"Taux Fed actuel       : {current_rate:.2f}%")
    print(f"Taux attendu (future) : {future_rate:.2f}%")

    proba_hike = calc_proba_move(future_rate, current_rate)
    proba_hike = max(0, min(1, proba_hike))  # Clamp entre 0 et 1

    print(f"\nProbabilité HAUSSE +25bp : {proba_hike*100:.1f}%")
    print(f"Probabilité STATU QUO    : {100-proba_hike*100:.1f}%")

if __name__ == "__main__":
    main()
