# Dockerfile

# Utilisation de l'image officielle de Python 3.12 Alpine
FROM python:3.12-alpine

# Définition du répertoire de travail
WORKDIR /app

# Environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie des fichiers de l'application
COPY . .

# Exposition du port utilisé par FastAPI
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
