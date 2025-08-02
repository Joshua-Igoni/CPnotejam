#!/bin/sh
set -e

# Wait for Postgres to accept connections
echo "⏳ Waiting for Postgres at $POSTGRES_HOST:$POSTGRES_PORT..."
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  sleep 1
done
echo "Postgres is up ✔"
python notejam/manage.py migrate --noinput

exec "$@"