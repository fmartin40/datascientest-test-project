import requests
from core.config import settings
import streamlit as st


@st.cache_data
def fetch_villes():
    try:
        response = requests.get(settings.LISTE_VILLE)
        response.raise_for_status()
        villes = response.json()
        return villes
    except Exception as e:
        st.warning(f"Erreur lors de la récupération des villes : {e}")
        return []


@st.cache_data
def fetch_entreprises():
    try:
        response = requests.get(settings.LISTE_ENTREPRISE)
        response.raise_for_status()
        entreprises = response.json()
        return entreprises
    except Exception as e:
        st.warning(f"Erreur lors de la récupération des entreprises : {e}")
        return []


@st.cache_data
def fetch_types_contrat():
    try:
        response = requests.get(settings.LISTE_CONTRAT)
        response.raise_for_status()
        contrats = response.json()
        return contrats
    except Exception as e:
        st.warning(f"Erreur lors de la récupération des types de contrat : {e}")
        return []


@st.cache_data
def fetch_durees_travail():
    try:
        response = requests.get(settings.LISTE_DUREE)
        response.raise_for_status()
        durees = response.json()
        return durees
    except Exception as e:
        st.warning(f"Erreur lors de la récupération des durées de travail : {e}")
        return []


@st.cache_data
def fetch_modes_travail():
    try:
        response = requests.get(settings.LISTE_MODE)
        response.raise_for_status()
        modes = response.json()
        return modes
    except Exception as e:
        st.warning(f"Erreur lors de la récupération des modes de travail : {e}")
        return []
