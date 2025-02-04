#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Wait for postgres
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "Waiting for postgres..."
  sleep 1
done

echo "PostgreSQL started"

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver 0.0.0.0:8000