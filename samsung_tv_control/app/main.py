"""FastAPI service to control a Samsung TV's volume (and power) from anywhere.

Run locally:
    cd samsung_tv_control
    pip install -r requirements.txt
    cp .env.example .env   # then edit it
    uvicorn app.main:app --host 0.0.0.0 --port 8000

Then open http://<this-device-ip>:8000/ on your phone.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from . import tv
from .config import Settings, get_settings

settings = get_settings()

app = FastAPI(
    title="Samsung TV Volume Control",
    description="Control your Samsung TV's volume remotely.",
    version="1.0.0",
)

_STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")


def require_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    key: str | None = Query(default=None),
) -> None:
    """Reject the request unless a valid API key is supplied.

    Accepts the key via the ``X-API-Key`` header or a ``?key=`` query param
    (the query param lets the simple web UI work from a bookmarked link).
    If no API_KEY is configured, auth is skipped (local-only mode).
    """
    if not settings.auth_required:
        return
    supplied = x_api_key or key
    if supplied != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")


def _ok(action: str, **extra) -> JSONResponse:
    return JSONResponse({"ok": True, "action": action, **extra})


def _tv_call(fn, *args) -> JSONResponse:
    try:
        fn(*args)
    except tv.TVError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return _ok(fn.__name__, args=list(args))


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(_STATIC_DIR / "index.html")


@app.get("/api/health")
def health() -> dict:
    return {
        "status": "up",
        "method": settings.method,
        "tv_host": settings.host,
        "tv_port": settings.port,
        "auth_required": settings.auth_required,
    }


@app.post("/api/volume/up", dependencies=[Depends(require_key)])
def api_volume_up(steps: int = Query(default=1, ge=1, le=30)) -> JSONResponse:
    return _tv_call(tv.volume_up, settings, steps)


@app.post("/api/volume/down", dependencies=[Depends(require_key)])
def api_volume_down(steps: int = Query(default=1, ge=1, le=30)) -> JSONResponse:
    return _tv_call(tv.volume_down, settings, steps)


@app.post("/api/volume/panic", dependencies=[Depends(require_key)])
def api_volume_panic() -> JSONResponse:
    """Drop the volume by several steps at once — the 'son turned it up' button."""
    return _tv_call(tv.volume_down, settings, settings.panic_steps)


@app.post("/api/mute", dependencies=[Depends(require_key)])
def api_mute() -> JSONResponse:
    return _tv_call(tv.mute, settings)


@app.post("/api/power", dependencies=[Depends(require_key)])
def api_power() -> JSONResponse:
    return _tv_call(tv.power, settings)
