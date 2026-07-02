#!/usr/bin/env bash
set -e

echo "OIIA Cat Meme Generator"

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

PORT=3000
if lsof -i :$PORT >/dev/null 2>&1; then
    echo "Port $PORT in use, killing existing process..."
    kill $(lsof -t -i :$PORT) 2>/dev/null || true
    sleep 1
fi

echo "Starting server on http://localhost:$PORT"
node server.js
