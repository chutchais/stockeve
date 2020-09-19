#!/bin/sh

echo "Start migrations..."

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"