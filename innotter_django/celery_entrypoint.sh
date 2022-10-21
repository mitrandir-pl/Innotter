#!/bin/bash
poetry run celery -A core worker -l INFO
