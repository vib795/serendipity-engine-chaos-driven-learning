# Serendipity Engine - Deployment Guide

## Quick Start with Docker Compose

### Prerequisites
- Docker and Docker Compose installed
- OpenAI API key (get one at https://platform.openai.com/api-keys)

### Steps

1. **Set up your environment variables**
   ```bash
   # Edit the .env file and add your OpenAI API key
   OPENAI_API_KEY=sk-your-actual-openai-key-here
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Run database migrations** (in a new terminal)
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

4. **Access the application**
   - Frontend: http://localhost:3001
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Local Development Setup

### Backend (Python + FastAPI)

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install uv** (if not already installed)
   ```bash
   pip install uv
   ```

3. **Install dependencies**
   ```bash
   uv pip install -e .
   ```

4. **Set up environment**
   ```bash
   cp ../.env.example ../.env
   # Edit .env and add your OpenAI API key
   ```

5. **Start PostgreSQL and Redis**
   ```bash
   docker-compose up db redis
   ```

6. **Run migrations**
   ```bash
   uv run alembic upgrade head
   ```

7. **Start the backend server**
   ```bash
   uv run uvicorn app.main:app --reload
   ```

### Frontend (Next.js + TypeScript)

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment**
   ```bash
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

## Testing the Application

1. **Visit http://localhost:3001**

2. **Click the "Generate Connection" button**

3. **Watch as the AI finds unexpected connections between random topics!**

## Troubleshooting

### Common Issues

**"OpenAI API key is required" error**
- Make sure you've added your OpenAI API key to the `.env` file
- Restart the Docker containers after adding the key

**Database connection errors**
- Ensure PostgreSQL is running: `docker-compose up db`
- Check that migrations have been run: `docker-compose exec backend alembic upgrade head`

**Frontend can't connect to backend**
- Check that the backend is running on port 8000
- Verify NEXT_PUBLIC_API_URL in `.env.local` points to `http://localhost:8000`

**Port already in use errors**
- Stop any services using ports 3000, 8000, 5432, or 6379
- Or modify the port mappings in `docker-compose.yml`

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    User's Browser                        │
│                  (http://localhost:3001)                 │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                 Next.js Frontend                         │
│  - React components with Framer Motion animations       │
│  - Tailwind CSS styling                                 │
│  - React Query for state management                     │
└─────────────────────┬───────────────────────────────────┘
                      │ REST API calls
                      ▼
┌─────────────────────────────────────────────────────────┐
│                 FastAPI Backend                          │
│  - RESTful API endpoints                                │
│  - Connection generation logic                          │
│  - External API integrations                            │
└──────┬──────────────┬──────────────┬───────────────────┘
       │              │              │
       ▼              ▼              ▼
┌───────────┐  ┌──────────┐  ┌─────────────────────────┐
│PostgreSQL │  │  Redis   │  │  External APIs          │
│ Database  │  │  Cache   │  │  - Wikipedia            │
│           │  │          │  │  - PokéAPI              │
│           │  │          │  │  - Open Trivia DB       │
│           │  │          │  │  - Facts, Numbers, etc. │
└───────────┘  └──────────┘  └─────────────────────────┘
                      │
                      ▼
               ┌─────────────┐
               │  OpenAI API │
               │  (GPT-4)    │
               └─────────────┘
```

## Key Features Implemented

1. **Random Topic Fetching**: Pulls from 6 diverse external APIs
2. **AI Connection Generation**: Uses GPT-4 to find genuine intellectual bridges
3. **Beautiful UI**: Gradient effects, smooth animations, responsive design
4. **Database Persistence**: Saves all topics and connections
5. **Docker Support**: Easy deployment with docker-compose
6. **API Documentation**: Auto-generated Swagger/OpenAPI docs

## Next Steps

- Add user authentication
- Implement favorites functionality
- Create connection chains (A→B→C)
- Add sharing with social metadata
- Implement pre-generation queue for instant delivery
- Add connection quality voting

## API Endpoints

### Generate Connection
```bash
curl -X POST http://localhost:8000/api/v1/connections/generate
```

### Get Connection by ID
```bash
curl http://localhost:8000/api/v1/connections/{connection_id}
```

### List Connections
```bash
curl http://localhost:8000/api/v1/connections/?skip=0&limit=10
```

### Get Popular Connections
```bash
curl http://localhost:8000/api/v1/connections/popular?limit=10
```

## Production Deployment

For production deployment:

1. **Use production-grade secrets**
   - Generate a strong SECRET_KEY
   - Use environment-specific API keys

2. **Configure CORS properly**
   - Update CORS_ORIGINS to include your production domain

3. **Use managed databases**
   - Consider using AWS RDS, Google Cloud SQL, or similar for PostgreSQL
   - Use Redis Cloud or ElastiCache for Redis

4. **Enable SSL/TLS**
   - Use HTTPS for all connections
   - Configure SSL certificates

5. **Set up monitoring**
   - Use tools like Sentry for error tracking
   - Monitor API usage and costs

6. **Optimize AI usage**
   - Implement rate limiting
   - Use connection pre-generation
   - Consider caching popular connections

---

*Happy discovering! May you find many serendipitous connections!*
