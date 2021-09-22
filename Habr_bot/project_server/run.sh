#!/bin/bash

set -e
alembic revision -m "first" --autogenerate --head head
alembic upgrade head
python main.py