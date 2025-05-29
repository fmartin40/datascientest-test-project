import streamlit as st
import requests
from datetime import datetime
from ressources import (
    fetch_villes,
    fetch_entreprises,
    fetch_types_contrat,
    fetch_durees_travail,
    fetch_modes_travail,
)


def afficher_recherche():
    st.set_page_config(page_title="Top Skills for Data Nerds", layout="wide")
    st.title(" Dashboard Job Market")

    # ----------------------------
    # Champs de recherche et dates (en haut de la page)
    # ----------------------------
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_query = st.text_input("🔍 Recherche de compétence", "")
    with col2:
        start_date = st.date_input("Date de début", value=datetime(2025, 5, 1))
    with col3:
        end_date = st.date_input("Date de fin", value=datetime(2025, 5, 10))

    # ----------------------------
    # Menus déroulants supplémentaires (nouvelle ligne)
    # ----------------------------
    villes_data = fetch_villes()
    villes_options = ["Toutes"] + [
        v["libelle"].capitalize() for v in villes_data if v.get("libelle")
    ]
    villes_ids = {
        v["libelle"].capitalize(): v["id"] for v in villes_data if v.get("libelle")
    }

    entreprises_data = fetch_entreprises()
    entreprises_options = ["Toutes"] + [
        e["libelle"].capitalize() for e in entreprises_data if e.get("libelle")
    ]
    entreprises_ids = {
        e["libelle"].capitalize(): e["id"] for e in entreprises_data if e.get("libelle")
    }

    contrats_data = fetch_types_contrat()
    contrats_options = ["Tous"] + [
        c["libelle"].capitalize() for c in contrats_data if c.get("libelle")
    ]
    contrats_ids = {
        c["libelle"].capitalize(): c["id"] for c in contrats_data if c.get("libelle")
    }

    durees_data = fetch_durees_travail()
    durees_options = ["Toutes"] + [
        d["libelle"].capitalize() for d in durees_data if d.get("libelle")
    ]
    durees_ids = {
        d["libelle"].capitalize(): d["id"] for d in durees_data if d.get("libelle")
    }

    modes_data = fetch_modes_travail()
    modes_options = ["Tous"] + [
        m["libelle"].capitalize() for m in modes_data if m.get("libelle")
    ]
    modes_ids = {
        m["libelle"].capitalize(): m["id"] for m in modes_data if m.get("libelle")
    }

    col_ville, col_entreprise, col_contrat, col_duree, col_mode = st.columns(5)
    with col_ville:
        ville = st.selectbox("Ville", villes_options)
        ville_id = villes_ids.get(ville) if ville != "Toutes" else None
    with col_entreprise:
        entreprise = st.selectbox("Entreprise", entreprises_options)
        entreprise_id = (
            entreprises_ids.get(entreprise) if entreprise != "Toutes" else None
        )
    with col_contrat:
        type_contrat = st.selectbox("Type de contrat", contrats_options)
        type_contrat_id = (
            contrats_ids.get(type_contrat) if type_contrat != "Tous" else None
        )
    with col_duree:
        duree_travail = st.selectbox("Durée de travail", durees_options)
        duree_travail_id = (
            durees_ids.get(duree_travail) if duree_travail != "Toutes" else None
        )
    with col_mode:
        mode_travail = st.selectbox("Mode de travail", modes_options)
        mode_travail_id = (
            modes_ids.get(mode_travail) if mode_travail != "Tous" else None
        )

    # ----------------------------
    # Bouton de recherche et affichage des résultats (juste sous les menus déroulants)
    # ----------------------------
    if st.button("🔎 Rechercher les offres"):
        params = {}
        if ville_id:
            params["ville"] = ville_id
        if entreprise_id:
            params["entreprise"] = entreprise_id
        if type_contrat_id:
            params["type_contrat"] = type_contrat_id
        if duree_travail_id:
            params["duree_travail"] = duree_travail_id
        if mode_travail_id:
            params["mode_travail"] = mode_travail_id
        # Ajout du paramètre light à False par défaut
        params["light"] = False
        # Tu peux ajouter d'autres filtres ici si besoin

        jobs_url = "http://localhost:8003/jobs"
        with st.spinner("Recherche des offres en cours..."):
            try:
                response = requests.get(jobs_url, params=params)
                response.raise_for_status()
                jobs = response.json()
                if jobs:
                    st.success(f"{len(jobs)} offre(s) trouvée(s)")
                    col1, col2 = st.columns([2, 3])
                    with col1:
                        st.markdown("#### Offres d'emploi")
                        # Affichage en grille (2 colonnes)
                        n_col = 2
                        rows = [jobs[i : i + n_col] for i in range(0, len(jobs), n_col)]
                        for row in rows:
                            cols = st.columns(n_col)
                            for idx, job in enumerate(row):
                                with cols[idx]:
                                    job_id = job.get("job_id") or job.get("id")
                                    titre = job.get("libelle", "Sans titre")
                                    entreprise = job.get("entreprise", {}).get(
                                        "libelle", ""
                                    )
                                    type_contrat = job.get("type_contrat", {}).get(
                                        "libelle", ""
                                    )
                                    mode_travail = job.get("mode_travail", {}).get(
                                        "libelle", ""
                                    )
                                    duree_travail = job.get("duree_travail", {}).get(
                                        "libelle", ""
                                    )
                                    # Nom entreprise
                                    st.markdown(
                                        f"<span style='font-size:16px'>🏢 {entreprise}</span>",
                                        unsafe_allow_html=True,
                                    )
                                    # Titre de l'offre en lien hypertexte (sous le nom de l'entreprise)
                                    link_clicked = st.markdown(
                                        f"<a href='#{job_id}' style='text-decoration:underline;color:#2222aa;font-weight:bold;font-size:16px;' id='job_{job_id}'>{titre}</a>",
                                        unsafe_allow_html=True,
                                    )
                                    # Gestion du clic sur le lien (hack Streamlit)
                                    if "clicked_job_id" not in st.session_state:
                                        st.session_state["clicked_job_id"] = None
                                    if st.session_state.get("clicked_job_id") != job_id:
                                        if (
                                            st.session_state.get("last_url_hash")
                                            != job_id
                                        ):
                                            import streamlit as st2
                                            import urllib.parse

                                            url_hash = st.query_params.get(
                                                "job", [None]
                                            )[0]
                                            if url_hash == job_id:
                                                st.session_state["selected_job_id"] = (
                                                    job_id
                                                )
                                                st.session_state["clicked_job_id"] = (
                                                    job_id
                                                )
                                    # Badges
                                    badges = []
                                    if type_contrat:
                                        badges.append(
                                            f'<span style="background-color:#e0e0e0;border-radius:8px;padding:2px 8px;margin-right:4px;">{type_contrat}</span>'
                                        )
                                    if mode_travail:
                                        badges.append(
                                            f'<span style="background-color:#e0e0e0;border-radius:8px;padding:2px 8px;margin-right:4px;">{mode_travail}</span>'
                                        )
                                    if duree_travail:
                                        badges.append(
                                            f'<span style="background-color:#e0e0e0;border-radius:8px;padding:2px 8px;margin-right:4px;">{duree_travail}</span>'
                                        )
                                    if badges:
                                        st.markdown(
                                            " ".join(badges), unsafe_allow_html=True
                                        )
                                    st.markdown("---")
                    with col2:
                        selected_job_id = st.session_state.get("selected_job_id")
                        if selected_job_id:
                            detail_url = f"http://localhost:8003/jobs/{selected_job_id}"
                            try:
                                detail_resp = requests.get(detail_url)
                                detail_resp.raise_for_status()
                                job_detail = detail_resp.json()
                                st.markdown(
                                    f"### {job_detail.get('libelle', 'Sans titre')}"
                                )
                                st.write(job_detail)
                            except Exception as e:
                                st.error(
                                    f"Erreur lors de la récupération du détail : {e}"
                                )
                        else:
                            st.info(
                                "Cliquez sur une offre à gauche pour voir le détail."
                            )
                else:
                    st.info("Aucune offre trouvée pour ces critères.")
            except Exception as e:
                st.error(f"Erreur lors de la récupération des offres : {e}")
