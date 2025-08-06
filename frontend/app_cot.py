import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(CURRENT_DIR, "data", "cot_financial_full.csv")

@st.cache_data
def load_data(csv_path):
    if not os.path.exists(csv_path):
        st.error(f"Fichier non trouvé : {csv_path}")
        return None
    df = pd.read_csv(csv_path, dtype={'As_of_Date_In_Form_YYMMDD': str})
    df['Date'] = pd.to_datetime(df['As_of_Date_In_Form_YYMMDD'], format='%y%m%d')
    return df

df = load_data(CSV_PATH)

def format_number(x):
    if abs(x) >= 1_000_000:
        return f"{x/1_000_000:.1f}M"
    if abs(x) >= 1_000:
        return f"{x/1_000:.1f}K"
    return str(x)

def display(): 
    df = load_data(CSV_PATH)

    ASSET_CLASSES = {
    # FX (Devises)
    "AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE": "FX",
    "BRAZILIAN REAL - CHICAGO MERCANTILE EXCHANGE": "FX",
    "BRITISH POUND - CHICAGO MERCANTILE EXCHANGE": "FX",
    "CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE": "FX",
    "EURO FX - CHICAGO MERCANTILE EXCHANGE": "FX",
    "EURO FX/BRITISH POUND XRATE - CHICAGO MERCANTILE EXCHANGE": "FX",
    "JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE": "FX",
    "MEXICAN PESO - CHICAGO MERCANTILE EXCHANGE": "FX",
    "NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE": "FX",
    "SO AFRICAN RAND - CHICAGO MERCANTILE EXCHANGE": "FX",
    "SWISS FRANC - CHICAGO MERCANTILE EXCHANGE": "FX",
    "USD INDEX - ICE FUTURES U.S.": "FX",

    # Indices actions
    "S&P 500 Consolidated - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "S&P 500 ANNUAL DIVIDEND INDEX - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "S&P 500 QUARTERLY DIVIDEND IND - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "E-MINI S&P 500 - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "MICRO E-MINI S&P 500 INDEX - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "NASDAQ MINI - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "NASDAQ-100 Consolidated - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "MICRO E-MINI NASDAQ-100 INDEX - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "DJIA Consolidated - CHICAGO BOARD OF TRADE": "Indice",
    "DJIA x $5 - CHICAGO BOARD OF TRADE": "Indice",
    "MICRO E-MINI DJIA (x$0.5) - CHICAGO BOARD OF TRADE": "Indice",
    "RUSSELL E-MINI - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "MICRO E-MINI RUSSELL 2000 INDX - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "E-MINI S&P 400 STOCK INDEX - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "EMINI RUSSELL 1000 GROWTH - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "EMINI RUSSELL 1000 VALUE INDEX - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "NIKKEI STOCK AVERAGE - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "NIKKEI STOCK AVERAGE YEN DENOM - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "DOW JONES U.S. REAL ESTATE IDX - CHICAGO BOARD OF TRADE": "Indice",
    "BBG COMMODITY - CHICAGO BOARD OF TRADE": "Indice",
    "MSCI EAFE  - ICE FUTURES U.S.": "Indice",
    "MSCI EM INDEX - ICE FUTURES U.S.": "Indice",
    "VIX FUTURES - CBOE FUTURES EXCHANGE": "Indice",
    "RUSSELL 2000 ANNUAL DIVIDEND  - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "E-MINI S&P COMMUNICATION INDEX - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "E-MINI S&P CONSU STAPLES INDEX - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "E-MINI S&P ENERGY INDEX - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "E-MINI S&P FINANCIAL INDEX - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "E-MINI S&P HEALTH CARE INDEX - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "E-MINI S&P INDUSTRIAL INDEX - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "E-MINI S&P MATERIALS INDEX - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "E-MINI S&P TECHNOLOGY INDEX - CHICAGO MERCANTILE EXCHANGE": "Indice",
    "E-MINI S&P UTILITIES INDEX - CHICAGO MERCANTILE EXCHANGE": "Indice",

    # Bonds / Taux / Swaps
    "UST 2Y NOTE - CHICAGO BOARD OF TRADE": "Taux",
    "UST 5Y NOTE - CHICAGO BOARD OF TRADE": "Taux",
    "UST 10Y NOTE - CHICAGO BOARD OF TRADE": "Taux",
    "MICRO 10 YEAR YIELD - CHICAGO BOARD OF TRADE": "Taux",
    "UST BOND - CHICAGO BOARD OF TRADE": "Taux",
    "ULTRA UST 10Y - CHICAGO BOARD OF TRADE": "Taux",
    "ULTRA UST BOND - CHICAGO BOARD OF TRADE": "Taux",
    "2 YEAR ERIS SOFR SWAP - CHICAGO BOARD OF TRADE": "Taux",
    "5 YEAR ERIS SOFR SWAP - CHICAGO BOARD OF TRADE": "Taux",
    "10 YEAR ERIS SOFR SWAP - CHICAGO BOARD OF TRADE": "Taux",
    "FED FUNDS - CHICAGO BOARD OF TRADE": "Taux",
    "SOFR-1M - CHICAGO MERCANTILE EXCHANGE": "Taux",
    "SOFR-3M - CHICAGO MERCANTILE EXCHANGE": "Taux",
    "EURO SHORT TERM RATE - CHICAGO MERCANTILE EXCHANGE": "Taux",
    "ADJUSTED INT RATE S&P 500 TOTL - CHICAGO MERCANTILE EXCHANGE": "Taux",

    # Crypto / Tokens
    "BITCOIN - CHICAGO MERCANTILE EXCHANGE": "Crypto",
    "MICRO BITCOIN - CHICAGO MERCANTILE EXCHANGE": "Crypto",
    "Nano Bitcoin  - LMX LABS LLC": "Crypto",
    "ETHER CASH SETTLED - CHICAGO MERCANTILE EXCHANGE": "Crypto",
    "MICRO ETHER  - CHICAGO MERCANTILE EXCHANGE": "Crypto",
    "NANO ETHER - LMX LABS LLC": "Crypto",
    "DOGECOIN - LMX LABS LLC": "Crypto",
    "CARDONA - LMX LABS LLC": "Crypto",
    "LITECOIN CASH - LMX LABS LLC": "Crypto",
    "CHAINLINK - LMX LABS LLC": "Crypto",
    "AVALANCHE - LMX LABS LLC": "Crypto",
    "POLKADOT - LMX LABS LLC": "Crypto",
    "NANO SOLANA - LMX LABS LLC": "Crypto",
    "NANO STELLAR - LMX LABS LLC": "Crypto",
    "NANO XRP - LMX LABS LLC": "Crypto",
    "STELLAR - LMX LABS LLC": "Crypto",
    "1K SHIB - LMX LABS LLC": "Crypto",
    }

    st.title("COT Financial Futures – Smart Money Donut + Tableau évolution hebdo")

    df = load_data(CSV_PATH)
    if df is not None:
        df['Asset_Class'] = df['Market_and_Exchange_Names'].map(ASSET_CLASSES).fillna("Autre")
        famille_labels = {
            "FX": "Devises (FX)",
            "Indice": "Indices",
            "Taux": "Bonds\Taux\Swaps",
            "Crypto": "Crypto\Tokens",
            "Autre": "Autre"
        }
        order = ["FX", "Indice", "Taux", "Crypto", "Autre"]
        all_familles = df['Asset_Class'].unique().tolist()
        familles_sorted = [f for f in order if f in all_familles]
        selected_familles = st.multiselect(
            "Filtrer les actifs par classe d'actif (famille) :",
            options=[famille_labels[f] for f in familles_sorted],
            default=[famille_labels[f] for f in familles_sorted if f != "Autre"]
        )
        famille_map_inv = {v: k for k, v in famille_labels.items()}
        familles_cle = [famille_map_inv[v] for v in selected_familles]

        markets_filtered = (
            df[df['Asset_Class'].isin(familles_cle)][['Market_and_Exchange_Names', 'Asset_Class']]
            .drop_duplicates()
            .sort_values(['Asset_Class', 'Market_and_Exchange_Names'])
        )
        markets = markets_filtered['Market_and_Exchange_Names'].tolist()

        CATS = {
            "Dealer/Intermediary": {
                "long": "Dealer_Positions_Long_All",
                "short": "Dealer_Positions_Short_All",
                "net": "Net_Dealer"
            },
            "Asset Manager/Institutional": {
                "long": "Asset_Mgr_Positions_Long_All",
                "short": "Asset_Mgr_Positions_Short_All",
                "net": "Net_AssetManager"
            },
            "Leveraged Funds": {
                "long": "Lev_Money_Positions_Long_All",
                "short": "Lev_Money_Positions_Short_All",
                "net": "Net_LevFunds"
            },
            "Other Reportables": {
                "long": "Other_Rept_Positions_Long_All",
                "short": "Other_Rept_Positions_Short_All",
                "net": "Net_OtherReport"
            },
            "Nonreportable": {
                "long": "NonRept_Positions_Long_All",
                "short": "NonRept_Positions_Short_All",
                "net": "Net_NonReport"
            }
        }
        cat_names = list(CATS.keys())

        selected_market = st.selectbox(
            "Sélectionne un marché / actif (pour le tableau évolution)",
            markets,
            index=markets.index("EURO FX - CHICAGO MERCANTILE EXCHANGE") if "EURO FX - CHICAGO MERCANTILE EXCHANGE" in markets else 0
        )
        selected_cats = st.multiselect(
            "Catégories à afficher (pour le tableau évolution)",
            cat_names,
            default=["Leveraged Funds"]
        )
        dff = df[df['Market_and_Exchange_Names'] == selected_market].copy()
        dff = dff.sort_values("Date")
        date_min, date_max = dff['Date'].min().date(), dff['Date'].max().date()
        start_date, end_date = st.slider(
            "Filtrer par plage de dates",
            min_value=date_min,
            max_value=date_max,
            value=(date_min, date_max),
            format="YYYY-MM-DD"
        )
        dff = dff[(dff['Date'] >= pd.to_datetime(start_date)) & (dff['Date'] <= pd.to_datetime(end_date))].reset_index(drop=True)

        st.subheader("Tableau des changements hebdo")
        change_cols = []
        for cat in selected_cats:
            cols = CATS[cat]
            for typ, label in zip(['long', 'short', 'net'], ['Long', 'Short', 'Net']):
                col_name = f"{cat} {label}"
                dff[col_name] = dff[cols[typ]]
                dff[f"{col_name} Δ"] = dff[col_name].diff()
                change_cols += [col_name, f"{col_name} Δ"]

        dff_show = dff.sort_values("Date", ascending=False)[['Date'] + change_cols]
        st.dataframe(dff_show)
        st.download_button(
            label="Télécharger ce tableau filtré (CSV)",
            data=dff_show.to_csv(index=False).encode('utf-8'),
            file_name=f"COT_{selected_market.replace(' ','_')}_long_short_net.csv",
            mime='text/csv'
        )

        st.markdown("---")
        st.header("Smart Money Donut : Répartition Long/Short par paire & catégorie (type PMT)")

        all_dates = df['Date'].sort_values().dt.strftime("%Y-%m-%d").unique().tolist()
        selected_date_str = st.selectbox("Choisis la semaine à afficher (Donut)", all_dates, index=len(all_dates)-1)
        cat_donut_multi = st.multiselect(
            "Catégories à afficher (1 donut/catégorie par marché)",
            cat_names,
            default=["Leveraged Funds"]
        )
        markets_for_donut = st.multiselect(
            "Marchés à afficher (1 donut par marché)",
            markets,
            default=[selected_market]
        )
        for cat_donut in cat_donut_multi:
            if len(markets_for_donut) == 0:
                st.info("Sélectionne au moins un marché à afficher pour voir le donut chart.")
                continue
            donut_cols = st.columns(len(markets_for_donut))
            for i, market in enumerate(markets_for_donut):
                this_row = df[(df['Market_and_Exchange_Names'] == market) & (df['Date'] == pd.to_datetime(selected_date_str))]
                if not this_row.empty:
                    long_value = int(this_row[CATS[cat_donut]['long']].values[0])
                    short_value = int(this_row[CATS[cat_donut]['short']].values[0])
                    net_value = long_value - short_value
                    total = long_value + short_value
                    long_pct = long_value / total * 100 if total else 0
                    short_pct = short_value / total * 100 if total else 0

                    fig = go.Figure()
                    fig.add_trace(go.Pie(
                        labels=['Long', 'Short'],
                        values=[long_value, short_value],
                        hole=0.7,
                        marker=dict(colors=['#18d6b0', '#f54986']),
                        sort=False,
                        direction='clockwise',
                        pull=[0.04, 0.04],
                        textinfo='none',
                        hoverinfo='label+value+percent',
                    ))
                    fig.update_layout(
                        margin=dict(l=10, r=10, t=60, b=10),
                        template="plotly_dark",
                        showlegend=False,
                        height=320,
                        annotations=[
                            dict(
                                text=f"<b>{market}</b>",
                                x=0.5, y=1.22, xref='paper', yref='paper',
                                font_size=18, showarrow=False, align='center', font_family="Arial"
                            ),
                            dict(
                                text=f"<span style='font-size:14px'>{cat_donut}</span>",
                                x=0.5, y=1.09, xref='paper', yref='paper',
                                font_size=13, showarrow=False, align='center', font_family="Arial"
                            ),
                            dict(
                                text=(
                                    f"<span style='color:#18d6b0; font-size:16px; font-weight:600;"
                                    "text-shadow:1px 1px 4px #072e2d;'>"
                                    f"Long<br>{format_number(long_value)} / {long_pct:.0f}%"
                                    "</span>"
                                ),
                                x=0.17, y=0.61, xref='paper', yref='paper',
                                showarrow=False, align='center'
                            ),
                            dict(
                                text=(
                                    f"<span style='color:#f54986; font-size:16px; font-weight:600;"
                                    "text-shadow:1px 1px 4px #380c1a;'>"
                                    f"Short<br>{format_number(short_value)} / {short_pct:.0f}%"
                                    "</span>"
                                ),
                                x=0.83, y=0.61, xref='paper', yref='paper',
                                showarrow=False, align='center'
                            ),
                            dict(
                                text=f"<b>Net</b><br><span style='font-size:22px; color:{'#18d6b0' if net_value>0 else '#f54986'}'>{net_value:+,}</span>",
                                x=0.5, y=0.5, xref='paper', yref='paper',
                                font_size=21, showarrow=False, align='center', font_family="Arial"
                            ),
                        ]
                    )
                    fig.update_traces(
                        textfont_size=13,
                        marker_line_color='rgba(0,0,0,0)',
                    )
                    donut_cols[i].plotly_chart(fig, use_container_width=True)
                else:
                    donut_cols[i].info(f"Aucune donnée : {market}")

    else:
        st.warning("Aucune donnée à afficher. Veuillez lancer le script d'extraction d'abord.")

    st.caption("Terminal Perso – COT Financial Donut Dashboard v5.0 (par famille d'actif, PMT style)")
