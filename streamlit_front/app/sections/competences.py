import streamlit as st
import pandas as pd
import requests

# ---------------------------------------------
# Mapping ville libellé -> identifiant API
# ---------------------------------------------
VILLE_ID = {
    "Paris": 2,
    "Lyon": 3,
    "Marseille": 4,
}

API_ENDPOINT = "http://localhost:8003/competences/ville?ville_id={vid}"


@st.cache_data(show_spinner=False)
def fetch_skills(ville: str) -> pd.DataFrame:
    """Interroge l'API et renvoie un DataFrame normalisé."""
    if ville not in VILLE_ID:
        return pd.DataFrame()

    vid = VILLE_ID[ville]
    try:
        resp = requests.get(API_ENDPOINT.format(vid=vid), timeout=30)
        resp.raise_for_status()
        data = pd.DataFrame(resp.json())
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return pd.DataFrame()

    if data.empty:
        return data

    data["pct_cat"] = data["pct_cat"].astype(float)
    data["nb_offres"] = data["nb_offres"].astype(int)
    return data


def afficher_competences_globales():
    # ----------------------------
    # Filtres utilisateur (menu haut)
    # ----------------------------
    ville = st.selectbox("Ville:", ["Paris", "Marseille", "Lyon"])

    skill_category = st.radio(
        "Skills:",
        options=[
            "Languages",
            "Tools",
            "Databases",
            "Cloud",
            "Libraries",
            "Frameworks",
            "Orchestrateur",
            "DevOps",
            "Monitoring",
        ],
        horizontal=True,
    )

    # ----------------------------
    # Chargement des données API
    # ----------------------------
    df = fetch_skills(ville)

    if df.empty:
        st.warning("Aucune compétence trouvée.")
        return

    # Filtrer selon la catégorie sélectionnée
    df_filtered = df[df["categorie"].str.lower() == skill_category.lower()]
    df_filtered = df_filtered.sort_values("pct_cat", ascending=False)

    # ----------------------------
    # Affichage graphique
    # ----------------------------
    st.markdown(f"### 📊 Compétences — {skill_category}")
    if not df_filtered.empty:
        for _, row in df_filtered.iterrows():
            st.progress(
                int(row["pct_cat"]),
                text=f"{row['libelle'].title()} — {row['pct_cat']}%",
            )
    else:
        st.warning("Aucune compétence dans cette catégorie.")


if __name__ == "__main__":
    afficher_competences_globales()
