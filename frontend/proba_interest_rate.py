import streamlit as st
import requests
from bs4 import BeautifulSoup

def display():
    URL = "https://www.investing.com/central-banks/fed-rate-monitor"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    def get_soup(url):
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        return BeautifulSoup(r.text, "lxml")

    @st.cache_data(ttl=1800)
    def scrape_data():
        soup = get_soup(URL)
        fed_monitor = scrape_fed_monitor(soup)
        central_banks = scrape_central_banks(soup)
        return fed_monitor, central_banks

    def scrape_fed_monitor(soup):
        fed_info = {}
        fed_box = soup.find("div", id="fedMonitorBoxData")
        if not fed_box:
            return fed_info
        # Date de la réunion
        date_elem = fed_box.find("span", string="Meeting Time:")
        fed_info["meeting_time"] = date_elem.find_next("i").get_text(strip=True) if date_elem else ""
        # Prix future (si dispo)
        price_elem = fed_box.find("span", string="Future Price:")
        fed_info["future_price"] = price_elem.find_next("i").get_text(strip=True) if price_elem else ""
        # Probabilités de taux
        fed_info["rates"] = []
        for item in fed_box.find_all("div", class_="percfedRateItem"):
            spans = item.find_all("span")
            if len(spans) == 2:
                fed_info["rates"].append({
                    "range": spans[0].get_text(strip=True),
                    "probability": spans[1].get_text(strip=True)
                })
        return fed_info

    def scrape_central_banks(soup):
        cb_list = []
        table = soup.find("table", class_="centralBankSideBlockTbl")
        if not table:
            return cb_list
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) >= 5:
                name = cells[2].get_text(strip=True)
                rate = cells[3].get_text(strip=True)
                next_meeting = cells[4].get_text(strip=True)
                cb_list.append({
                    "name": name,
                    "rate": rate,
                    "next_meeting": next_meeting
                })
        return cb_list

    st.title("📊 Central Banks Dashboard")

    fed_monitor, central_banks = scrape_data()

    # --- FED MONITOR ---
    st.header("🇺🇸 Fed Monitor Tool")
    if fed_monitor:
        st.markdown(f"**Prochaine réunion** : {fed_monitor.get('meeting_time', 'N/A')}")
        if fed_monitor.get("future_price"):
            st.markdown(f"**Prix du future** : {fed_monitor['future_price']}")
        if fed_monitor.get("rates"):
            st.subheader("Probabilités de taux (%)")
            st.table([{ "Range": r["range"], "Probabilité": r["probability"] } for r in fed_monitor["rates"]])
    else:
        st.warning("Données Fed Monitor non disponibles.")

    # --- TABLE BANQUES CENTRALES ---
    st.header("🏦 Banques Centrales (Global)")
    if central_banks:
        st.subheader("Tableau récapitulatif")
        st.dataframe(central_banks, use_container_width=True)
    else:
        st.warning("Table des banques centrales non disponible.")

    st.caption("Données extraites de Investing.com • Refresh auto toutes les 30min.")
