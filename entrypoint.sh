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

GUNICORN_CMD="gunicorn --bind 0.0.0.0:${PORT:-5000} --workers ${GUNICORN_WORKERS:-4} application:application"

if [ -n "${NEW_RELIC_LICENSE_KEY:-}" ] && [ -n "${NEW_RELIC_APP_NAME:-}" ]; then
  echo "New Relic configuration detected. Starting app with New Relic instrumentation..."
  exec newrelic-admin run-program $GUNICORN_CMD
else
  echo "No New Relic license key or app name found. Starting app without New Relic."
  exec $GUNICORN_CMD
fi