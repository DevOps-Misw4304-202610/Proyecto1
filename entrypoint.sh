#!/bin/sh
set -eu

echo "Running database migrations..."

max_attempts="${DB_MIGRATION_RETRIES:-12}"
sleep_seconds="${DB_MIGRATION_RETRY_DELAY:-5}"

attempt=1
while [ "$attempt" -le "$max_attempts" ]; do
  if flask db upgrade; then
    echo "Database migrations completed successfully."
    break
  fi

  if [ "$attempt" -eq "$max_attempts" ]; then
    echo "Database migrations failed after ${max_attempts} attempts."
    exit 1
  fi

  echo "Migration attempt ${attempt} failed. Retrying in ${sleep_seconds}s..."
  attempt=$((attempt + 1))
  sleep "$sleep_seconds"
done

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:${PORT:-8000} --workers ${GUNICORN_WORKERS:-4} application:application