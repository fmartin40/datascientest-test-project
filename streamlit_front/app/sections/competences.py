import streamlit as st
import pandas as pd


def afficher_competences_globales():
    # ----------------------------
    # Simuler les filtres (menu haut)
    # ----------------------------
    job_title = st.selectbox(
        "Job Title:", ["Select All", "Data Engineer", "Data Analyst", "Data Scientist"]
    )
    country = st.selectbox("Country:", ["Select All", "France", "USA", "Germany"])
    skill_category = st.radio(
        "Skills:",
        options=[
            "All",
            "Languages",
            "Tools",
            "Databases",
            "Cloud",
            "Libraries",
            "Frameworks",
        ],
        horizontal=True,
    )

    # ----------------------------
    # Simuler des données de compétence globales
    # ----------------------------
    @st.cache_data
    def fetch_skills(job_title, country, category):
        data = [
            {"skill": "Python", "percentage": 55.2},
            {"skill": "SQL", "percentage": 53.8},
            {"skill": "AWS", "percentage": 24.7},
            {"skill": "Azure", "percentage": 21.2},
            {"skill": "Spark", "percentage": 19.8},
            {"skill": "Tableau", "percentage": 16.6},
            {"skill": "R", "percentage": 16.5},
            {"skill": "Java", "percentage": 14.5},
            {"skill": "Excel", "percentage": 13.0},
            {"skill": "Power BI", "percentage": 12.2},
            {"skill": "Snowflake", "percentage": 11.7},
            {"skill": "Scala", "percentage": 11.2},
            {"skill": "Hadoop", "percentage": 11.0},
        ]
        return pd.DataFrame(data)

    df_bar = fetch_skills(job_title, country, skill_category)

    # ----------------------------
    # Affichage des barres horizontales
    # ----------------------------
    st.markdown("### 📊 Compétences globales")
    if not df_bar.empty:
        for _, row in df_bar.iterrows():
            st.progress(
                int(row["percentage"]), text=f"{row['skill']} — {row['percentage']}%"
            )
    else:
        st.warning("Aucune compétence trouvée.")
