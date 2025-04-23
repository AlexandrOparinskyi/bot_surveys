FROM python:3.12.0

RUN mkrid uploads

WORKDIR app/

COPY database/ database/
COPY config.py /app

RUN pip install --no-cache-dir fastapi sqladmin sqlalchemy asyncpg gunicorn environs uvicorn python-slugify