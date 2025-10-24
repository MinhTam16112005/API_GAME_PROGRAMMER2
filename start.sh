#!/bin/bash

echo "Starting Game Creation API with MSSQL..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running. Please start Docker first."
    exit 1
fi

# Check if MSSQL container exists and start it
if docker ps -a --format "table {{.Names}}" | grep -q "mssql_server"; then
    echo "Starting existing MSSQL container..."
    docker start mssql_server
else
    echo "Creating new MSSQL container..."
    docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourStrong@Passw0rd" -e "MSSQL_PID=Express" -p 1433:1433 --name mssql_server -d mcr.microsoft.com/mssql/server:2019-latest
    
    echo "Waiting for SQL Server to start (30 seconds)..."
    sleep 30
    
    echo "Creating GameAPI database..."
    docker exec mssql_server /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "YourStrong@Passw0rd" -C -Q "CREATE DATABASE GameAPI;" || echo "Database might already exist"
fi

# Wait a bit for SQL Server to be ready
echo "Waiting for SQL Server to be ready..."
sleep 10

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Start the API
echo "Starting FastAPI server..."
echo "API will be available at: http://localhost:8000"
echo "Interactive docs at: http://localhost:8000/docs"
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
