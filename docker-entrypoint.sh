#!/bin/sh

set -e

echo "Waiting for database"
while ! mysqladmin ping -h db --silent; do
  >&2 echo -n "."
  sleep 1
done
echo "Database ready for connections."

echo "Migrating Database"
python manage.py migrate
python manage.py flush --noinput

echo "Starting bCTF."
exec gunicorn --chdir /app/ \
    bctf.wsgi \
    --workers=4 \
    --bind 0.0.0.0:8000