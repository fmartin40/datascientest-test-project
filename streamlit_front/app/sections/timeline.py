import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from api.functions import fetch_timeline_data

# ----------------------------
# Visualisation temporelle des compétences
# ----------------------------


def afficher_timeline():
    # Récupération des données depuis l'API
    try:
        data = fetch_timeline_data()
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return
    if not data:
        st.warning("Aucune donnée à afficher.")
        return

    # Construction du DataFrame
    records = []
    for item in data:
        competence = item["competence"]
        categorie = item["categorie"]
        for v in item["values"]:
            records.append(
                {
                    "date": v["date"],
                    "competence": competence,
                    "categorie": categorie,
                    "count": v["count"],
                    "pct_offres": v.get("pct_offres", 0),
                }
            )
    df_time = pd.DataFrame(records)
    if df_time.empty:
        st.warning("Aucune donnée à afficher.")
        return

    # Liste des catégories disponibles
    categories = df_time["categorie"].unique().tolist()
    categories.sort()

    # Interface sélection de groupe (catégorie)
    st.markdown("### Évolution des compétences dans le temps")
    selected_group = st.radio(
        "Choisissez une catégorie :",
        options=categories,
        horizontal=True,
    )

    # Filtrer les compétences de la catégorie sélectionnée
    competences = (
        df_time[df_time["categorie"] == selected_group]["competence"].unique().tolist()
    )
    competences.sort()

    # Ne garder que les compétences qui ont au moins une date (présentes dans df_time pour la catégorie sélectionnée)
    competences_with_dates = df_time[
        (df_time["categorie"] == selected_group) & (df_time["competence"].notnull())
    ]["competence"].value_counts()
    competences = [c for c in competences if competences_with_dates[c] > 0]

    selected_competences = st.multiselect(
        "Filtrer les compétences :",
        options=competences,
        default=competences[:2],
    )

    # Filtrer le DataFrame selon la sélection
    df_group = df_time[
        (df_time["categorie"] == selected_group)
        & (df_time["competence"].isin(selected_competences))
    ]

    # Conversion de la date
    df_group["date"] = pd.to_datetime(df_group["date"])

    # Tri par date
    df_group = df_group.sort_values(by="date")

    fig = px.line(
        df_group,
        x="date",
        y="pct_offres",
        color="competence",
        markers=True,
        title=f"Tendance quotidienne – {selected_group}",
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="% d'offres contenant la compétence",
        legend_title="Compétence",
        template="plotly_white",
    )

    st.plotly_chart(fig, use_container_width=True)
