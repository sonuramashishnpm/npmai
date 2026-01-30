#!/bin/bash

# Exit if anything fails
set -e

# Optional: any setup commands you need
echo "Starting FastAPI server..."

# Start the FastAPI server on the port specified by HF Spaces
uvicorn app:app --host 0.0.0.0 --port $PORT
