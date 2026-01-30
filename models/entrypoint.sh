#!/bin/bash
set -e

export OLLAMA_HOST=127.0.0.1:11434

ollama serve &
echo "Waiting for Ollama..."

while ! nc -z localhost 11434; do
  sleep 1
done

#Here we are writing in one folder and in one space but if you are using this code YOU CAN FACE MEMORY ISSUES SO BE CAREFULL HERE.
ollama pull llama3.2
ollama pull qwen2.5-coder:7b
ollama pull falcon:7b-instruct
ollama pull codellama:7b-instruct
ollama pull internlm2:7b
ollama pull maxkb/baichuan2:13b-chat
ollama pull vicuna:7b
ollama pull gemma2:9b
ollama pull mistral:7b
ollama pull phi3:medium

echo "Starting FastAPI..."
exec python3 -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-7860}
