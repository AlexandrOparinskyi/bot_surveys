FROM python:3.12.0

WORKDIR app/

COPY database/ database/
COPY config.py /app
COPY static static/
COPY templates templates/

RUN pip install --no-cache-dir fastapi sqladmin sqlalchemy asyncpg gunicorn environs uvicorn python-slugify jinja2