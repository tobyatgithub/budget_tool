#! /bin/bash

set -e

cd /src

# python3 manage.py test -v 2 && \
# coverage run --source='.' manage.py test -v 1
# coverage report
python3 manage.py makemigrations --noinput  # flask migrate
python3 manage.py migrate --noinput  # flask upgrade
python3 manage.py migrate authtoken
python3 manage.py collectstatic --noinput
python3 manage.py runserver 0.0.0.0:8000

# gunicorn budget_tool.wsgi:application -w 3 -b :8000