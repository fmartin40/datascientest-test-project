import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Top Skills for Data Nerds", layout="wide")
st.title("🛠️ Top Skills for Data Nerds 😳")

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

# ----------------------------
# Visualisation temporelle des compétences
# ----------------------------

# Données simulées par catégorie
categories = {
    "Langages": ["python", "java", "scala", "sql", "bash", "go", "shell"],
    "Librairies Python": ["pandas", "numpy", "pyarrow", "polars", "fastapi"],
    "Orchestrateurs & ETL": [
        "airflow",
        "luigi",
        "dagster",
        "prefect",
        "dbt",
        "talend",
        "nifi",
        "informatica",
        "matillion",
        "stitch",
        "fivetran",
    ],
    "Cloud & Stockage": [
        "aws",
        "gcp",
        "azure",
        "s3",
        "gcs",
        "bigquery",
        "redshift",
        "snowflake",
        "databricks",
        "synapse",
        "data lake",
        "data warehouse",
    ],
    "Bases de Données": [
        "postgresql",
        "mysql",
        "sql server",
        "clickhouse",
        "mongodb",
        "cassandra",
        "dynamodb",
        "redis",
        "elasticsearch",
        "neo4j",
    ],
    "Streaming & Big Data": ["kafka", "kinesis", "flink", "spark", "beam", "hadoop"],
    "CI/CD & DevOps": [
        "git",
        "github",
        "gitlab",
        "ci/cd",
        "jenkins",
        "github actions",
        "gitlab ci/cd",
        "terraform",
        "ansible",
        "vault",
        "docker",
        "kubernetes",
        "helm",
    ],
    "Monitoring & Sécurité": ["grafana", "prometheus", "datadog", "iam", "oauth2"],
    "Data Viz & Qualité": [
        "superset",
        "looker",
        "tableau",
        "powerbi",
        "soda",
        "great expectations",
    ],
}

dates = pd.date_range("2025-05-01", "2025-05-10")


@st.cache_data
def generate_time_data():
    data = []
    for cat, skills in categories.items():
        for skill in skills:
            counts = np.random.randint(10, 40, size=len(dates))
            for date, count in zip(dates, counts):
                data.append(
                    {
                        "date": date,
                        "competence": skill,
                        "categorie": cat,
                        "count": count,
                    }
                )
    return pd.DataFrame(data)


df_time = generate_time_data()

# Interface sélection de groupe
st.markdown("### 📈 Évolution des compétences dans le temps")
selected_group = st.radio("Choisissez une catégorie :", list(categories.keys()))

# Filtrer et afficher
df_group = df_time[df_time["categorie"] == selected_group]

fig = px.line(
    df_group,
    x="date",
    y="count",
    color="competence",
    markers=True,
    title=f"Tendance quotidienne – {selected_group}",
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Occurrences",
    legend_title="Compétence",
    template="plotly_white",
)

st.plotly_chart(fig, use_container_width=True)
