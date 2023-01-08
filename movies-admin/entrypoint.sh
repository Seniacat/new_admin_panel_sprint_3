#!/bin/bash

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py compilemessages -l en -l ru
python manage.py loaddata 'fixtures.json'
uwsgi --strict --ini uwsgi.ini