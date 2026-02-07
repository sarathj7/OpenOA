FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY backend/requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy entire backend application
COPY backend /app/backend

# ALSO COPY EXAMPLES DATA (important for plantdata.yml)
COPY examples /app/examples

# Expose API port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
