FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=5000 \
    FLASK_ENV=production \
    WORKERS=2 \
    TIMEOUT=30

WORKDIR /app

# Combine RUN commands and add security updates
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip==24.3.1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY *.py ./
COPY .env ./

# Create non-root user for security
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:$PORT/health || exit 1

EXPOSE $PORT

CMD gunicorn --bind 0.0.0.0:$PORT \
    --workers $WORKERS \
    --threads 1 \
    --worker-class uvicorn.workers.UvicornWorker \
    --timeout $TIMEOUT \
    --worker-tmp-dir /dev/shm \
    --log-level info \
    app:app