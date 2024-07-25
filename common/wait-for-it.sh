#!/usr/bin/env bash
# wait-for-it.sh

set -e

host="$1"
shift
port="$1"
shift

# if [ "$DB_TYPE" != "neo" ]; then
#   echo "DB_TYPE is not neo, skipping wait-for-it.sh"
#   exec "$@"
# fi

echo "Waiting for $host:$port"
until nc -z "$host" "$port"; do
  >&2 echo "Service $host:$port is unavailable - sleeping"
  sleep 1
done

>&2 echo "Service $host:$port is up - executing command"
exec "$@"
