#!/bin/sh

# python manage.py flush --no-input
python manage.py migrate
python manage.py loaddata utils/genres_fixture.json
python manage.py loaddata utils/books_fixture.json
# python manage.py collectstatic --no-input --clear
gunicorn --bind :8000 --workers 3 setup.wsgi:application

exec "$@"