FROM python:3

WORKDIR /innotter_django

COPY . .

RUN chmod +x django_entrypoint.sh celery_entrypoint.sh
RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry install
