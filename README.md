# ✨ Serendipity Engine

> **Innovation begins where ideas collide.**

A chaos-driven learning application that generates unexpected intellectual connections between completely unrelated topics. Discover surprising bridges between random domains like "What do quantum entanglement and Pikachu's origin story have in common?" or "The hidden link between Medieval bread-making and Bitcoin mining."

## 🎯 Core Philosophy

Innovation often comes from unexpected connections. We're automating serendipity — the happy accidents that lead to breakthrough ideas.

## 🔮 The Magic

The app fetches random data from multiple unrelated APIs (Wikipedia, Pokémon, trivia databases, number facts, quotes, and more), then uses AI to find genuine, intellectually satisfying connections between them. Not forced jokes, but real conceptual bridges that make you say "Huh, I never thought of it that way."

## 🛠️ Technical Stack

### Backend
- **Framework:** FastAPI
- **Package Manager:** uv (modern Python package manager)
- **Python Version:** 3.11+
- **Database:** PostgreSQL with SQLAlchemy ORM + Alembic migrations
- **Caching:** Redis for API response caching and rate limiting
- **AI Integration:** OpenAI API (GPT-4) or Anthropic Claude API
- **Task Queue:** Celery with Redis broker
- **API Documentation:** Auto-generated OpenAPI/Swagger

### Frontend
- **Framework:** Next.js 14+ with TypeScript (App Router)
- **Styling:** Tailwind CSS + Framer Motion for animations
- **State Management:** Zustand + React Query
- **UI Components:** Radix UI primitives + custom components
- **Icons:** Lucide React

### Infrastructure
- **Containerization:** Docker + Docker Compose
- **Environment:** .env files for configuration

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 20+ (if running frontend locally)
- Python 3.11+ with uv (if running backend locally)
- OpenAI API key or Anthropic API key

### Running with Docker Compose

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd serendipity-engine-chaos-driven-learning
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. **Start the application:**
   ```bash
   docker-compose up
   ```

4. **Access the application:**
   - Frontend: http://localhost:3001
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Running Locally (Development)

#### Backend

```bash
cd backend

# Install uv if not already installed
pip install uv

# Install dependencies
uv sync

# Run database migrations
uv run alembic upgrade head

# Start the server
uv run uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

## 🎨 Features

- **One-Click Serendipity:** Generate random connections with a single click
- **Multi-Source Topics:** Pulls from Wikipedia, Pokémon, trivia, facts, numbers, quotes, and more
- **AI-Powered Connections:** GPT-4 or Claude analyzes topics and finds genuine intellectual bridges
- **Beautiful Animations:** Smooth, delightful animations enhance the discovery experience
- **Share Discoveries:** Unique URLs for each connection
- **Favorites:** Save your favorite connections
- **Browse & Explore:** View popular and recent connections

## 📡 API Endpoints

### Connection Endpoints
- `POST /api/v1/connections/generate` - Generate a new random connection
- `GET /api/v1/connections/random` - Get a pre-generated connection (fast)
- `GET /api/v1/connections/{id}` - Get specific connection
- `GET /api/v1/connections` - List connections (paginated)
- `GET /api/v1/connections/popular` - Most favorited connections

### Topic Endpoints
- `GET /api/v1/topics/random` - Get random topics
- `GET /api/v1/topics/random/{source}` - Get random from specific source
- `GET /api/v1/topics/{id}` - Get topic details

## 🔌 External APIs Used

- **Wikipedia API** - Random articles and knowledge
- **PokéAPI** - Pokémon lore and data
- **Open Trivia Database** - Trivia questions and facts
- **Useless Facts API** - Interesting facts
- **Numbers API** - Number trivia and math facts
- **Quotable API** - Random quotes
- **OpenAI API** or **Anthropic Claude API** - AI connection generation

## 🏗️ Project Structure

```
serendipity-engine/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── tasks/        # Celery tasks
│   │   └── utils/        # Utilities
│   ├── tests/            # Backend tests
│   └── alembic/          # Database migrations
├── frontend/             # Next.js frontend
│   ├── app/              # App router pages
│   ├── components/       # React components
│   ├── hooks/            # Custom hooks
│   ├── services/         # API services
│   ├── store/            # State management
│   └── types/            # TypeScript types
└── docker-compose.yml    # Docker orchestration
```

## 🧪 Development

### Running Tests

**Backend:**
```bash
cd backend
uv run pytest
```

**Frontend:**
```bash
cd frontend
npm test
```

### Database Migrations

```bash
cd backend
# Create a new migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback
uv run alembic downgrade -1
```

## 🎯 Roadmap

- [x] Core connection generation
- [x] Multi-source topic fetching
- [x] Beautiful UI with animations
- [ ] User authentication
- [ ] Connection chains (A→B→C)
- [ ] Adjustable "weirdness" level
- [ ] Custom topic requests
- [ ] Social sharing with metadata
- [ ] Connection quality voting
- [ ] Topic recommendations

## 📝 License

MIT License - feel free to use this project for learning and experimentation!

## 🙏 Acknowledgments

Built with:
- FastAPI, Next.js, and the amazing open-source community
- Wikipedia, PokéAPI, Open Trivia DB, and other public APIs
- OpenAI and Anthropic for AI capabilities

---

*"What unexpected connection will you discover today?"*
