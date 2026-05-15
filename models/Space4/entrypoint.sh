#!/bin/bash
set -e

export OLLAMA_HOST=127.0.0.1:11434

ollama serve &
echo "Waiting for Ollama..."

while ! nc -z localhost 11434; do
  sleep 1
done

ollama pull phi3:medium

echo "Starting FastAPI..."
exec python3 -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-7860}
