FROM python:3.12-slim

EXPOSE 8000

RUN useradd service -m
RUN pip install --upgrade pip poetry

USER service
WORKDIR /app

RUN chown -R service /app

COPY . .

RUN poetry install --no-root

ENV DJANGO_SETTINGS_MODULE=cornern.settings

CMD ["bash", "./deployment/start.sh"]
