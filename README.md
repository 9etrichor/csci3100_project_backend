# CSCI3100 Project Backend

A Django REST API backend for the CSCI3100 project, featuring user authentication with JWT tokens and PostgreSQL database.

## Tech Stack

- **Framework**: Django 5.2.7
- **API**: Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: PostgreSQL
- **Package Management**: uv
- **Containerization**: Docker & Docker Compose

## Features

- User registration and authentication
- JWT-based token authentication
- Custom user model
- RESTful API endpoints
- Docker containerization for easy deployment

## Local Development Setup

### Prerequisites

- Python 3.12+
- uv package manager
- PostgreSQL (or use Docker)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ivincentwchk/csci3100_project_backend.git
   cd csci3100_project_backend
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and secret key
   ```

4. **Run migrations**:
   ```bash
   uv run python manage.py migrate
   ```

5. **Start the development server**:
   ```bash
   uv run python manage.py runserver
   ```

The API will be available at `http://localhost:8000`.

## Docker Setup

### Prerequisites

- Docker & Docker Compose

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Ivincentwchk/csci3100_project_backend.git
   cd csci3100_project_backend
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env if needed (defaults are provided for development)
   ```

3. **Run database migrations**:
   ```bash
   docker-compose --profile migrate up migrate
   ```

4. **Start the application**:
   ```bash
   docker-compose up web
   ```

The API will be available at `http://localhost:8000`.

### Docker Commands

- **Start all services**: `docker-compose up`
- **Run migrations**: `docker-compose --profile migrate up migrate`
- **Stop services**: `docker-compose down`
- **View logs**: `docker-compose logs web`
- **Rebuild**: `docker-compose up --build`

### Docker Details

- Uses `uv` for fast dependency management in containers.
- Installs dependencies globally to avoid virtual environment issues.
- Compatible with local `uv` usage for development.

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Users
- `GET /api/users/` - List users (authenticated)
- `GET /api/users/{id}/` - User details (authenticated)

## Project Structure

```
csci3100_project_backend/
├── backend_project/          # Django project settings
│   ├── settings.py          # Main settings
│   ├── urls.py              # URL configuration
│   └── wsgi.py              # WSGI application
├── users/                    # Custom user app
│   ├── models.py            # User model
│   ├── views.py             # API views
│   └── serializers.py       # DRF serializers
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Docker services
├── pyproject.toml            # Project dependencies
├── uv.lock                   # Dependency lock file
└── README.md                 # This file
```

## Environment Variables

Create a `.env` file with the following variables:

```env
# Django settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DB_NAME=backend_db
DB_USER=django_user
DB_PASSWORD=secure_password
DB_HOST=db
DB_PORT=5432

# PostgreSQL settings (for Docker)
POSTGRES_DB=backend_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=secure_password
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add feature'`
4. Push to your fork: `git push origin feature-name`
5. Create a Pull Request

## License

This project is part of the CSCI3100 course assignment.