"""Configuration loaded from environment variables (and an optional .env file)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv() -> None:
    """Minimal .env loader so we don't add a dependency just for this.

    Only sets a key if it isn't already present in the real environment.
    """
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.is_file():
        return
    for raw in env_path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_DEFAULT_PORTS = {"ws": 8002, "legacy": 55000}


@dataclass(frozen=True)
class Settings:
    method: str
    host: str
    port: int
    name: str
    token_file: str
    api_key: str
    panic_steps: int

    @property
    def auth_required(self) -> bool:
        return bool(self.api_key)


def get_settings() -> Settings:
    _load_dotenv()

    method = os.environ.get("TV_METHOD", "ws").strip().lower()
    if method not in _DEFAULT_PORTS:
        raise ValueError(
            f"TV_METHOD must be one of {sorted(_DEFAULT_PORTS)}, got {method!r}"
        )

    host = os.environ.get("TV_HOST", "").strip()
    if not host:
        raise ValueError("TV_HOST is required (your TV's IP address).")

    port = int(os.environ.get("TV_PORT", _DEFAULT_PORTS[method]))

    return Settings(
        method=method,
        host=host,
        port=port,
        name=os.environ.get("TV_NAME", "HomeVolumeControl").strip(),
        token_file=os.environ.get("TV_TOKEN_FILE", "./tv_token.txt").strip(),
        api_key=os.environ.get("API_KEY", "").strip(),
        panic_steps=int(os.environ.get("PANIC_STEPS", "5")),
    )
