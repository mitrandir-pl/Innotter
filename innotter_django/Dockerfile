FROM python:3

WORKDIR /innotter_django

COPY . .

RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry install
