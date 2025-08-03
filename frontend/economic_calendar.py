import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ----- TABLEAU DES TIMEZONES (valeur Investing.com : label affiché) -----
TIMEZONE_MAP = {
    "55": "Europe/Paris (UTC+2, heure d'été)", 
    "27": "UTC+0", 
    "43": "Europe/London (UTC+1, heure d'été)", 
    "87": "US/Eastern (UTC-4, NY)", 
    "91": "Asia/Tokyo (UTC+9, JP)", 
    "94": "Australia/Sydney (UTC+10)", 
    "122": "Europe/Moscow (UTC+3)", 
    "151": "Europe/Berlin (UTC+2)"
}
TIMEZONE_LIST = [f"{v} (id {k})" for k, v in TIMEZONE_MAP.items()]
DEFAULT_TZ_ID = "55"

def get_timezone_id_from_label(label):
    for tz_id, tz_label in TIMEZONE_MAP.items():
        if tz_label in label:
            return tz_id
    return DEFAULT_TZ_ID

def get_dates(period):
    today = datetime.now()
    if period == "Aujourd'hui":
        return today.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")
    elif period == "Hier":
        yest = today - timedelta(days=1)
        return yest.strftime("%Y-%m-%d"), yest.strftime("%Y-%m-%d")
    elif period == "Demain":
        tom = today + timedelta(days=1)
        return tom.strftime("%Y-%m-%d"), tom.strftime("%Y-%m-%d")
    elif period == "Cette semaine":
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
    elif period == "Semaine prochaine":
        start = today - timedelta(days=today.weekday()) + timedelta(days=7)
        end = start + timedelta(days=6)
        return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
    else:
        return today.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")

def investing_get_calendar(start_date, end_date, time_zone="55", lang="fr"):
    import requests
    from bs4 import BeautifulSoup
    url = "https://www.investing.com/economic-calendar/Service/getCalendarFilteredData"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.investing.com/economic-calendar/"
    }
    data = {
        "country[]": [],
        "importance[]": [],
        "category": "",
        "timeZone": time_zone,
        "timeFilter": "timeOnly",
        "dateFrom": start_date,
        "dateTo": end_date,
        "currentTab": "custom",
        "limit_from": 0
    }
    session = requests.Session()
    session.headers.update(headers)
    res = session.post(url, data=data)
    j = res.json()
    html = j['data']
    soup = BeautifulSoup(html, "lxml")
    rows = soup.find_all("tr", {"event_attr_id": True})
    events = []
    for row in rows:
        cells = row.find_all("td")
        if not cells or len(cells) < 7:
            continue
        heure = cells[0].get_text(strip=True)
        pays = cells[1].find("span", class_="flagCur").get("title", "") if cells[1].find("span", class_="flagCur") else cells[1].get_text(strip=True)
        importance = len(cells[2].find_all("i", class_="grayFullBullishIcon"))
        event = cells[3].get_text(strip=True)
        link = cells[3].find("a")
        url_event = "https://www.investing.com" + link.get('href') if link else ""
        actuel = cells[4].get_text(strip=True)
        consensus = cells[5].get_text(strip=True)
        precedent = cells[6].get_text(strip=True)
        date_event = ""
        if "data-event-datetime" in row.attrs:
            date_event = row["data-event-datetime"][:10]
        events.append({
            "Date": date_event,
            "Heure": heure,
            "Pays": pays,
            "Importance": importance,
            "Intitulé": event,
            "URL": url_event,
            "Prévision": consensus,
            "Précédent": precedent,
            "Chiffre publié": actuel,
        })
    return pd.DataFrame(events)

def display():
    st.title("📅 Calendrier Économique - Investing.com (Multi-période, UTC au choix, filtrage complet)")

    utc_label = st.selectbox("Fuseau horaire des horaires à afficher (UTC) :", TIMEZONE_LIST, index=0)
    tz_id = get_timezone_id_from_label(utc_label)

    PERIODES = [
        "Hier", "Aujourd'hui", "Demain", "Cette semaine", "Semaine prochaine"
    ]

    @st.cache_data(ttl=900)
    def get_calendar_multi(periods, time_zone):
        dfs = {}
        for period in periods:
            start, end = get_dates(period)
            df = investing_get_calendar(start, end, time_zone=time_zone, lang="fr")
            dfs[period] = df
        return dfs

    dfs = get_calendar_multi(PERIODES, tz_id)

    tabs = st.tabs(PERIODES)
    imp_map = {1:"⭐",2:"⭐⭐",3:"⭐⭐⭐"}
    majors = ['USD','EUR','GBP','JPY','CHF','AUD','CAD','NZD','CNY']

    def color_importance(val):
        if val=="⭐":
            return "background-color: #dbeafe;"
        if val=="⭐⭐":
            return "background-color: #fde68a;"
        if val=="⭐⭐⭐":
            return "background-color: #fecaca;"
        return ""
    def color_majors(val):
        return "color: #0ea5e9; font-weight:bold" if val in majors else ""

    def day_fr(d):
        for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
            try:
                dt = datetime.strptime(d, fmt)
                break
            except ValueError:
                continue
        else:
            return d
        mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
        jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        return f"{jours[dt.weekday()]} {dt.day} {mois[dt.month-1]} {dt.year}"

    for i, period in enumerate(PERIODES):
        with tabs[i]:
            df = dfs[period]
            if df.empty:
                st.warning("Aucun événement trouvé ou problème de scraping pour cette période.")
            else:
                df['ImportanceStr'] = df['Importance'].map(imp_map).fillna("")
                pays = st.multiselect(f"Filtrer par pays ({period}) :", options=sorted(df['Pays'].unique()), key=f"pays_{period}", default=[])
                importance = st.multiselect(f"Filtrer par importance ({period}) :", options=sorted(df['ImportanceStr'].unique()), key=f"imp_{period}", default=[])
                search = st.text_input(f"Filtrer par mot-clé/intitulé ({period}) :", key=f"search_{period}")

                df_filtered = df.copy()
                if pays:
                    df_filtered = df_filtered[df_filtered['Pays'].isin(pays)]
                if importance:
                    df_filtered = df_filtered[df_filtered['ImportanceStr'].isin(importance)]
                if search:
                    df_filtered = df_filtered[df_filtered['Intitulé'].str.contains(search, case=False, na=False)]

                # Nettoyage : on supprime les lignes avec date vide (optionnel, ou mieux : réparer)
                df_filtered = df_filtered[df_filtered["Date"].str.len() > 0]

                # Tri et affichage
                if "Date" in df_filtered.columns and len(df_filtered) > 0:
                    df_filtered = df_filtered.sort_values(by=["Date", "Heure"])
                    df_filtered["Label jour"] = df_filtered["Date"].apply(day_fr)
                    jours = df_filtered["Label jour"].unique()
                    for jour in jours:
                        st.markdown(f"### {jour}")
                        df_jour = df_filtered[df_filtered["Label jour"] == jour]
                        cols = ["Heure", "Pays", "ImportanceStr", "Intitulé", "Prévision", "Précédent", "Chiffre publié"]
                        df_show = df_jour[cols].rename(columns={"ImportanceStr":"Importance"})
                        st.dataframe(
                            df_show.style
                                .applymap(color_importance, subset=["Importance"])
                                .applymap(color_majors, subset=["Pays"]),
                            use_container_width=True,
                            height=400
                        )
                else:
                    st.warning("Aucun événement trouvé ou problème de scraping pour cette période.")

    st.caption("Scraping Investing.com | API cachée | 🇫🇷 FR | Usage personnel | Affichage multi-période, par jour, fuseau horaire personnalisable.")
