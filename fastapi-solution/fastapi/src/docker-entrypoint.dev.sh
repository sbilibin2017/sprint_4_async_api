#!/bin/bash

echo "Waiting for redis..."
while ! nc -z redis $REDIS_PORT; do
  sleep 1
done
echo "Redis started"

echo "Waiting for elasticsearch..."
while ! nc -z elasticsearch $ELASTIC_PORT; do
  sleep 1
done
echo "Elasticsearch started"

python3 main.py

