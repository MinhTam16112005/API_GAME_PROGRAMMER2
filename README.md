# Game Creation API

A FastAPI service that creates educational games with AI-generated distractor texts. The API accepts a game with `title`, `original_text`, and optional fields (`host`, `category`, `grade_level`), then generates exactly 3 distractor texts that resemble the original but include small inaccuracies.

## How It Works

1. **Input**: Send a POST request to `/game/create` with:
   - `title` (required): Game title
   - `original_text` (required): The correct text content
   - `host` (optional): Game host/teacher
   - `category` (optional): Subject category
   - `grade_level` (optional): Grade level (1-12)

2. **Processing**: 
   - Game is saved to MSSQL database
   - Google Gemini AI generates 3 distractor texts
   - Distractors are saved to database linked to the game

3. **Output**: Returns the complete saved game record with:
   - Game ID, title, original_text, and metadata
   - All 3 generated distractor texts
   - Creation timestamps

## Features

- **Single Game Creation Endpoint**: `POST /game/create` - Creates a game and generates 3 distractors
- **AI-Powered Distractor Generation**: Uses Google Gemini AI for intelligent distractor generation
- **Fallback System**: Rule-based distractor generation when AI is unavailable
- **MSSQL Database**: Microsoft SQL Server database for data persistence
- **Complete Game Response**: Returns the saved game with all 3 generated distractors

## Complete Setup Guide

### Prerequisites

- Python 3.8+
- Docker (for MSSQL database)
- Virtual environment (recommended)

### Step-by-Step Installation

#### 1. **Clone and Navigate**
   ```bash
   git clone <repository-url>
   cd API_GAME_PROGRAMMER2
   ```

#### 2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

#### 3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

#### 4. **Set Up MSSQL Database with Docker**

   **Start SQL Server Container:**
   ```bash
   docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourStrong@Passw0rd" -e "MSSQL_PID=Express" -p 1433:1433 --name mssql_server -d mcr.microsoft.com/mssql/server:2019-latest
   ```

   **Wait for container to start (30-60 seconds), then create database:**
   ```bash
   docker exec mssql_server /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "YourStrong@Passw0rd" -C -Q "CREATE DATABASE GameAPI;"
   ```

#### 5. **Configure Environment Variables**
   
   The `.env` file is already configured with MSSQL settings:
   ```bash
   # Database Configuration
   DATABASE_URL=mssql+pymssql://sa:YourStrong%40Passw0rd@localhost:1433/GameAPI
   
   # LLM Configuration  
   GEMINI_API_KEY=your_gemini_key
   LLM_PROVIDER=gemini
   
   # Application Configuration
   DEBUG=True
   HOST=0.0.0.0
   PORT=8000
   ```

#### 6. **Start the Application**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### 7. **Test the API**
   
   **Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```
   
   **Create a Game:**
   ```bash
   curl -X POST "http://localhost:8000/game/create" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Photosynthesis Quiz",
       "original_text": "Plants use sunlight to convert carbon dioxide and water into glucose and oxygen.",
       "host": "Science Teacher", 
       "category": "Biology",
       "grade_level": 7
     }'
   ```
   
   **Get All Games:**
   ```bash
   curl http://localhost:8000/game/
   ```

#### 8. **Access Interactive Documentation**
   - Open http://localhost:8000/docs for Swagger UI
   - Open http://localhost:8000/redoc for ReDoc

### Quick Commands Reference

**Super Easy Start (Recommended):**
```bash
# One command to start everything!
./start.sh
```

**Super Easy Stop:**
```bash
# One command to stop everything!
./stop.sh
```

**Manual Commands:**
```bash
# Start everything manually:
# 1. Start MSSQL (if not running)
docker start mssql_server

# 2. Start API
cd /Users/tam1611/Documents/Documents_folder/Gamer-task/API_GAME_PROGRAMMER2
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Stop everything manually:
# Stop API
pkill -f uvicorn

# Stop MSSQL
docker stop mssql_server
```

**Check status:**
```bash
# Check if API is running
curl http://localhost:8000/health

# Check if MSSQL is running  
docker ps | grep mssql_server
```

## API Endpoints

### Core Functionality
- **POST** `/game/create` - **Main endpoint**: Create a game with title, original_text, and optional fields, returns game with 3 generated distractors
- **GET** `/health` - Health check endpoint

### Additional Endpoints (for testing/development)
- **GET** `/game/{game_id}` - Get a specific game by ID
- **GET** `/game/` - Get all games

## Example Usage

### Create a Game

```bash
curl -X POST "http://localhost:8000/game/create" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Photosynthesis Quiz",
    "original_text": "Plants use sunlight to convert carbon dioxide and water into glucose and oxygen.",
    "host": "Science Teacher",
    "category": "Biology",
    "grade_level": 7
  }'
```

### Response

```json
{
  "id": 1,
  "title": "Photosynthesis Quiz",
  "original_text": "Plants use sunlight to convert carbon dioxide and water into glucose and oxygen.",
  "host": "Science Teacher",
  "category": "Biology",
  "grade_level": 7,
  "created_at": "2025-10-24T19:37:45.163000",
  "updated_at": "2025-10-24T19:37:45.163000",
  "distractors": [
    {
      "id": 1,
      "distractor_text": "Plants use moonlight to convert carbon dioxide and water into glucose and oxygen.",
      "created_at": "2025-10-24T19:37:45.160000"
    },
    {
      "id": 2,
      "distractor_text": "Plants use sunlight to absorb carbon dioxide and water into glucose and oxygen.",
      "created_at": "2025-10-24T19:37:45.160000"
    },
    {
      "id": 3,
      "distractor_text": "Plants use sunlight to convert carbon dioxide and water into carbon dioxide and oxygen.",
      "created_at": "2025-10-24T19:37:45.160000"
    }
  ]
}
```

## Database

The application uses **Microsoft SQL Server (MSSQL)** running in a Docker container. The database `GameAPI` is created automatically with the proper schema.

### Database Schema

**Games Table:**
- `id` (INTEGER IDENTITY - Primary Key)
- `title` (VARCHAR(255))
- `original_text` (VARCHAR(MAX))
- `host` (VARCHAR(100), Optional)
- `category` (VARCHAR(50), Optional)
- `grade_level` (INTEGER, Optional)
- `created_at` (DATETIMEOFFSET)
- `updated_at` (DATETIMEOFFSET)

**Distractors Table:**
- `id` (INTEGER IDENTITY - Primary Key)
- `game_id` (INTEGER - Foreign Key to games.id)
- `distractor_text` (VARCHAR(MAX))
- `created_at` (DATETIMEOFFSET)

### Database Connection Details

- **Server**: localhost:1433
- **Database**: GameAPI
- **Username**: sa
- **Password**: YourStrong@Passw0rd
- **Driver**: pymssql

## Configuration

### Environment Variables

- `DATABASE_URL`: MSSQL database connection string
- `GEMINI_API_KEY`: Google Gemini API key for AI distractor generation
- `LLM_PROVIDER`: LLM provider selection (gemini)
- `DEBUG`: Enable debug mode (default: True)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

### Database Configuration

The API is configured to use Microsoft SQL Server (MSSQL) by default:

1. **MSSQL Container**: Uses Docker to run SQL Server
2. **Connection**: pymssql driver for Python connectivity
3. **Database**: GameAPI database created automatically
4. **Tables**: games and distractors tables created on startup

## Development

### Project Structure

```
API_GAME_PROGRAMMER2/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py              # Configuration
│   ├── database.py            # Database setup
│   ├── models/                # SQLAlchemy models
│   │   ├── game.py
│   │   └── distractor.py
│   ├── schemas/               # Pydantic schemas
│   │   └── game.py
│   ├── services/              # Business logic
│   │   ├── game_service.py
│   │   └── llm_service.py
│   └── api/                   # API routes
│       └── game_routes.py
├── requirements.txt
├── docker-compose.yml         # SQL Server setup
└── README.md
```

### Adding New Features

1. **New Models**: Add to `app/models/`
2. **New Services**: Add to `app/services/`
3. **New Routes**: Add to `app/api/`
4. **New Schemas**: Add to `app/schemas/`

## Testing

The API includes comprehensive testing:

- Health check endpoint
- Game creation with distractor generation
- Database operations
- Fallback distractor generation

Test the API using the interactive documentation at `/docs` or with curl commands.

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check your `DATABASE_URL` configuration
   - Ensure MSSQL container is running: `docker ps | grep mssql_server`
   - Start container if needed: `docker start mssql_server`

2. **Gemini API Errors**
   - Verify your `GEMINI_API_KEY` is correct
   - Check your Google AI Studio account has credits
   - The system will fall back to rule-based generation

3. **Port Already in Use**
   - Change the port: `--port 8001`
   - Kill existing processes: `pkill -f uvicorn`

## License

MIT License - see LICENSE file for details.