#!/bin/bash

echo "Waiting for Ollama to be ready..."
until curl --output /dev/null --silent --fail http://localhost:11434/api/version; do
    printf "."
    sleep 5
done

echo -e "\nPulling Mistral model..."
curl -X POST http://localhost:11434/api/pull \
    -H "Content-Type: application/json" \
    -d '{"name":"mistral:instruct"}'

echo -e "\nModel initialized successfully!"