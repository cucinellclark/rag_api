#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Use the venv's python/uvicorn directly to avoid activation issues under PM2
VENV="$SCRIPT_DIR/rag_env"
PYTHON="$VENV/bin/python3"
UVICORN="$VENV/bin/uvicorn"

PORT=${RAG_API_PORT:-$("$PYTHON" -c "import json; print(json.load(open('config.json')).get('port', 8001))")}
exec "$UVICORN" app.main:app --host 0.0.0.0 --port "$PORT"
