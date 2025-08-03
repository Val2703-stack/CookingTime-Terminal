from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

def fetch_bank_trades_auto(email, password):
    LOGIN_URL = "https://access.primemarket-terminal.com/"
    DASHBOARD_URL = "https://access.primemarket-terminal.com/prime-dashboard?template=bank-trades#"

    options = Options()
    # options.add_argument("--headless")  # Décommente pour mode invisible
    driver = webdriver.Chrome(options=options)

    # Aller à la page de login
    driver.get(LOGIN_URL)
    time.sleep(2)

    # Remplir les champs login
    driver.find_element(By.NAME, "Email").send_keys(email)
    driver.find_element(By.NAME, "Password").send_keys(password)
    # Coche la case "Stay logged in" si besoin
    try:
        driver.find_element(By.NAME, "KeepLoggedIn").click()
    except Exception:
        pass

    # Clique sur le bouton login
    driver.find_element(By.ID, "btnLogin").click()
    time.sleep(5)  # attendre chargement/redirection

    # Va sur la page Bank Trades
    driver.get(DASHBOARD_URL)
    time.sleep(5)  # attendre que la table se charge

    trades = []
    rows = driver.find_elements(By.CSS_SELECTOR, "table.TableBankTrades tbody tr")
    for row in rows:
        trades.append({
            "Banque": row.get_attribute("data-name-of-bank"),
            "Type": row.get_attribute("data-order-type"),
            "Paire": row.get_attribute("data-currency"),
            "Date": row.get_attribute("data-trade-date"),
            "Prix entrée": row.get_attribute("data-trade-entry"),
            "Stop Loss": row.get_attribute("data-trade-stop-loss"),
            "Take Profit": row.get_attribute("data-trade-take-profit"),
            "Statut": row.get_attribute("data-trade-status"),
        })
    driver.quit()
    return pd.DataFrame(trades)

import streamlit as st
import pandas as pd

st.title("Section Bank Trade (auto login + scraping)")

EMAIL = st.text_input("Email", type="default")
PASSWORD = st.text_input("Mot de passe", type="password")

if st.button("Rafraîchir les Bank Trades"):
    if EMAIL and PASSWORD:
        with st.spinner("Connexion et récupération en cours..."):
            df = fetch_bank_trades_auto(EMAIL, PASSWORD)
            st.success("Données récupérées !")
            st.dataframe(df)
    else:
        st.warning("Merci de renseigner email et mot de passe.")
