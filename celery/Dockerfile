# Stage 1: Build stage
FROM python:3.9-slim AS build

WORKDIR /app
COPY requirements.txt .
RUN python -m venv venv && . venv/bin/activate && pip install --no-cache-dir -r requirements.txt
# COPY /worker/ /worker/
COPY ./app /app/

# Stage 2: Runtime stage
FROM python:3.9-slim
WORKDIR /app
# Copy the virtual environment and application code
COPY --from=build /app /app
# Set the PATH to use the virtual environment
ENV PATH="/app/venv/bin:$PATH"
# Run the Celery worker
# CMD ["celery", "-A", "tasks", "worker", "-l", "info"]
# CMD ["celery", "-A", "tasks", "app.workers", "--loglevel=INFO", "--logfile=/logs/worker.log"]