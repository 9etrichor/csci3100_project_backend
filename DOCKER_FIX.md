# Fixing PostgreSQL Docker Setup Issue

## Problem
When running `docker-compose --profile migrate up migrate`, the PostgreSQL container failed to start with the error:
```
Error: Database is uninitialized and superuser password is not specified.
You must specify POSTGRES_PASSWORD to a non-empty value for the superuser.
```

## Root Cause
The `docker-compose.yml` was configured to use environment variables from `.env` file for the database service, but it was missing the required PostgreSQL environment variables:
- `POSTGRES_PASSWORD`: Required password for the PostgreSQL superuser
- `POSTGRES_USER`: Username for the superuser (optional, defaults to 'postgres')
- `POSTGRES_DB`: Database name to create (optional)

The Django settings were using custom DB env vars (`DB_USER`, `DB_PASSWORD`, etc.), but PostgreSQL needs its own env vars for initialization.

## Solution
1. **Updated `.env.example`** to include PostgreSQL-specific variables:
   ```
   # PostgreSQL settings
   POSTGRES_DB=backend_db
   POSTGRES_USER=django_user
   POSTGRES_PASSWORD=secure_password
   ```

2. **Recopied `.env.example` to `.env`** to apply the changes:
   ```bash
   cp .env.example .env
   ```

3. **Ran migrations again**:
   ```bash
   docker-compose --profile migrate up migrate
   ```
   - This time, PostgreSQL initialized successfully with the provided credentials.
   - Django migrations applied without errors.

4. **Started the web service**:
   ```bash
   docker-compose up web
   ```
   - The application started successfully and is accessible at `http://localhost:8000`.

## Key Learnings
- PostgreSQL Docker image requires `POSTGRES_PASSWORD` for superuser setup.
- Always ensure Docker-specific env vars are provided when using official images.
- Use `.env.example` for templates and copy to `.env` for actual values.
- Separate migration runs from app startup for better control in Docker environments.

## Files Modified
- `.env.example`: Added PostgreSQL env vars
- `.env`: Updated via copy from `.env.example`

The backend is now fully Dockerized and running with proper database connectivity.
