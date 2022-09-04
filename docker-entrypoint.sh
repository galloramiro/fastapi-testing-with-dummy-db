#!/bin/bash

# Run the migrations
if python /app/bin/wait_for_db.py; then
    if [ "$RUN_MIGRATIONS" = "true" ]; then
        pipenv run bash -c 'alembic upgrade head;'
        if [ "$EXIT_AFTER_MIGRATIONS" = "true" ]; then
           exit 0
        fi
    fi
    exec "$@"
else
    echo "ERROR CONNECTING TO DATABASE"
    exit 1
fi