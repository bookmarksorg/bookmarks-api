#!/bin/sh

# python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input --clear
python manage.py loaddata utils/books_fixture.json
python manage.py loaddata utils/genres_fixture.json

exec "$@"