import os
import json
import requests
import psycopg2

from psycopg2 import sql
from datetime import datetime
from dotenv import load_dotenv
from datetime import timezone

from utils.date import safe_parse_iso_date


class FranceTravailAPI:
    """
    Classe pour interagir avec l'API France Travail.
    Gère l'authentification, la recherche d'offres et la récupération des détails d'offres.
    """

    # URL pour générer l'access token
    ACCESS_TOKEN_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"

    # URL pour l'api France Travail
    SEARCH_API_URL = (
        "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
    )
    OFFER_API_URL = (
        "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/{id}"
    )

    def __init__(self):
        # Charger les variables d'environnement depuis le fichier .env
        load_dotenv()
        self.client_id = os.getenv("FRANCE_TRAVAIL_CLIENT_ID")
        self.client_secret = os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET")
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/x-www-form-urlencoded"}
        )

        self.access_token = None
        self.current_date = datetime.now().strftime("%d%m%Y")

        # Récupérer la racine du projet
        self.root_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../..")
        )
        # Construire le bon chemin vers `data/`
        self.data_dir = os.path.join(self.root_dir, "data")
        # Vérifier si le dossier `data/` existe, sinon le créer
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)

    def get_access_token(self):
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "api_offresdemploiv2 o2dsoffre",
        }

        try:
            response = self.session.post(self.ACCESS_TOKEN_URL, data=data)
            response.raise_for_status()
            self.access_token = response.json().get("access_token")
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération du token : {e}")

    def search_offers(self, params):
        """
        Recherche les offres d'emploi en fonction des paramètres fournis.
        :param params: Dictionnaire contenant les paramètres de recherche.
        :return: Liste des offres d'emploi.
        """

        if not self.access_token:
            print("Erreur : aucun token d'accès disponible.")
            return []

        headers = {"Authorization": f"Bearer {self.access_token}"}
        all_offers = []
        range_start = 0
        range_step = 50

        while True:
            # Définition du paramètre de pagination "range" pour cette requête
            params["range"] = f"{range_start}-{range_start + range_step - 1}"

            try:
                response = requests.get(
                    self.SEARCH_API_URL, headers=headers, params=params
                )
                if response.status_code == 200:
                    # Toutes les annonces ont été envoyées en une seule fois
                    data = response.json()
                    all_offers.extend(data.get("resultats", []))
                    print("Toutes les offres ont été récupérées en une seule fois.")
                    break
                elif response.status_code == 206:
                    # Réponse partielle : récupération des annonces de cette page
                    data = response.json()
                    offers = data.get("resultats", [])
                    print(f"Nombre d'offres reçues lors de cet appel : {len(offers)}")
                    all_offers.extend(offers)

                    # Condition de fin : si moins de 50 offres sont reçues, fin de pagination
                    if len(offers) < range_step:
                        print(
                            "Fin de la pagination : toutes les offres ont été récupérées."
                        )
                        break
                    else:
                        # Continuer la pagination si on reçoit exactement `range_step` offres
                        range_start += range_step
                elif response.status_code == 204:
                    print("Aucune offre ne correspond aux critères de recherche.")
                    break
                elif response.status_code == 400:
                    print("Erreur 400 : Requête invalide. Vérifiez les paramètres.")
                    print(response)
                    break
                elif response.status_code == 500:
                    print(
                        "Erreur 500 : Erreur interne du serveur. Réessayez plus tard."
                    )
                    break
                else:
                    print(f"Code de réponse inattendu : {response.status_code}")
                    break

            except requests.exceptions.RequestException as e:
                print(f"Erreur lors de la récupération des offres : {e}")
                break

        return all_offers

    def save_offers_in_json_file(self, offers):
        """
        Sauvegarde les offres d'emploi dans un fichier JSON.
        """

        filename = f"{self.current_date}-offres_d_emploi.json"
        filepath = os.path.join(self.data_dir, filename)

        # Sauvegarder dans un fichier JSON
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(offers, f, ensure_ascii=False, indent=4)

        print(f"Offres sauvegardées dans {filename}")

    # def insert_offers_to_db(self, offers):
    #     """
    #     Insère les offres d'emploi dans une base de données PostgreSQL.
    #     """

    #     conn = None
    #     cursor = None

    #     try:
    #         # Connexion à la base PostgreSQL
    #         conn = psycopg2.connect(
    #             dbname = os.getenv('DB_NAME'),
    #             user = os.getenv('DB_USER'),
    #             password = os.getenv('DB_PASSWORD'),
    #             host="pgdatabase",
    #             port="5432"
    #         )
    #         cursor = conn.cursor()

    #         # Insérer les données dans la table
    #         for offer in offers:
    #             try:
    #                 # Sécurité sur les dates
    #                 raw_date_actualisation = offer.get("dateActualisation")
    #                 format_date_actualisation = safe_parse_iso_date(raw_date_actualisation)

    #                 if not format_date_actualisation:
    #                     print(f"Date invalide pour l'offre {offer.get('id')} : {raw_date_actualisation}")
    #                     continue

    #                 raw_date_creation = offer.get("dateCreation")
    #                 format_date_creation = safe_parse_iso_date(raw_date_creation)

    #                 if not format_date_creation:
    #                     print(f"Date invalide pour l'offre {offer.get('id')} : {raw_date_creation}")
    #                     continue

    #                 # Vérification de l'existence
    #                 cursor.execute('SELECT "id", "dateActualisation" FROM "OffreEmploi" WHERE "source_offre_id" = %s', (offer.get("id"),))
    #                 existing_offer = cursor.fetchone()

    #                 if existing_offer:
    #                     existing_id, existing_date = existing_offer
    #                     should_update = True

    #                     if existing_date:
    #                         existing_date = existing_date.replace(tzinfo=timezone.utc)
    #                         if format_date_actualisation <= existing_date:
    #                             print(f"Offre {offer.get('id')} déjà à jour. Ignorée.")
    #                             should_update = False

    #                     if should_update:
    #                         print(f"Mise à jour de l'offre {offer.get('id')}")
    #                         cursor.execute('DELETE FROM "OffreEmploi" WHERE "id" = %s', (existing_id,))
    #                     else:
    #                         continue

    #                 lieuTravail_id = self.insert_lieuTravail(cursor, offer.get("lieuTravail"))
    #                 entreprise_id = self.insert_entreprise(cursor, offer.get("entreprise"))
    #                 salaire_id = self.insert_salaire(cursor, offer.get("salaire"))
    #                 contact_id = self.insert_contact(cursor, offer.get("contact"))
    #                 agence_id = self.insert_agence(cursor, offer.get("agence"))
    #                 origine_id = self.insert_origine_offre(cursor, offer.get("origineOffre"))

    #                 insert_query = """
    #                 INSERT INTO "OffreEmploi" (
    #                     "source",
    #                     "source_offre_id",
    #                     "intitule",
    #                     "description",
    #                     "dateCreation",
    #                     "dateActualisation",
    #                     "lieuTravail_id",
    #                     "romeCode",
    #                     "romeLibelle",
    #                     "appellationlibelle",
    #                     "entreprise_id",
    #                     "typeContrat",
    #                     "typeContratLibelle",
    #                     "natureContrat",
    #                     "experienceExige",
    #                     "experienceLibelle",
    #                     "experienceCommentaire",
    #                     "dureeTravailLibelle",
    #                     "dureeTravailLibelleConverti",
    #                     "complementExercice",
    #                     "conditionExercice",
    #                     "alternance",
    #                     "salaire_id",
    #                     "contact_id",
    #                     "agence_id",
    #                      "nombrePostes",
    #                      "accessibleTH",
    #                      "deplacementCode",
    #                      "deplacementLibelle",
    #                     "qualificationCode",
    #                     "qualificationLibelle",
    #                     "codeNAF",
    #                     "secteurActivite",
    #                     "secteurActiviteLibelle",
    #                     "trancheEffectifEtab",
    #                     "offresManqueCandidats",
    #                     "origine_id"
    #                 ) VALUES (
    #                     'France Travail',
    #                     %(source_offre_id)s,
    #                     %(intitule)s,
    #                     %(description)s,
    #                     %(dateCreation)s,
    #                     %(dateActualisation)s,
    #                     %(lieuTravail_id)s,
    #                     %(romeCode)s,
    #                     %(romeLibelle)s,
    #                     %(appellationlibelle)s,
    #                     %(entreprise_id)s,
    #                     %(typeContrat)s,
    #                     %(typeContratLibelle)s,
    #                     %(natureContrat)s,
    #                     %(experienceExige)s,
    #                     %(experienceLibelle)s,
    #                     %(experienceCommentaire)s,
    #                     %(dureeTravailLibelle)s,
    #                     %(dureeTravailLibelleConverti)s,
    #                     %(complementExercice)s,
    #                     %(conditionExercice)s,
    #                     %(alternance)s,
    #                     %(salaire_id)s,
    #                     %(contact_id)s,
    #                     %(agence_id)s,
    #                     %(nombrePostes)s,
    #                     %(accessibleTH)s,
    #                     %(deplacementCode)s,
    #                     %(deplacementLibelle)s,
    #                     %(qualificationCode)s,
    #                     %(qualificationLibelle)s,
    #                     %(codeNAF)s,
    #                     %(secteurActivite)s,
    #                     %(secteurActiviteLibelle)s,
    #                     %(trancheEffectifEtab)s,
    #                     %(offresManqueCandidats)s,
    #                     %(origine_id)s
    #                 )
    #                 """

    #                 cursor.execute(insert_query, {
    #                     "source_offre_id": offer.get("id"),
    #                     "intitule": offer.get("intitule"),
    #                     "description": offer.get("description"),
    #                     "dateCreation": format_date_creation.isoformat(),
    #                     "dateActualisation": format_date_actualisation.isoformat(),
    #                     "lieuTravail_id": lieuTravail_id,
    #                     "romeCode": offer.get("romeCode"),
    #                     "romeLibelle": offer.get("romeLibelle"),
    #                     "appellationlibelle": offer.get("appellationlibelle"),
    #                     "entreprise_id": entreprise_id,
    #                     "typeContrat": offer.get("typeContrat"),
    #                     "typeContratLibelle": offer.get("typeContratLibelle"),
    #                     "natureContrat": offer.get("natureContrat"),
    #                     "experienceExige": offer.get("experienceExige"),
    #                     "experienceLibelle": offer.get("experienceLibelle"),
    #                     "experienceCommentaire": offer.get("experienceCommentaire"),
    #                     "dureeTravailLibelle": offer.get("dureeTravailLibelle"),
    #                     "dureeTravailLibelleConverti": offer.get("dureeTravailLibelleConverti"),
    #                     "complementExercice": offer.get("complementExercice"),
    #                     "conditionExercice": offer.get("conditionExercice"),
    #                     "alternance": offer.get("alternance"),
    #                     "salaire_id": salaire_id,
    #                     "contact_id": contact_id,
    #                     "agence_id": agence_id,
    #                     "nombrePostes": offer.get("nombrePostes"),
    #                     "accessibleTH": offer.get("accessibleTH"),
    #                     "deplacementCode": offer.get("deplacementCode"),
    #                     "deplacementLibelle": offer.get("deplacementLibelle"),
    #                     "qualificationCode": offer.get("qualificationCode"),
    #                     "qualificationLibelle": offer.get("qualificationLibelle"),
    #                     "codeNAF": offer.get("codeNAF"),
    #                     "secteurActivite": offer.get("secteurActivite"),
    #                     "secteurActiviteLibelle": offer.get("secteurActiviteLibelle"),
    #                     "trancheEffectifEtab": offer.get("trancheEffectifEtab"),
    #                     "offresManqueCandidats": offer.get("offresManqueCandidats"),
    #                     "origine_id": origine_id
    #                 })

    #                 cursor.execute('SELECT id FROM "OffreEmploi" WHERE "source_offre_id" = %s', (offer.get("id"),))
    #                 offre_id = cursor.fetchone()[0]

    #                 for formation in offer.get("formations", []):
    #                     formation_data = {
    #                         "codeFormation": formation.get("codeFormation"),
    #                         "domaineLibelle": formation.get("domaineLibelle"),
    #                         "niveauLibelle": formation.get("niveauLibelle"),
    #                         "commentaire": formation.get("commentaire"),
    #                         "exigence": formation.get("exigence")
    #                     }
    #                     formation_id = self.insert_or_get_id(cursor, "Formation", formation_data, "codeFormation")
    #                     cursor.execute(
    #                         'INSERT INTO "OffreEmploi_Formation" ("offre_id", "formation_id") VALUES (%s, %s) ON CONFLICT DO NOTHING',
    #                         (offre_id, formation_id)
    #                     )

    #                 for langue in offer.get("langues", []):
    #                     langue_data = {
    #                         "libelle": langue.get("libelle"),
    #                         "exigence": langue.get("exigence")
    #                     }
    #                     langue_id = self.insert_or_get_id(cursor, "Langue", langue_data, "libelle")
    #                     cursor.execute(
    #                         'INSERT INTO "OffreEmploi_Langue" ("offre_id", "langue_id") VALUES (%s, %s) ON CONFLICT DO NOTHING',
    #                         (offre_id, langue_id)
    #                     )

    #                 for permis in offer.get("permis", []):
    #                     permis_data = {
    #                         "libelle": permis.get("libelle"),
    #                         "exigence": permis.get("exigence")
    #                     }
    #                     permis_id = self.insert_or_get_id(cursor, "Permis", permis_data, "libelle")
    #                     cursor.execute(
    #                         'INSERT INTO "OffreEmploi_Permis" ("offre_id", "permis_id") VALUES (%s, %s) ON CONFLICT DO NOTHING',
    #                         (offre_id, permis_id)
    #                     )

    #                 for outil in offer.get("outilsBureautiques", []):
    #                     outil_data = {"libelle": outil}
    #                     outil_id = self.insert_or_get_id(cursor, "OutilBureautique", outil_data, "libelle")
    #                     cursor.execute(
    #                         'INSERT INTO "OffreEmploi_OutilBureautique" ("offre_id", "outil_id") VALUES (%s, %s) ON CONFLICT DO NOTHING',
    #                         (offre_id, outil_id)
    #                     )

    #                 for competence in offer.get("competences", []):
    #                     competence_data = {
    #                         "code": competence.get("code"),
    #                         "libelle": competence.get("libelle"),
    #                         "exigence": competence.get("exigence")
    #                     }
    #                     competence_id = self.insert_or_get_id(cursor, "Competence", competence_data, "code")
    #                     cursor.execute(
    #                         'INSERT INTO "OffreEmploi_Competence" ("offre_id", "competence_id") VALUES (%s, %s) ON CONFLICT DO NOTHING',
    #                         (offre_id, competence_id)
    #                     )

    #                 for qualite in offer.get("qualitesProfessionnelles", []):
    #                     qualite_data = {
    #                         "libelle": qualite.get("libelle"),
    #                         "description": qualite.get("description")
    #                     }
    #                     qualite_id = self.insert_or_get_id(cursor, "QualiteProfessionnelle", qualite_data, "libelle")
    #                     cursor.execute(
    #                         'INSERT INTO "OffreEmploi_QualiteProfessionnelle" ("offre_id", "qualite_id") VALUES (%s, %s) ON CONFLICT DO NOTHING',
    #                         (offre_id, qualite_id)
    #                     )

    #                 contexte = offer.get("contexteTravail", {})

    #                 # Insérer les horaires
    #                 for horaire in contexte.get("horaires", []):
    #                     contexte_data = { "libelle": horaire, "type": "horaire" }
    #                     contexte_id = self.insert_or_get_id(cursor, "ContexteTravail", contexte_data, "libelle")
    #                     cursor.execute(
    #                         'INSERT INTO "OffreEmploi_ContexteTravail" ("offre_id", "contexte_id") VALUES (%s, %s) ON CONFLICT DO NOTHING',
    #                         (offre_id, contexte_id)
    #                     )

    #                 # Insérer les conditions d'exercice
    #                 for condition in contexte.get("conditionsExercice", []):
    #                     contexte_data = { "libelle": condition, "type": "condition" }
    #                     contexte_id = self.insert_or_get_id(cursor, "ContexteTravail", contexte_data, "libelle")
    #                     cursor.execute(
    #                         'INSERT INTO "OffreEmploi_ContexteTravail" ("offre_id", "contexte_id") VALUES (%s, %s) ON CONFLICT DO NOTHING',
    #                         (offre_id, contexte_id)
    #                     )
    #             except Exception as e:
    #                 print(f"Erreur d'insertion pour l'offre {offer.get('id')}: {e}")

    #         # Commit les changements et fermer la connexion
    #         conn.commit()
    #         print("Données insérées avec succès dans la base de données.")
    #     except Exception as e:
    #         print(f"Erreur lors de la connexion ou de l'insertion dans la base : {e}")
    #     finally:
    #         if cursor:
    #             cursor.close()
    #         if conn:
    #             conn.close()

    # def insert_lieuTravail(self,cursor, lieuTravail):
    #     if lieuTravail is None:
    #         return None

    #     data = {
    #         "libelle": lieuTravail.get('libelle'),
    #         "latitude": lieuTravail.get('latitude'),
    #         "longitude": lieuTravail.get('longitude'),
    #         "codePostal": lieuTravail.get('codePostal'),
    #         "commune": lieuTravail.get('commune')
    #     }
    #     return self.insert_or_get_id(cursor, "LieuTravail", data, "libelle")

    # def insert_entreprise(self,cursor, entreprise):
    #     if entreprise.get('nom') is None:
    #         return None

    #     data = {
    #         "nom": entreprise.get('nom'),
    #         "description": entreprise.get('description'),
    #         "logo": entreprise.get('logo'),
    #         "url": entreprise.get('url'),
    #         "entrepriseAdaptee": entreprise.get('entrepriseAdaptee')
    #     }
    #     return self.insert_or_get_id(cursor, "Entreprise", data, "nom")

    # def insert_salaire(self, cursor, salaire):
    #     if not salaire:
    #         return None
    #     data = {
    #         "libelle": salaire.get("libelle"),
    #         "commentaire": salaire.get("commentaire"),
    #         "complement1": salaire.get("complement1"),
    #         "complement2": salaire.get("complement2")
    #     }
    #     return self.insert_or_get_id(cursor, "Salaire", data, "libelle")

    # def insert_contact(self, cursor, contact):
    #     if not contact:
    #         return None
    #     data = {
    #         "nom": contact.get("nom"),
    #         "coordonnees1": contact.get("coordonnees1"),
    #         "coordonnees2": contact.get("coordonnees2"),
    #         "coordonnees3": contact.get("coordonnees3"),
    #         "telephone": contact.get("telephone"),
    #         "courriel": contact.get("courriel"),
    #         "commentaire": contact.get("commentaire"),
    #         "urlRecruteur": contact.get("urlRecruteur"),
    #         "urlPostulation": contact.get("urlPostulation")
    #     }
    #     return self.insert_or_get_id(cursor, "Contact", data, "courriel")

    # def insert_agence(self, cursor, agence):
    #     if not agence:
    #         return None
    #     data = {
    #         "telephone": agence.get("telephone"),
    #         "courriel": agence.get("courriel")
    #     }
    #     return self.insert_or_get_id(cursor, "Agence", data, "courriel")

    # def insert_origine_offre(self, cursor, origineOffre):
    #     """
    #     Insère une origineOffre et ses partenaires dans les tables correspondantes.
    #     :param cursor: Curseur PostgreSQL
    #     :param origineOffre: Dictionnaire JSON extrait de l'offre
    #     :return: ID de l'origineOffre insérée
    #     """
    #     if not origineOffre:
    #         return None

    #     # Insertion ou récupération de l'origine de l'offre
    #     data = {
    #         "origine": origineOffre.get("origine"),
    #         "urlOrigine": origineOffre.get("urlOrigine")
    #     }
    #     origine_id = self.insert_or_get_id(cursor, "OrigineOffre", data, "urlOrigine")

    #     # Insertion des partenaires liés à cette origine
    #     for partenaire in origineOffre.get("partenaires", []):
    #         partenaire_data = {
    #             "nom": partenaire.get("nom"),
    #             "url": partenaire.get("url"),
    #             "logo": partenaire.get("logo")
    #         }
    #         partenaire_id = self.insert_or_get_id(cursor, "Partenaire", partenaire_data, "url")

    #         # Liaison N:N entre OrigineOffre et Partenaire
    #         cursor.execute(
    #             """
    #             INSERT INTO "OrigineOffre_Partenaire" ("origine_id", "partenaire_id")
    #             VALUES (%s, %s)
    #             ON CONFLICT DO NOTHING
    #             """,
    #             (origine_id, partenaire_id)
    #         )

    #     return origine_id

    # def insert_or_get_id(self,cursor, table, data, unique_column):
    #     """
    #     Insère une entrée dans une table si elle n'existe pas et retourne son id.
    #     :param cursor: Curseur PostgreSQL
    #     :param table: Nom de la table
    #     :param data: Dictionnaire contenant les données à insérer
    #     :param unique_column: Colonne utilisée pour vérifier l'existence
    #     :return: L'id de l'entrée (nouvelle ou existante)
    #     """

    #     query_check = sql.SQL("SELECT id FROM {table} WHERE {unique_column} = %s").format(
    #         table=sql.Identifier(table),
    #         unique_column=sql.Identifier(unique_column)
    #     )
    #     cursor.execute(query_check, (data[unique_column],))
    #     result = cursor.fetchone()

    #     if result:
    #         return result[0]  # L'entrée existe, retourner l'id

    #     # Insérer une nouvelle entrée
    #     columns = data.keys()
    #     query_insert = sql.SQL("INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING id").format(
    #         table=sql.Identifier(table),
    #         columns=sql.SQL(", ").join(map(sql.Identifier, columns)),
    #         values=sql.SQL(", ").join(sql.Placeholder() * len(columns))
    #     )
    #     cursor.execute(query_insert, tuple(data.values()))
    #     return cursor.fetchone()[0]

    def fetch_offer_details(self, offer_id):
        """
        Récupère les détails d'une offre et les sauvegarde dans un fichier JSON.
        """
        if not self.access_token:
            print("Erreur : aucun token d'accès disponible.")
            return

        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = self.OFFER_API_URL.format(id=offer_id)

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            offer_details = response.json()

            # Sauvegarde des détails de l'offre dans un fichier JSON
            filename = f"{self.current_date}-{offer_id}.json"
            filepath = os.path.join(self.data_dir, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(offer_details, f, ensure_ascii=False, indent=4)
            print(f"Détails de l'offre {offer_id} sauvegardés dans {filename}")

        except requests.exceptions.RequestException as e:
            print(
                f"Erreur lors de la récupération des détails de l'offre {offer_id} : {e}"
            )
