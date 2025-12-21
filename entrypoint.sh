#!/bin/bash
set -e

# Wait for DB
/wait-for-db.sh db 5432

# Apply migrations
python manage.py migrate --noinput

python manage.py collectstatic --noinput

# Load initial data 
if [ ! -f "/app/.data_loaded" ]; then
    python manage.py loaddata initial_data.json || true
    touch /app/.data_loaded
fi


# exec "$@"
exec gunicorn EventHub.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --log-level info


