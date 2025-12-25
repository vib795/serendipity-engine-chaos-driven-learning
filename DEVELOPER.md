# Serendipity Engine - Developer Guide

This guide provides detailed information about the architecture, implementation, and development workflow for the Serendipity Engine.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Backend Architecture](#backend-architecture)
- [Frontend Architecture](#frontend-architecture)
- [Database Schema](#database-schema)
- [API Integration](#api-integration)
- [Error Handling](#error-handling)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Common Issues and Solutions](#common-issues-and-solutions)

## Architecture Overview

The Serendipity Engine is a full-stack application built with a FastAPI backend and Next.js frontend, designed to generate unexpected intellectual connections between topics.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Next.js Frontend (Port 3001)              │
│  ┌─────────────┬──────────────┬─────────────────────────┐  │
│  │  Pages      │  Components   │  Services & Hooks       │  │
│  │  - page.tsx │  - Connection │  - connectionService.ts │  │
│  │             │  - Topic      │  - useGenerate...ts     │  │
│  └─────────────┴──────────────┴─────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/REST API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 FastAPI Backend (Port 8000)                  │
│  ┌──────────────┬─────────────────┬─────────────────────┐  │
│  │ API Routes   │  Services        │  Models & Schemas   │  │
│  │ - connections│  - topic_fetcher │  - Connection       │  │
│  │              │  - conn_gen      │  - Topic            │  │
│  │              │  - external APIs │  - User, Favorites  │  │
│  └──────────────┴─────────────────┴─────────────────────┘  │
└────┬─────────────────┬──────────────────┬──────────────────┘
     │                 │                  │
     ▼                 ▼                  ▼
┌──────────┐    ┌──────────┐      ┌────────────────────┐
│PostgreSQL│    │  Redis   │      │  External APIs     │
│ Database │    │  Cache   │      │  - Wikipedia       │
│          │    │          │      │  - PokéAPI         │
│          │    │          │      │  - Trivia DB       │
│          │    │          │      │  - Facts, Numbers  │
└──────────┘    └──────────┘      └────────────────────┘
                                           │
                                           ▼
                                    ┌──────────────┐
                                    │ OpenAI GPT-4 │
                                    └──────────────┘
```

## Backend Architecture

### Technology Stack

- **Framework**: FastAPI (async/await support)
- **Package Manager**: uv (modern Python package manager)
- **Database**: PostgreSQL with SQLAlchemy (async)
- **Migrations**: Alembic
- **HTTP Client**: httpx (async)
- **AI Integration**: OpenAI API or Anthropic Claude

### Directory Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Settings and configuration
│   ├── database.py             # Database connection
│   ├── api/
│   │   ├── __init__.py
│   │   └── connections.py      # Connection endpoints
│   ├── models/
│   │   ├── connection.py       # Connection database model
│   │   ├── topic.py            # Topic database model
│   │   ├── user.py             # User database model
│   │   └── favorite.py         # Favorite database model
│   ├── schemas/
│   │   ├── connection.py       # Connection Pydantic schemas
│   │   └── topic.py            # Topic Pydantic schemas
│   └── services/
│       ├── topic_fetcher.py    # Aggregates topics from all sources
│       ├── connection_generator.py  # AI connection generation
│       └── external/           # External API integrations
│           ├── wikipedia.py
│           ├── pokemon.py
│           ├── trivia.py
│           ├── facts.py
│           ├── numbers.py
│           └── quotes.py
├── alembic/
│   ├── versions/
│   │   └── 001_initial.py      # Initial schema migration
│   └── env.py
├── pyproject.toml              # Python dependencies
└── Dockerfile
```

### Key Components

#### 1. Connection Generation Flow

```python
# backend/app/api/connections.py

@router.post("/generate")
async def generate_connection():
    # 1. Fetch two random topics from different sources
    topic_a, topic_b = await topic_fetcher.fetch_topic_pair()

    # 2. Save topics to database (with duplicate checking)
    topic_a_model = await save_or_get_topic(topic_a)
    topic_b_model = await save_or_get_topic(topic_b)

    # 3. Generate AI connection
    generated = await connection_generator.generate_connection(topic_a, topic_b)

    # 4. Save connection to database
    connection_model = await save_connection(generated)

    # 5. Return response
    return GenerateConnectionResponse(...)
```

#### 2. Topic Fetcher Service

The `TopicFetcher` service aggregates topics from multiple external APIs with weighted random selection and automatic retry logic.

```python
# backend/app/services/topic_fetcher.py

class TopicFetcher:
    def __init__(self, services: dict):
        self.services = services
        # Weighted selection for better diversity
        self.source_weights = {
            TopicSource.WIKIPEDIA: 2.0,
            TopicSource.POKEMON: 1.5,
            TopicSource.TRIVIA: 2.0,
            # ... more sources
        }

    async def fetch_random_topic(self, max_retries: int = 3) -> Topic:
        """Fetch with automatic retry and fallback."""
        for attempt in range(max_retries):
            try:
                selected_source = weighted_random(self.source_weights)
                topic = await self.services[selected_source].fetch_random()
                return topic
            except Exception as e:
                # Try next source on failure
                continue
```

**Key Features**:
- Weighted random selection favors high-quality sources
- Automatic retry with fallback (up to 3 attempts)
- Source exclusion to ensure diversity
- SSL verification disabled in development mode

#### 3. Custom vs Random Topics

The application supports two modes:

**Random Mode** (`/api/v1/connections/generate`):
- Fetches topics from external APIs
- Ensures topics come from different sources
- Uses `source_id` from external API

**Custom Mode** (`/api/v1/connections/generate-custom`):
- User provides topic titles
- Creates topics with `source_id=None`
- Uses `category="Custom"` for identification
- Duplicate checking uses `(source, title, category)`

```python
# Custom topic creation
topic_data = TopicData(
    source=TopicSource.WIKIPEDIA,  # Default source
    source_id=None,                # No external ID
    title=custom_input,
    summary=custom_input,
    category="Custom",             # Mark as custom
    tags=["custom", "user-provided"],
)

# Custom duplicate checking
existing = await db.execute(
    select(TopicModel).where(
        TopicModel.source == source,
        TopicModel.title == title,
        TopicModel.category == "Custom",  # Include category
    )
)
```

#### 4. Error Handling Strategy

**SSL Certificate Errors**:
```python
# Disabled in development mode
verify_ssl = not settings.debug
http_client = httpx.AsyncClient(verify=verify_ssl)
```

**API Timeout/Failure**:
```python
# Automatic retry with exponential backoff
for attempt in range(max_retries):
    try:
        return await external_api_call()
    except Exception as e:
        if attempt < max_retries - 1:
            await asyncio.sleep(2 ** attempt)
        continue
```

**Database Constraints**:
```python
# Check for duplicates before insertion
existing = await db.execute(
    select(Model).where(unique_conditions)
)
if existing:
    return existing
else:
    db.add(new_model)
```

## Frontend Architecture

### Technology Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **State Management**: React Query (@tanstack/react-query)
- **HTTP Client**: Axios

### Directory Structure

```
frontend/
├── app/
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Homepage (main UI)
│   └── globals.css             # Global styles
├── components/
│   ├── connection/
│   │   ├── ConnectionDisplay.tsx
│   │   ├── GenerateButton.tsx
│   │   └── TopicBubble.tsx
│   └── animations/
│       └── ThinkingAnimation.tsx
├── hooks/
│   └── useGenerateConnection.ts  # Main connection hook
├── services/
│   ├── api.ts                  # Axios instance
│   └── connectionService.ts    # API service layer
├── types/
│   └── connection.ts           # TypeScript types
└── package.json
```

### Key Components

#### 1. Main Page Component

```typescript
// frontend/app/page.tsx

export default function HomePage() {
  const { connection, topicA, topicB, isGenerating, generate, generateCustom } =
    useGenerateConnection();

  const [mode, setMode] = useState<'random' | 'custom'>('random');
  const [customTopicA, setCustomTopicA] = useState('');
  const [customTopicB, setCustomTopicB] = useState('');

  const handleGenerate = () => {
    if (mode === 'random') {
      generate();
    } else {
      generateCustom(customTopicA, customTopicB);
    }
  };

  return (
    // UI with mode toggle, input fields, and connection display
  );
}
```

#### 2. Connection Hook

```typescript
// frontend/hooks/useGenerateConnection.ts

export function useGenerateConnection() {
  const [connection, setConnection] = useState<Connection | null>(null);
  const [topicA, setTopicA] = useState<Topic | null>(null);
  const [topicB, setTopicB] = useState<Topic | null>(null);

  const randomMutation = useMutation({
    mutationFn: connectionService.generateConnection,
    onSuccess: (data) => {
      setTopicA(data.topic_a);
      setTopicB(data.topic_b);
      setConnection(data.connection);
    },
  });

  const customMutation = useMutation({
    mutationFn: ({ topicA, topicB }) =>
      connectionService.generateCustomConnection(topicA, topicB),
    onSuccess: (data) => {
      // Same as random
    },
  });

  return {
    connection,
    topicA,
    topicB,
    isGenerating: randomMutation.isPending || customMutation.isPending,
    generate: () => randomMutation.mutate(),
    generateCustom: (a, b) => customMutation.mutate({ topicA: a, topicB: b }),
  };
}
```

#### 3. API Service Layer

```typescript
// frontend/services/connectionService.ts

export const connectionService = {
  async generateConnection(): Promise<GenerateConnectionResponse> {
    const response = await api.post('/connections/generate');
    return response.data;
  },

  async generateCustomConnection(topicA: string, topicB: string) {
    const response = await api.post('/connections/generate-custom', {
      topic_a: topicA,
      topic_b: topicB,
    });
    return response.data;
  },
};
```

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐         ┌──────────────────┐
│     Topics      │◄────────│   Connections    │
│─────────────────│         │──────────────────│
│ id (UUID) PK    │         │ id (UUID) PK     │
│ source          │         │ topic_a_id FK    │
│ source_id       │         │ topic_b_id FK    │
│ title           │         │ connection_title │
│ summary         │         │ connection_summary│
│ category        │         │ creativity_score │
│ tags[]          │         │ model_used       │
│ created_at      │         │ created_at       │
└─────────────────┘         └──────────────────┘
                                     ▲
                                     │
                            ┌────────┴────────┐
                            │                 │
                    ┌───────┴────────┐  ┌─────┴──────┐
                    │   Favorites    │  │   Users    │
                    │────────────────│  │────────────│
                    │ id (UUID) PK   │  │ id (UUID)  │
                    │ user_id FK     │  │ email      │
                    │ connection_id  │  │ username   │
                    │ created_at     │  │ created_at │
                    └────────────────┘  └────────────┘
```

### Key Constraints

**Unique Constraints**:
- `(source, source_id)` on Topics table - Prevents duplicate external topics
- `(topic_a_id, topic_b_id)` on Connections table - Prevents duplicate connections
- `(user_id, connection_id)` on Favorites table - One favorite per user per connection

**Why Custom Topics Work**:
- Custom topics have `source_id=None`
- Duplicate check uses `(source, title, category)` instead of `(source, source_id)`
- This allows multiple custom topics with different titles

### Migration Management

```bash
# Create new migration
cd backend
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback one version
uv run alembic downgrade -1

# View migration history
uv run alembic history
```

## API Integration

### External APIs

| API | Purpose | Rate Limit | Retry Logic |
|-----|---------|------------|-------------|
| Wikipedia | General knowledge | None | 3 retries |
| PokéAPI | Pop culture | None | 3 retries |
| Open Trivia DB | Facts | None | 3 retries |
| Useless Facts | Interesting tidbits | None | 3 retries |
| Numbers API | Math/number facts | None | 3 retries |
| Quotable | Philosophical quotes | None | 3 retries |
| OpenAI GPT-4 | AI connections | RPM based | No retry |

### Adding a New External API

1. Create service in `backend/app/services/external/`:

```python
# backend/app/services/external/new_api.py

class NewAPIService:
    def __init__(self, http_client: httpx.AsyncClient):
        self.http = http_client
        self.base_url = "https://api.example.com"

    async def fetch_random(self) -> Topic:
        response = await self.http.get(f"{self.base_url}/random")
        data = response.json()

        return Topic(
            source=TopicSource.NEW_API,
            source_id=data["id"],
            title=data["title"],
            summary=data["description"],
            # ... map other fields
        )
```

2. Add to `TopicSource` enum:

```python
# backend/app/services/topic_fetcher.py

class TopicSource(str, Enum):
    WIKIPEDIA = "wikipedia"
    # ... existing sources
    NEW_API = "new_api"
```

3. Register in `TopicFetcher`:

```python
# backend/app/main.py

app.state.topic_fetcher = TopicFetcher(
    # ... existing services
    new_api_service=NewAPIService(http),
)
```

## Error Handling

### Backend Error Handling

**HTTPException for Client Errors**:
```python
from fastapi import HTTPException

if not found:
    raise HTTPException(status_code=404, detail="Connection not found")
```

**Try/Except for External APIs**:
```python
try:
    topic = await external_api.fetch_random()
except httpx.TimeoutException:
    # Retry with different source
    pass
except Exception as e:
    logger.error(f"API error: {e}")
    # Fallback logic
```

### Frontend Error Handling

**React Query Error Handling**:
```typescript
const mutation = useMutation({
  mutationFn: connectionService.generateConnection,
  onError: (err: Error) => {
    setError(err.message || 'Failed to generate connection');
  },
});
```

**Input Validation**:
```typescript
const generateCustom = (topicA: string, topicB: string) => {
  if (!topicA.trim() || !topicB.trim()) {
    setError('Please enter both topics');
    return;
  }
  customMutation.mutate({ topicA, topicB });
};
```

## Development Workflow

### Setting Up Development Environment

1. **Clone and setup**:
```bash
git clone <repo-url>
cd serendipity-engine-chaos-driven-learning
cp .env.example .env
# Edit .env with your API keys
```

2. **Start with Docker Compose**:
```bash
docker-compose up --build
```

3. **Run migrations**:
```bash
docker-compose exec backend alembic upgrade head
```

4. **Access services**:
- Frontend: http://localhost:3001
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Local Development (Without Docker)

**Backend**:
```bash
cd backend
uv sync
docker-compose up db redis  # Just DB and Redis
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

### Code Style

**Backend**:
- Use `ruff` for linting
- Use `black` for formatting
- Line length: 100 characters
- Type hints required for public functions

**Frontend**:
- Use ESLint + Prettier
- TypeScript strict mode
- Functional components with hooks

### Git Workflow

1. Create feature branch from `main`:
```bash
git checkout -b feature/custom-topics
```

2. Make changes and commit:
```bash
git add .
git commit -m "feat: add custom topic input feature"
```

3. Push and create PR:
```bash
git push origin feature/custom-topics
```

## Testing

### Backend Testing

```bash
cd backend
uv run pytest

# With coverage
uv run pytest --cov=app

# Specific test
uv run pytest tests/test_connections.py
```

### Frontend Testing

```bash
cd frontend
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage
```

### Manual Testing Checklist

- [ ] Random connection generation works
- [ ] Custom topic input works
- [ ] Mode toggle switches correctly
- [ ] Error messages display properly
- [ ] Animations are smooth
- [ ] Database persists connections
- [ ] Duplicate topics are reused
- [ ] API documentation is accessible

## Common Issues and Solutions

### Issue: Database Migration Fails

**Symptom**: `relation "topics" does not exist`

**Solution**:
```bash
docker-compose exec backend alembic upgrade head
```

### Issue: SSL Certificate Errors

**Symptom**: `certificate verify failed: certificate has expired`

**Solution**: Set `DEBUG=true` in `.env` to disable SSL verification in development.

### Issue: Custom Topics Duplicate Error

**Symptom**: `duplicate key value violates unique constraint "idx_topics_source_id"`

**Solution**: Ensure custom topics use `source_id=None` and duplicate checking includes `category="Custom"`.

### Issue: Frontend Can't Connect

**Symptom**: CORS errors or connection refused

**Solution**:
1. Check `CORS_ORIGINS` in `.env` includes `http://localhost:3001`
2. Verify backend is running on port 8000
3. Check `NEXT_PUBLIC_API_URL` in frontend

### Issue: External API Timeouts

**Symptom**: All external APIs failing

**Solution**: Check internet connection. The retry logic should handle occasional failures automatically.

## Performance Optimization

### Backend Optimization

1. **Database Indexing**: Indexes on frequently queried fields
```sql
CREATE INDEX idx_connections_created_at ON connections(created_at);
CREATE INDEX idx_topics_source ON topics(source);
```

2. **Connection Pooling**: SQLAlchemy handles automatically

3. **Caching** (Future): Redis for topic caching
```python
cached = await redis.get(f"topic:{source}:{id}")
if cached:
    return Topic.parse_raw(cached)
```

### Frontend Optimization

1. **React Query Caching**: Automatic stale-while-revalidate
2. **Code Splitting**: Next.js automatic route-based splitting
3. **Image Optimization**: Next.js Image component (when images added)

## Security Considerations

1. **API Keys**: Never commit to repository, use `.env`
2. **SQL Injection**: SQLAlchemy ORM prevents by default
3. **XSS**: React escapes by default
4. **CORS**: Configured for specific origins only
5. **Rate Limiting**: Implement for production (TODO)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Ensure all tests pass
5. Submit a pull request

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Framer Motion Documentation](https://www.framer.com/motion/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)

---

*Happy coding! May your connections be serendipitous!*
