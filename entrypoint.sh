#!/bin/sh

# Wait for postgres
until nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    echo "Waiting for postgres..."
    sleep 1
done

echo "PostgreSQL started"

# Create DCRT directory if it doesn't exist and set permissions
# Assuming the container runs as user ID 1000 (adjust if different)
mkdir -p /code/DCRT
chown -R 1000:1000 /code/DCRT
chmod -R 755 /code/DCRT
# Note: Keep media dir creation if other parts of the app use it
mkdir -p /code/media
chown -R 1000:1000 /code/media
chmod -R 755 /code/media

# Run migrations
python manage.py migrate

# Start server
exec python manage.py runserver 0.0.0.0:8005