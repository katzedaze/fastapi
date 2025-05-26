# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack web application built with:

- **Backend**: FastAPI with PostgreSQL, SQLModel, and JWT authentication
- **Frontend**: Next.js with TypeScript, Tailwind CSS, and shadcn/ui
- **Infrastructure**: Docker Compose for containerization

## Tech Stack Details

### Backend (Python 3.12 LTS)

- **FastAPI** v0.115.12 - Modern async web framework
- **SQLModel** v0.0.24 - SQL databases with Python objects (SQLAlchemy + Pydantic)
- **PostgreSQL** 17 - Primary database
- **Alembic** v1.16.1 - Database migrations
- **JWT Authentication** - Using python-jose[cryptography]
- **Data Seeding** - Factory Boy + Faker for test data
- **Testing** - pytest with async support
- **Code Quality** - Black, Ruff, mypy for formatting and linting

### Frontend (Node.js 20+)

- **Next.js** v15.3.2 - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** v4 - Utility-first CSS framework
- **shadcn/ui** - Pre-installed component library (New York style)
- **Axios** - HTTP client with interceptors
- **Zod** - Runtime type validation
- **React Hook Form** - Form management
- **js-cookie** - Cookie management

## Commands

### Quick Start

```bash
make fresh          # Clean install: build, migrate, and seed
make up            # Start all services
make down          # Stop all services
make docs          # Open API documentation
```

### Backend Development

```bash
make migrate        # Run database migrations
make makemigrations m="description"  # Create new migration
make seed          # Seed database with test data
make test          # Run backend tests
make test-cov       # Run backend tests with coverage
make format        # Format code with Black and Ruff
make lint          # Lint backend code (ruff + mypy)
make shell-backend # Access backend container shell
make shell-db      # Access PostgreSQL shell
```

### Frontend Development

```bash
cd frontend
npm run dev        # Start development server (http://localhost:3000) with Turbopack
npm run build      # Create production build
npm run lint       # Run ESLint checks
```

### Debugging

```bash
make logs          # Show logs from all services
make logs-backend  # Show backend logs only
make logs-frontend # Show frontend logs only
make restart       # Restart all services
docker-compose ps  # Check container status
```

## Project Structure

```
fastapi/
├── backend/
│   ├── app/
│   │   ├── api/v1/         # API version 1 endpoints
│   │   │   ├── endpoints/  # Route handlers
│   │   │   └── api.py      # API router aggregation
│   │   ├── core/           # Core functionality
│   │   │   ├── config.py   # Settings management
│   │   │   └── security.py # Password hashing, JWT
│   │   ├── db/             # Database configuration
│   │   │   ├── base.py     # Model imports
│   │   │   └── session.py  # Database session
│   │   ├── models/         # SQLModel database models
│   │   │   ├── user.py     # User model with UUID
│   │   │   ├── item.py     # Item model with relationships
│   │   │   └── enums.py    # Enum definitions
│   │   └── utils/          # Utilities
│   │       └── factories.py # Test data factories
│   ├── alembic/            # Database migrations
│   ├── scripts/            # Utility scripts
│   │   └── seed_db.py      # Database seeding
│   └── tests/              # Test suite
└── frontend/
    ├── app/                # Next.js App Router
    │   ├── (auth)/         # Auth pages (login)
    │   ├── (dashboard)/    # Protected pages
    │   └── api/            # API routes (if needed)
    ├── components/         # React components
    │   └── ui/            # shadcn/ui components
    ├── contexts/          # React contexts
    │   └── auth-context.tsx # Authentication state
    ├── services/          # API service layer
    │   ├── api-client.ts  # Axios configuration with interceptors
    │   ├── auth.service.ts # Authentication services
    │   ├── item.service.ts # Item CRUD services
    │   └── user.service.ts # User management services
    ├── types/             # TypeScript type definitions
    │   └── schemas/       # Zod schemas for validation
    ├── lib/               # Utilities
    │   └── utils.ts       # Helper functions
    ├── hooks/             # Custom React hooks
    └── middleware.ts      # Next.js middleware for route protection
```

## Key Implementation Details

### Database Models

All models use:

- **UUID** primary keys (not integers)
- **Enums** with lowercase keys and values
- **Timestamps** with timezone-aware datetime
- **Relationships** using SQLModel's Relationship

Example:

```python
class User(UserBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    role: UserRole = Field(default=UserRole.user)  # Enum field
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

### API Authentication

- JWT tokens stored in cookies and localStorage
- Axios interceptors automatically attach tokens
- Protected routes check authentication state
- Role-based access control (admin/user/guest)

### Frontend Patterns

- **Protected Routes**: Next.js middleware checks authentication cookies
- **API Client**: Centralized Axios instance with request/response interceptors
- **Service Layer**: Organized API calls in dedicated service files
- **Type Safety**: Zod schemas for runtime validation and TypeScript types
- **Error Handling**: Global error interceptor with toast notifications
- **Form Validation**: Zod schemas with React Hook Form integration
- **State Management**: React Context API for authentication state

## Common Tasks

### Adding a New Model

1. Create model in `/backend/app/models/`
2. Import in `/backend/app/db/base.py`
3. Create migration: `make makemigrations m="add_model_name"`
4. Run migration: `make migrate`
5. Add factory in `/backend/app/utils/factories.py`
6. Update seed script if needed

### Adding a New API Endpoint

1. Create route handler in `/backend/app/api/v1/endpoints/`
2. Add router to `/backend/app/api/v1/api.py`
3. Implement authentication dependencies if needed
4. Add tests in `/backend/tests/`

### Adding a Frontend Page

1. Create page in appropriate `/frontend/app/` directory
2. Use existing components from `/frontend/components/ui/`
3. Implement authentication check if needed (middleware handles route protection)
4. Create service functions in `/frontend/services/` for API calls
5. Define TypeScript types in `/frontend/types/schemas/`
6. Add form validation using Zod schemas if needed

## Testing

### Backend Tests

```bash
make test                              # Run all tests
make test-cov                         # Run tests with coverage report
docker-compose exec backend pytest -v  # Verbose output
docker-compose exec backend pytest tests/test_specific.py  # Run specific test file
```

### Manual API Testing

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>
- Default credentials: <admin@example.com> / admin123

## Environment Variables

Backend (`/backend/.env`):

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/fastapi_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure PYTHONPATH=/app in Docker
2. **Migration Conflicts**: Use `make clean && make fresh`
3. **Type Errors**: Run `make lint` to check types
4. **CORS Issues**: Check BACKEND_CORS_ORIGINS in .env

### Database Issues

```bash
# Reset database completely
make clean
make fresh

# Check database
make shell-db
\dt  # List tables
\d+ users  # Describe users table
\d+ items  # Describe items table
```

### Container Issues

```bash
# Rebuild specific service
docker-compose build backend
docker-compose up -d backend

# View real-time logs
docker-compose logs -f backend
```

## Code Style Guidelines

### Python/Backend

- Use type hints for all functions
- Follow PEP 8 (enforced by Black)
- Use SQLModel for models and schemas
- Prefer async functions for endpoints
- Add docstrings for complex functions

### TypeScript/Frontend

- Use TypeScript strict mode
- Define interfaces for all API responses
- Use const assertions for constants
- Prefer functional components with hooks
- Keep components small and focused

## Security Considerations

- Never commit .env files
- Use strong SECRET_KEY for JWT
- Validate all user inputs
- Implement rate limiting for production
- Keep dependencies updated
- Use HTTPS in production

## Performance Tips

- Use database indexes on frequently queried fields
- Implement pagination for list endpoints
- Use React.memo for expensive components
- Lazy load components when possible
- Cache API responses appropriately

## Deployment Checklist

- [ ] Update environment variables
- [ ] Run database migrations
- [ ] Build frontend for production
- [ ] Configure reverse proxy (nginx)
- [ ] Set up SSL certificates
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Create backup strategy

# important-instruction-reminders

Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
