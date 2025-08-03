import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from streamlit_autorefresh import st_autorefresh

URL = "https://www.financialjuice.com/home"
REFRESH_SEC = 60  # évite de surcharger le site, rafraîchit toutes les 60s

st.set_page_config(page_title="FinancialJuice News Feed", layout="wide")
st.title("🟧 FinancialJuice News Feed quasi-live")

st_autorefresh(interval=REFRESH_SEC * 1000, key="refresh")

def get_news():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(URL)
    # Attends que les news apparaissent (max 10s)
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    news_items = []
    for item in soup.find_all("li", class_="news-item"):
        time_tag = item.find("span", class_="news-time")
        time = time_tag.text.strip() if time_tag else ""
        headline_tag = item.find("span", class_="news-headline")
        headline = headline_tag.text.strip() if headline_tag else item.text.strip()
        link = item.find("a", href=True)
        url = "https://www.financialjuice.com" + link["href"] if link else URL
        news_items.append({
            "time": time,
            "headline": headline,
            "url": url
        })
    return news_items

try:
    news_items = get_news()
    for news in news_items[:15]:
        st.markdown(f"**{news['time']}** – [{news['headline']}]({news['url']})")
        st.markdown("---")
except Exception as e:
    st.error(f"Erreur lors du scraping FinancialJuice : {e}")
