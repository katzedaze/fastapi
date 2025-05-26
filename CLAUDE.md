# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Quick Start
- `make fresh` - Fresh install: clean, setup, start, migrate, and seed
- `make up` - Start all services
- `make down` - Stop all services
- `make docs` - Open API documentation at http://localhost:8000/docs

### Backend Development
- `make migrate` - Run database migrations
- `make makemigrations m="description"` - Create a new migration
- `make seed` - Seed database with dummy data
- `make test` - Run backend tests
- `make format` - Format code with Black and Ruff
- `make lint` - Lint backend code

### Frontend Development (from `/frontend` directory)
- `npm run dev` - Start development server on http://localhost:3000
- `npm run build` - Create production build
- `npm run start` - Start production server
- `npm run lint` - Run ESLint checks

### Debugging
- `make logs` - Show logs from all services
- `make shell-backend` - Open shell in backend container
- `make shell-db` - Open PostgreSQL shell

## Architecture

This is a full-stack application with FastAPI backend and Next.js frontend.

### Backend Stack
- **Framework**: FastAPI v0.115.12 with async support
- **ORM**: SQLModel v0.0.24 (SQLAlchemy + Pydantic integration)
- **Database**: PostgreSQL 17 LTS
- **Migrations**: Alembic v1.16.1
- **Authentication**: JWT with python-jose
- **Data Generation**: Faker + Factory Boy for seeding

### Frontend Stack
- **Framework**: Next.js 15.3.2 with App Router
- **UI Library**: shadcn/ui (New York style) - all components pre-installed
- **Styling**: Tailwind CSS v4 with CSS variables
- **Forms**: React Hook Form + Zod for validation
- **State**: Built-in React state

### Project Structure

#### Backend (`/backend`)
- `/app/api/` - API endpoints organized by version
- `/app/core/` - Core functionality (config, security)
- `/app/db/` - Database session and base configuration
- `/app/models/` - SQLModel database models
- `/app/schemas/` - Pydantic schemas (for non-SQLModel cases)
- `/app/utils/` - Utilities including data factories
- `/alembic/` - Database migrations
- `/scripts/` - Utility scripts (e.g., database seeding)

#### Frontend (`/frontend`)
- `/app/` - Next.js App Router pages and layouts
- `/components/ui/` - shadcn/ui components (pre-installed)
- `/lib/` - Utility functions
- `/hooks/` - Custom React hooks

### Key Backend Patterns
- Use SQLModel for both database models and API schemas
- Dependency injection for database sessions and authentication
- JWT tokens for API authentication
- Factory Boy for generating test data
- Alembic for database migrations

### API Authentication
- Login endpoint: `POST /api/v1/auth/login`
- Protected endpoints require Bearer token
- Default superuser: `admin@example.com` / `admin123`

### Database Models
- **User**: Authentication and user management
- **Item**: Example resource with CRUD operations

### Environment Variables
Copy `.env.example` to `.env` and configure:
- Database credentials
- JWT secret key
- API URLs