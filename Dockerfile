# Use Python 3.12 slim as base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install uv for fast package management
RUN pip install uv

# Set work directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .
# Install dependencies globally using uv
RUN uv pip install --system -r requirements.txt
RUN python3 -c "import django; print('Django version:', django.get_version())"

# Copy project files
COPY . .

# Collect static files
RUN python3 manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run the application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
