# Root entry point — lets Render find the app from the project root.
# All real code lives in backend/app/

import sys
import os

# Add backend to the Python path so `app.*` imports resolve correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app.main import app  # noqa: F401 — re-exported for uvicorn
