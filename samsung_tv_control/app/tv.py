"""Thin abstraction over the two Samsung remote-control protocols.

- ``ws``     -> modern Tizen TVs (2016+) via the ``samsungtvws`` library.
- ``legacy`` -> older TVs (2012-2015) via the ``samsungctl`` library.

Both backends ultimately emulate IR-remote key presses (volume up/down, mute,
power, etc.), which is the most reliable thing every Samsung TV understands.
"""

from __future__ import annotations

import time

from .config import Settings

# Keys we are willing to forward. Keeps an exposed endpoint from being abused
# to send arbitrary control codes to the TV.
ALLOWED_KEYS = {
    "KEY_VOLUP",
    "KEY_VOLDOWN",
    "KEY_MUTE",
    "KEY_POWER",
    "KEY_POWEROFF",
}

# Small gap between repeated presses so the TV registers each one.
_PRESS_DELAY = 0.12


class TVError(RuntimeError):
    """Raised when we cannot reach or command the TV."""


def _send_ws(settings: Settings, keys: list[str]) -> None:
    try:
        from samsungtvws import SamsungTVWS
    except ImportError as exc:  # pragma: no cover - dependency missing
        raise TVError(
            "samsungtvws is not installed. Run: pip install -r requirements.txt"
        ) from exc

    try:
        # Context manager opens the websocket and closes it cleanly afterwards.
        with SamsungTVWS(
            host=settings.host,
            port=settings.port,
            token_file=settings.token_file,
            name=settings.name,
            timeout=8,
        ) as tv:
            for i, key in enumerate(keys):
                if i:
                    time.sleep(_PRESS_DELAY)
                tv.send_key(key)
    except Exception as exc:  # noqa: BLE001 - surface any transport error uniformly
        raise TVError(f"Could not command TV at {settings.host}: {exc}") from exc


def _send_legacy(settings: Settings, keys: list[str]) -> None:
    try:
        import samsungctl
    except ImportError as exc:  # pragma: no cover - dependency missing
        raise TVError(
            "samsungctl is not installed. Run: pip install -r requirements.txt"
        ) from exc

    config = {
        "name": "python-remote",
        "description": settings.name,
        "id": "samsung-tv-control",
        "host": settings.host,
        "port": settings.port,
        "method": "legacy",
        "timeout": 8,
    }
    try:
        with samsungctl.Remote(config) as remote:
            for i, key in enumerate(keys):
                if i:
                    time.sleep(_PRESS_DELAY)
                remote.control(key)
    except Exception as exc:  # noqa: BLE001
        raise TVError(f"Could not command TV at {settings.host}: {exc}") from exc


def send_keys(settings: Settings, keys: list[str]) -> None:
    """Send one or more remote keys to the configured TV."""
    bad = [k for k in keys if k not in ALLOWED_KEYS]
    if bad:
        raise TVError(f"Refusing to send disallowed key(s): {', '.join(bad)}")

    if settings.method == "ws":
        _send_ws(settings, keys)
    else:
        _send_legacy(settings, keys)


# --- Convenience helpers used by the API routes -------------------------------

def volume_up(settings: Settings, steps: int = 1) -> None:
    send_keys(settings, ["KEY_VOLUP"] * max(1, steps))


def volume_down(settings: Settings, steps: int = 1) -> None:
    send_keys(settings, ["KEY_VOLDOWN"] * max(1, steps))


def mute(settings: Settings) -> None:
    send_keys(settings, ["KEY_MUTE"])


def power(settings: Settings) -> None:
    send_keys(settings, ["KEY_POWER"])
