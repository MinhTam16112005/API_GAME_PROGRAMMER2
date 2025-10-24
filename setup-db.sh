#!/bin/bash

echo "Setting up SQL Server with Docker..."

# Start SQL Server
docker-compose up -d

echo "Waiting for SQL Server to be ready..."
sleep 30

echo "Creating database..."
docker exec -it game_api_sqlserver /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "YourStrong@Passw0rd" -Q "CREATE DATABASE GameAPI;"

echo "Database setup complete!"
echo ""
echo "Connection details:"
echo "   Server: localhost:1433"
echo "   Database: GameAPI"
echo "   Username: sa"
echo "   Password: YourStrong@Passw0rd"
echo ""
echo "Update your .env file with:"
echo "   DATABASE_URL=mssql+pyodbc://sa:YourStrong@Passw0rd@localhost:1433/GameAPI"
