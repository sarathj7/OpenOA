FROM python:3.11-slim

WORKDIR /app

# System deps for scientific/python packages (kept minimal)
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*

# Copy repo (includes openoa + examples + backend)
COPY . /app

# Install OpenOA from source so `examples/` is importable too
RUN pip install --no-cache-dir -U pip \
  && pip install --no-cache-dir -e . \
  && pip install --no-cache-dir -r backend/requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

