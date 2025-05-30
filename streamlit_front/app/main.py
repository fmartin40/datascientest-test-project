import streamlit as st

from sections.competences import afficher_competences_globales
from sections.timeline import afficher_timeline
from sections.recherche import afficher_recherche


# -------------------------------------
# Visualisation du moteur de recherche
# -------------------------------------
afficher_recherche()
st.markdown("---")

# -------------------------------------
# Visualisation aggregée des compétences
# -------------------------------------
afficher_competences_globales()
st.markdown("---")

# -------------------------------------
# Visualisation temporelle des compétences
# -------------------------------------
afficher_timeline()
st.markdown("---")
