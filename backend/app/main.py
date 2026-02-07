from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, metrics, analysis, turbines, geospatial
from app.config import settings
import os

app = FastAPI(title="OpenOA API")

# ------------------ CORS FIX ------------------

origins = []

# Read CORS origins from environment
cors_env = os.getenv("BACKEND_CORS_ORIGINS")

if cors_env:
    try:
        # Expecting JSON array string
        import json
        origins = json.loads(cors_env)
    except Exception:
        origins = [cors_env]

# Always allow Render frontend if not already present
render_frontend = "https://openoa-frontend-pcuc.onrender.com"

if render_frontend not in origins:
    origins.append(render_frontend)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ ROUTERS ------------------

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(turbines.router, prefix="/api/turbines", tags=["turbines"])
app.include_router(geospatial.router, prefix="/api/geospatial", tags=["geospatial"])


@app.get("/")
def root():
    return {
        "message": "OpenOA Backend Running",
        "cors_allowed": origins
    }


# ------------------ DATA LOADING FIX ------------------

from openoa.schema.metadata import Metadata

DATA_PATH = "/app/examples/plantdata.yml"

if not os.path.exists(DATA_PATH):
    DATA_PATH = "examples/plantdata.yml"

try:
    metadata = Metadata.from_yaml(DATA_PATH)
    print("Successfully loaded plant metadata")
except Exception as e:
    print("ERROR LOADING METADATA:", e)
    metadata = None
