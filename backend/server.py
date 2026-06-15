# server.py — Emergent-platform entrypoint for Agent Colette
#
# The platform's supervisor runs `uvicorn server:app` from /app/backend.
# Agent Colette (fork of Odysseus) lives next to this file. We import its
# FastAPI app and re-export it, after preparing the runtime environment
# (data directory, .env file, MIME types, etc.) so the app starts cleanly
# on a fresh Emergent pod.
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).parent

# 1) Data directory — Agent Colette persists everything under DATA_DIR.
#    Default keeps it inside /app/backend/data so it survives hot reloads.
DATA_DIR = os.environ.setdefault(
    "ODYSSEUS_DATA_DIR", str(ROOT / "data")
)
Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
(Path(DATA_DIR) / "logs").mkdir(exist_ok=True)

# 2) Bootstrap a working .env in /app/backend if the user hasn't created one.
ENV_FILE = ROOT / ".env"
EXAMPLE_FILE = ROOT / ".env.example"
if not ENV_FILE.exists() and EXAMPLE_FILE.exists():
    shutil.copy2(EXAMPLE_FILE, ENV_FILE)

# 3) Sensible defaults for an Emergent-hosted environment.
os.environ.setdefault("AUTH_ENABLED", "true")
os.environ.setdefault("LOCALHOST_BYPASS", "false")
# Allow Emergent's preview origin (and any *.preview.emergentagent.com) plus
# loopback. The platform proxy presents the user as same-origin, so this is
# mostly for explicit CORS-aware clients.
os.environ.setdefault(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:8001,https://*.preview.emergentagent.com",
)
# Keep cookies usable behind Emergent's HTTPS proxy.
os.environ.setdefault("SECURE_COOKIES", "true")
# Don't auto-seed an admin password — the operator sets one via /setup.

# 4) Pre-create core directories that Agent Colette expects.
for sub in (
    "uploads", "personal_docs", "tts_cache", "generated_images",
    "deep_research", "chroma", "rag", "memory_vectors",
):
    (Path(DATA_DIR) / sub).mkdir(exist_ok=True)

# 5) Bring in Agent Colette's FastAPI application object.
#    `app.py` (the upstream orchestrator) defines `app = FastAPI(...)`.
from app import app  # noqa: E402,F401  re-exported for uvicorn
