# ===== STAGE 1: Build environment with uv =====
FROM python:3.10-slim as builder

WORKDIR /install

# Installer uv
RUN pip install uv

# Copier les fichiers nécessaires
COPY requirements.txt pyproject.toml uv.lock ./

# Installer les dépendances dans /install/packages
RUN uv pip install --system --target=/install/packages -r requirements.txt


# ===== STAGE 2: Runtime environment optimisé =====
FROM python:3.10-alpine

# Installer dépendances système pour les libs natives
RUN apk add --no-cache \
    libffi \
    libffi-dev \
    qt6-qtbase-dev \
    build-base \
    linux-headers \
    gcc \
    g++ \
    libxkbcommon \
    libxkbcommon-dev \
    freetype \
    freetype-dev \
    && pip install python-dotenv

# Créer utilisateur non-root
RUN adduser -D appuser

WORKDIR /app

# Copier les paquets installés depuis le builder
COPY --from=builder /install/packages /usr/local/lib/python3.10/site-packages

# Copier l'application
COPY app ./app
COPY .env .

# Installer PyFlow séparément
RUN pip install "git+https://github.com/pedroCabrera/PyFlow.git@6b522d2dfb0045b32b24cd42013ec4f03e931a55"

USER appuser

EXPOSE 8501

# Lancer Streamlit
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
