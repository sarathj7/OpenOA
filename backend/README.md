## Backend service (FastAPI + OpenOA)

This directory contains the FastAPI backend that wraps the OpenOA analytics
library and exposes a JSON API for the wind farm performance dashboard.

### Quick start (backend only)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open `http://localhost:8000/health` to verify the service is running.

Full API routes, OpenOA integration, and auth will be implemented in subsequent steps.

