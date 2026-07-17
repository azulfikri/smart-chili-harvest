#!/bin/sh
set -e

# Initialize database if it doesn't exist yet
python -m app.database.init_db

# Start the FastAPI server
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
