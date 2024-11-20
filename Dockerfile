FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=5000

WORKDIR /app

# Combine RUN commands to reduce layers
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip==24.3.1

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary files
COPY app.py .env ./
COPY ai_analysis.py competitive_analysis.py strategy_engine.py ./

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 1 --worker-class uvicorn.workers.UvicornWorker --timeout 30 app:app