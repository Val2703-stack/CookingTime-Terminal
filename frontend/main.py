import streamlit as st

# --- Import des modules encapsulés ---
import dashboard_générale
import dashboard_sentiment
import app_cot
import economic_calendar
import proba_interest_rate

# --- Configuration globale ---
st.set_page_config(
    page_title="CookingTime Terminal",
    layout="wide",
    page_icon="📈"
)

# --- Barre latérale de navigation ---
st.sidebar.title("CookingTime Terminal🧑‍🍳")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard générale",
        "Sentiment retail",
        "COT Smart Money",
        "Calendrier économique",
        "Probabilités Banques Centrales",
    ],
    index=0
)

# --- Routing : chaque menu appelle la fonction display() du module correspondant ---
if menu == "Dashboard générale":
    dashboard_générale.display()

elif menu == "Sentiment retail":
    dashboard_sentiment.display()

elif menu == "COT Smart Money":
    app_cot.display()

elif menu == "Calendrier économique":
    economic_calendar.display()

elif menu == "Probabilités Banques Centrales":
    proba_interest_rate.display()

# --- Footer général ---
st.markdown("---")
st.caption("🚀 Fait maison, pour les copains.")
