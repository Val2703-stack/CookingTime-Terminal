import streamlit as st
import pandas as pd
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(CURRENT_DIR, "data", "sentiment.csv")

def display():
    st.title("📊 Sentiment Retail (Myfxbook)")

    # --- Chargement du CSV ---
    try:
        df = pd.read_csv(csv_path)
        st.success(f"Fichier chargé : {csv_path}")
    except Exception as e:
        st.error(f"Erreur de chargement du fichier CSV : {e}")
        st.stop()

    # --- Sélecteur de paires et graphique ---
    st.subheader("Graphique sentiment par paire")

    all_pairs = df["Pair"].tolist()
    selected_pairs = st.multiselect(
        "Sélectionne une ou plusieurs paires à afficher :",
        options=all_pairs,
        default=all_pairs[:10]
    )

    df_selection = df[df["Pair"].isin(selected_pairs)]

    if df_selection.empty:
        st.warning("Sélectionne au moins une paire.")
    else:
        st.bar_chart(
            data=df_selection.set_index("Pair")[["Long (%)", "Short (%)"]],
            use_container_width=True
        )

    max_n = len(df)
    top_n = st.slider("Nombre de paires à afficher (TOP N trié par Long %):", 1, max_n, min(15, max_n))
    df_sorted = df.sort_values(by="Long (%)", ascending=False).head(top_n)
    st.write("Top", top_n, "paires (par Long %):")
    st.bar_chart(
        data=df_sorted.set_index("Pair")[["Long (%)", "Short (%)"]],
        use_container_width=True
    )

    pair_search = st.text_input("Chercher une paire (ex: EURUSD) :")
    if pair_search:
        sub = df[df["Pair"].str.contains(pair_search.upper(), case=False)]
        if not sub.empty:
            st.dataframe(sub)
        else:
            st.warning("Aucune paire trouvée.")

    st.caption("Dernière mise à jour : " + str(df['Updated'].iloc[0]) + " (UTC)")
