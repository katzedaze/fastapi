# FastAPI + Next.js Full Stack Application

A modern full-stack application with FastAPI backend and Next.js frontend, containerized with Docker.

## Tech Stack

### Backend

- Python 3.12 LTS
- FastAPI v0.115.12
- SQLAlchemy v2.0.41 + SQLModel v0.0.24
- PostgreSQL 17 LTS
- Alembic for migrations
- JWT authentication

### Frontend

- Next.js v15.3.2 (App Router)
- React v18.3.1
- TypeScript
- Tailwind CSS v4
- shadcn/ui components
- Zod for validation

## Quick Start

1. **Clone and setup environment:**

   ```bash
   cp .env.example .env
   ```

2. **Start the application:**

   ```bash
   make fresh
   ```

   This command will:
   - Build Docker containers
   - Start all services
   - Run database migrations
   - Seed the database with dummy data

3. **Access the application:**
   - Frontend: <http://localhost:3000>
   - Backend API: <http://localhost:8000>
   - API Documentation: <http://localhost:8000/docs>

## Development

### Common Commands

```bash
make up          # Start all services
make down        # Stop all services
make logs        # View logs
make migrate     # Run database migrations
make seed        # Seed database with dummy data
make test        # Run tests
make format      # Format code
make lint        # Lint code
```

### Shell Access

```bash
make shell-backend   # Access backend container
make shell-frontend  # Access frontend container
make shell-db       # Access PostgreSQL shell
```

## Default Credentials

- **Admin User:** <admin@example.com> / admin123
- **Regular Users:** Check the seed script output

## Project Structure

```
fastapi/
├── backend/            # FastAPI backend
│   ├── app/           # Application code
│   ├── alembic/       # Database migrations
│   └── scripts/       # Utility scripts
├── frontend/          # Next.js frontend
│   ├── app/          # Next.js App Router
│   └── components/   # React components
├── docker-compose.yml # Docker configuration
├── Makefile          # Development commands
└── .env.example      # Environment variables template
```

## API Documentation

Once the backend is running, you can access:

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting: `make test && make lint`
4. Submit a pull request

## License

MIT
