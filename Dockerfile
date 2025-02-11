# Dockerfile

# pull the official docker image
FROM python:3.12-alpine

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]