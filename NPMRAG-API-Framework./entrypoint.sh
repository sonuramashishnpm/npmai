#!/bin/bash
set -e

export OLLAMA_HOST=127.0.0.1:11434

ollama serve &
echo "Waiting for Ollama..."

while ! nc -z localhost 11434; do
  sleep 1
done

ollama pull llama3.2
ollama pull qwen2.5-coder:7b

echo "Starting FastAPI..."
exec python3 -m uvicorn app:app --host 0.0.0.0 --port ${PORT:-7860}
