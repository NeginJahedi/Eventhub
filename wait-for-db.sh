#!/bin/bash
# Usage: ./wait-for-db.sh host port
set -e

host="$1"
port="$2"
retries=30

until nc -z "$host" "$port"; do
  echo "Waiting for database at $host:$port..."
  retries=$((retries-1))
  if [ $retries -le 0 ]; then
    echo "Database did not become available in time"
    exit 1
  fi
  sleep 1
done

echo "Database is up"
