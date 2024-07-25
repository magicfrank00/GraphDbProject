#!/usr/bin/env bash
# wait-for-it.sh

set -e

sleep="$1"
shift

echo "Waiting for $sleep seconds"
sleep $sleep

exec "$@"