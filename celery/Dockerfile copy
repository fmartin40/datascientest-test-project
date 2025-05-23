FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app

# CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
