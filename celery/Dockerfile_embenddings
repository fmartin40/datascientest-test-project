FROM python:3.12-slim

# 1. Install system dependencies (minimal)
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. Set env vars to avoid cache downloads and prompts
ENV TRANSFORMERS_CACHE=/app/model_cache \
    HF_HOME=/app/model_cache \
    TORCH_HOME=/app/model_cache \
    PYTHONUNBUFFERED=1

# 3. Copy requirements first to leverage Docker cache
COPY requirements.txt /app/requirements.txt

WORKDIR /app

# 4. Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Preload only the needed model
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('distiluse-base-multilingual-cased-v2')"

# 6. Copy app source
COPY . /app

CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
