#!/bin/bash

echo "Stopping Game Creation API..."

# Stop FastAPI server
echo "Stopping FastAPI server..."
pkill -f uvicorn

# Stop MSSQL container
echo "Stopping MSSQL container..."
docker stop mssql_server

echo "All services stopped!"
echo ""
echo "To start again, run: ./start.sh"
