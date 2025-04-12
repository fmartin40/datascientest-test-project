# Stage 1: Build stage
FROM python:3.12-slim AS build

WORKDIR /app
COPY requirements.txt .
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install uv && \
    uv pip install --no-cache-dir -r requirements.txt
# Copier le dossier app local
COPY ./app /app/app/

# Stage 2: Runtime stage
FROM python:3.12-slim
WORKDIR /app
# Copy the virtual environment and application code
COPY --from=build /app /app
# Set the PATH to use the virtual environment
ENV PATH="/app/venv/bin:$PATH"
# Ajouter le répertoire au PYTHONPATH
ENV PYTHONPATH="/app:$PYTHONPATH"