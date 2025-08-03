import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

def display():
    # ------------ ASSETS (Forex, Indices, Actions US, Crypto, Commodities, Vol) ------------
    forex_majors = {
        'EUR/USD': 'EURUSD=X',
        'USD/JPY': 'JPY=X',
        'GBP/USD': 'GBPUSD=X',
        'USD/CHF': 'CHF=X',
        'AUD/USD': 'AUDUSD=X',
        'NZD/USD': 'NZDUSD=X',
        'USD/CAD': 'CAD=X',
    }
    forex_minors = {
        'EUR/GBP': 'EURGBP=X',
        'EUR/JPY': 'EURJPY=X',
        'GBP/JPY': 'GBPJPY=X',
        'EUR/AUD': 'EURAUD=X',
        'EUR/CHF': 'EURCHF=X',
        'AUD/JPY': 'AUDJPY=X',
        'CHF/JPY': 'CHFJPY=X',
        'GBP/CHF': 'GBPCHF=X',
        'AUD/NZD': 'AUDNZD=X',
        'CAD/JPY': 'CADJPY=X',
        'NZD/JPY': 'NZDJPY=X',
        'GBP/AUD': 'GBPAUD=X',
        'AUD/CAD': 'AUDCAD=X',
        'NZD/CAD': 'NZDCAD=X',
        'EUR/CAD': 'EURCAD=X',
        'GBP/CAD': 'GBPCAD=X',
        'AUD/CHF': 'AUDCHF=X',
        'NZD/CHF': 'NZDCHF=X',
    }
    maj_indices = {
        'S&P 500': '^GSPC',
        'Nasdaq 100': '^NDX',
        'Dow Jones 30': '^DJI',
        'Russell 2000': '^RUT',
        'FTSE 100 (UK)': '^FTSE',
        'DAX (Allemagne)': '^GDAXI',
        'CAC 40 (France)': '^FCHI',
        'EuroStoxx 50': '^STOXX50E',
        'Nikkei 225 (Japon)': '^N225',
        'Hang Seng (HK)': '^HSI',
        'S&P/ASX 200 (Australie)': '^AXJO',
        'SSE Composite (Chine)': '000001.SS',
        'Bovespa (Brésil)': '^BVSP',
        'S&P/TSX (Canada)': '^GSPTSE',
    }
    us_stocks = {
        'Apple (AAPL)': 'AAPL',
        'Microsoft (MSFT)': 'MSFT',
        'Nvidia (NVDA)': 'NVDA',
        'Tesla (TSLA)': 'TSLA',
        'Alphabet C (GOOG)': 'GOOG',
        'Alphabet A (GOOGL)': 'GOOGL',
        'Amazon (AMZN)': 'AMZN',
        'Meta Platforms (META)': 'META',
        'Broadcom (AVGO)': 'AVGO',
        'JPMorgan Chase (JPM)': 'JPM',
        'Berkshire Hathaway (BRK-B)': 'BRK-B',
        'Exxon Mobil (XOM)': 'XOM',
        'Visa (V)': 'V',
        'UnitedHealth (UNH)': 'UNH',
        'Procter & Gamble (PG)': 'PG',
        'Mastercard (MA)': 'MA',
        'Chevron (CVX)': 'CVX',
        'Johnson & Johnson (JNJ)': 'JNJ',
        'Costco (COST)': 'COST',
        'Walmart (WMT)': 'WMT',
    }
    cryptos = {
        'Bitcoin (BTC/USD)': 'BTC-USD',
        'Ethereum (ETH/USD)': 'ETH-USD',
        'Solana (SOL/USD)': 'SOL-USD',
        'Binance Coin (BNB/USD)': 'BNB-USD',
        'XRP (XRP/USD)': 'XRP-USD',
        'Cardano (ADA/USD)': 'ADA-USD',
        'Dogecoin (DOGE/USD)': 'DOGE-USD',
        'Toncoin (TON/USD)': 'TON11419-USD',
        'Avalanche (AVAX/USD)': 'AVAX-USD',
        'Polkadot (DOT/USD)': 'DOT-USD',
        'Chainlink (LINK/USD)': 'LINK-USD',
        'Polygon (MATIC/USD)': 'MATIC-USD',
    }
    commodities = {
        'Or (Gold)': 'GC=F',
        'Argent (Silver)': 'SI=F',
        'Pétrole WTI': 'CL=F',
        'Pétrole Brent': 'BZ=F',
        'Cuivre (Copper)': 'HG=F',
        'Platine (Platinum)': 'PL=F',
        'Palladium': 'PA=F',
        'Maïs (Corn)': 'ZC=F',
        'Blé (Wheat)': 'ZW=F',
        'Soja (Soybeans)': 'ZS=F',
        'Café (Coffee)': 'KC=F',
        'Cacao (Cocoa)': 'CC=F',
        'Sucre (Sugar)': 'SB=F',
        'Coton (Cotton)': 'CT=F',
        'Bois (Lumber)': 'LB=F',
    }
    vol_indices = {
        'VIX (S&P500)': '^VIX',
        'VXN (Nasdaq 100)': '^VXN',
        'VXD (Dow Jones)': '^VXD',
        'GVZ (Gold Volatility Index)': '^GVZ',
        'OVX (Oil Volatility Index)': '^OVX',
    }
    ASSETS = {
        "Forex Majors": {**forex_majors, **forex_minors},
        "Indices mondiaux": maj_indices,
        "Actions US": us_stocks,
        "Crypto": cryptos,
        "Commodities": commodities,
        "Indices de volatilité": vol_indices,
    }
    ALL_ASSETS = {}
    for asset_dict in ASSETS.values():
        ALL_ASSETS.update(asset_dict)

    st.title("📊 Terminal Cookingtime")

    # Cross-asset multiselect prioritaire
    cross_assets = st.sidebar.multiselect(
        "💡 Cross-asset : comparer n'importe quels actifs ensemble",
        list(ALL_ASSETS.keys()),
        default=[]
    )

    # Sélection par classe (seulement si cross_assets vide)
    asset_classes = list(ASSETS.keys())
    asset_class = st.sidebar.selectbox("Classe d'actifs :", asset_classes)

    asset_choices = list(ASSETS[asset_class].keys())
    selected_assets = st.sidebar.multiselect(
        "Sélectionne les actifs à afficher :", asset_choices, default=[asset_choices[0]]
    )

    # Choix de la liste utilisée : cross-asset prioritaire si sélectionné
    if cross_assets:
        asset_list = cross_assets
        asset_dict = ALL_ASSETS
    else:
        asset_list = selected_assets
        asset_dict = ASSETS[asset_class]

    col1, col2 = st.columns([2, 1])
    with col2:
        date1 = st.date_input("Date début", pd.to_datetime("2023-01-01"))
        date2 = st.date_input("Date fin", pd.to_datetime("2023-07-29"))

    with col1:
        st.write("### Résumé & comparatif multi-actifs")
        all_data = {}
        for asset in asset_list:
            ticker = asset_dict[asset]
            df = yf.download(ticker, start=date1, end=date2)
            if not df.empty:
                all_data[asset] = df
            else:
                st.warning(f"Aucune donnée pour {asset}.")

        if all_data:
            n = len(all_data)
            cols = st.columns(n)
            for i, (asset, df) in enumerate(all_data.items()):
                with cols[i]:
                    st.markdown(f"#### {asset}")
                    close_col = next((col for col in ['Close', 'Adj Close', 'adjusted_close', 'close'] if col in df.columns), df.columns[0])
                    st.line_chart(df[close_col], use_container_width=True)
                    if 'Volume' in df.columns:
                        st.bar_chart(df['Volume'], use_container_width=True)
                    df_for_display = df.copy()
                    if isinstance(df_for_display.columns, pd.MultiIndex):
                        df_for_display.columns = [f"{c[0]} ({c[1]})" for c in df_for_display.columns]
                        ticker_to_name = {
                            '^GSPC': 'S&P 500',
                            '^VIX': 'VIX',
                            '^VXN': 'VXN',
                            '^VXD': 'VXD',
                            '^GVZ': 'GVZ',
                            '^OVX': 'OVX',
                            '^NDX': 'Nasdaq 100',
                            '^STOXX50E': 'Eurostoxx 50',
                        }
                        df_for_display.columns = [
                            c.replace(f"({ticker})", f"({ticker_to_name.get(ticker, ticker)})") if "(" in c else c
                            for c, ticker in zip(df_for_display.columns, [x.split('(')[-1][:-1] for x in df_for_display.columns])
                        ]
                    else:
                        ticker_to_name = {
                            '^GSPC': 'S&P 500',
                            '^VIX': 'VIX',
                            '^VXN': 'VXN',
                            '^VXD': 'VXD',
                            '^GVZ': 'GVZ',
                            '^OVX': 'OVX',
                            '^NDX': 'Nasdaq 100',
                            '^STOXX50E': 'Eurostoxx 50',
                        }
                        df_for_display.columns = [ticker_to_name.get(c, c) for c in df_for_display.columns]

                    st.dataframe(df_for_display, use_container_width=True, height=600)

            display_mode = st.radio(
                "Mode de superposition graphique :",
                ["Absolu (prix)", "Performance normalisée", "Échelle logarithmique", "Rendements log cumulés"],
                index=1,
                horizontal=True
            )

            st.markdown("### Superposition de tous les actifs")
            fig, ax = plt.subplots(figsize=(10, 5))
            for asset, df in all_data.items():
                close_col = next((col for col in ['Close', 'Adj Close', 'adjusted_close', 'close'] if col in df.columns), df.columns[0])
                series = df[close_col]
                if display_mode == "Absolu (prix)":
                    ax.plot(df.index, series, label=asset)
                elif display_mode == "Performance normalisée":
                    norm = series / series.iloc[0]
                    ax.plot(df.index, norm, label=asset)
                elif display_mode == "Échelle logarithmique":
                    ax.plot(df.index, series, label=asset)
                    ax.set_yscale('log')
                elif display_mode == "Rendements log cumulés":
                    log_returns = np.log(series / series.shift(1)).cumsum()
                    ax.plot(df.index, log_returns, label=asset)

            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
        else:
            st.info("Sélectionne au moins un actif pour lancer l’analyse.")

    # NEWS FEED
    st.markdown("---")
    st.title("📰 News Feed Multi-Actifs avec Filtre")

    news_assets = st.multiselect(
        "Sélectionne les actifs dont tu veux voir les news :",
        list(ALL_ASSETS.keys()),
        default=selected_assets if selected_assets else ["Apple (AAPL)", "Nasdaq 100"]
    )

    keywords = st.text_input(
        "🔎 Filtrer les news par mots-clés/thèmes (ex : FOMC, CPI, earnings, Powell, SEC, inflation, recession…)", 
        ""
    )

    for asset in news_assets:
        ticker = ALL_ASSETS[asset]
        tk = yf.Ticker(ticker)
        news = tk.news

        st.subheader(f"📰 {asset} ({ticker})")
        shown = 0

        if not news or not isinstance(news, list):
            st.info("Aucune news disponible pour ce ticker.")
            continue

        for item in news[:10]:
            title = None
            if 'content' in item and 'title' in item['content']:
                title = item['content']['title']
            elif 'title' in item:
                title = item['title']

            link = None
            if 'content' in item and 'canonicalUrl' in item['content']:
                link = item['content']['canonicalUrl'].get('url')
            elif 'canonicalUrl' in item and 'url' in item['canonicalUrl']:
                link = item['canonicalUrl']['url']
            elif 'clickThroughUrl' in item and 'url' in item['clickThroughUrl']:
                link = item['clickThroughUrl']['url']
            elif 'link' in item:
                link = item['link']

            if not title or not link:
                continue

            if keywords:
                kwords = [kw.strip().lower() for kw in keywords.split(",") if kw.strip()]
                title_lower = title.lower() if title else ""
                if not any(kw in title_lower for kw in kwords):
                    continue

            st.markdown(f"- [{title}]({link})")
            shown += 1

            summary = None
            if 'content' in item and 'summary' in item['content']:
                summary = item['content']['summary']
            elif 'summary' in item:
                summary = item['summary']
            if summary:
                st.caption(summary)

        if shown == 0:
            st.info("Aucune news exploitable pour ce ticker (ou aucune news avec un titre/lien ou correspondant à ton filtre).")
