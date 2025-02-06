#!/bin/sh

# Wait for postgres
until nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo "Waiting for postgres..."
    sleep 1
done

echo "PostgreSQL started"

# Run migrations
python manage.py migrate

# Start server
exec python manage.py runserver 0.0.0.0:8005