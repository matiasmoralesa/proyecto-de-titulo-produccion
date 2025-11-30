# Dockerfile para Railway
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements-production.txt /app/backend/requirements-production.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements-production.txt

# Copy the entire project
COPY . /app/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings.railway

# Expose port
EXPOSE 8000

# Start command (will be overridden by railway.json)
CMD ["gunicorn", "wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
