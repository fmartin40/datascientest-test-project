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
from api.functions import fetch_jobs


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
        from_date = st.date_input("Date de début", value=datetime(2025, 5, 1))
    with col3:
        to_date = st.date_input("Date de fin", value=datetime(2025, 5, 10))

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
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date
        if search_query:
            params["competence"] = search_query
        # Ajout du paramètre light à False par défaut
        params["light"] = False
        # Tu peux ajouter d'autres filtres ici si besoin

        # jobs_url = "http://localhost:8003/jobs"
        with st.spinner("Recherche des offres en cours..."):
            try:
                # response = requests.get(jobs_url, params=params)
                # print("Status Code:", params)
                # print("Status Code:", response.status_code)
                # # print("Response Text:", response.text)
                # response.raise_for_status()
                # # jobs = response.json()
                # jobs = response.json()
                jobs = fetch_jobs(params)
                if jobs:
                    st.success(f"{len(jobs)} offre(s) trouvée(s)")

                    offres_par_page = 4
                    total_pages = (len(jobs) + offres_par_page - 1) // offres_par_page

                    # Initialiser la page active
                    if "page_offre" not in st.session_state:
                        st.session_state.page_offre = 1

                    # Sélectionner les offres de la page en cours
                    start = (st.session_state.page_offre - 1) * offres_par_page
                    end = start + offres_par_page
                    page_jobs = jobs[start:end]

                    rows = [page_jobs[i : i + 2] for i in range(0, len(page_jobs), 2)]

                    for row in rows:
                        cols = st.columns(2)
                        for idx, job in enumerate(row):
                            with cols[idx]:
                                job_id = job.get("job_id") or job.get("id")
                                titre = job.get("libelle", "Sans titre")
                                entreprise = job.get("entreprise", {}).get(
                                    "libelle", ""
                                )
                                ville = job.get("ville", {}).get("libelle", "")
                                type_contrat = job.get("type_contrat", {}).get(
                                    "libelle", ""
                                )
                                mode_travail = job.get("mode_travail", {}).get(
                                    "libelle", ""
                                )
                                duree_travail = job.get("duree_travail", {}).get(
                                    "libelle", ""
                                )
                                description = job.get("description", "")

                                competences = job.get("competences", [])
                                competences_text = (
                                    ", ".join(c["libelle"] for c in competences)
                                    if competences
                                    else "Non spécifiées"
                                )

                                # Affichage
                                st.markdown(f"### {titre}")

                                infos = (
                                    f"<b>Entreprise :</b> {entreprise} &nbsp;&nbsp; "
                                    f"<b>Ville :</b> {ville} &nbsp;&nbsp; "
                                    f"<b>Contrat :</b> {type_contrat} &nbsp;&nbsp; "
                                    f"<b>Mode :</b> {mode_travail} &nbsp;&nbsp; "
                                    f"<b>Durée :</b> {duree_travail} &nbsp;&nbsp; "
                                    f"<b>Compétences :</b> {competences_text}"
                                )
                                st.markdown(infos, unsafe_allow_html=True)

                                st.markdown("**Description :**")
                                st.write(description or "Aucune description.")

                                if job.get("url"):
                                    st.markdown(
                                        f"[🔗 Voir l'offre]({job['url']})",
                                        unsafe_allow_html=True,
                                    )

                    # Pagination discrète alignée à droite
                    st.markdown(
                        """
                        <style>
                        .pagination {
                            display: flex;
                            justify-content: flex-end;
                            gap: 6px;
                            margin-top: 30px;
                            margin-bottom: 10px;
                        }
                        .pagination button {
                            background: none;
                            border: 1px solid #ccc;
                            padding: 4px 10px;
                            font-size: 14px;
                            border-radius: 5px;
                            cursor: pointer;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True,
                    )

                    pag_cols = st.columns(total_pages)
                    st.markdown('<div class="pagination">', unsafe_allow_html=True)
                    for i in range(total_pages):
                        if pag_cols[i].button(str(i + 1), key=f"page_{i+1}"):
                            st.session_state.page_offre = i + 1
                            st.experimental_rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

                else:
                    st.info("Aucune offre trouvée pour ces critères.")
            except Exception as e:
                st.error(f"Erreur lors de la récupération des offres : {e}")
