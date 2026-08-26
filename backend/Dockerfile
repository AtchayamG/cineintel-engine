# Minimal production Dockerfile for Cloud Run
FROM python:3.11-slim

# Prevent Python from writing bytecode and ensure immediate stdout/stderr flush
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Install dependencies first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Cloud Run injects PORT; launch uvicorn listening on 0.0.0.0:$PORT
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
