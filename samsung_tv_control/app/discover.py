"""Automatically find a Samsung Smart TV on the local network.

Modern Tizen TVs expose an unauthenticated info endpoint at
``http://<ip>:8001/api/v2/`` that returns the device name and type. We scan the
local /24 subnet for it, so the user never has to look up the TV's IP.
"""

from __future__ import annotations

import json
import socket
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass


@dataclass
class FoundTV:
    host: str
    name: str
    model: str


def _local_ip() -> str | None:
    """Best-effort local IP of this machine (no traffic is actually sent)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return None
    finally:
        s.close()


def _probe(host: str, timeout: float) -> FoundTV | None:
    url = f"http://{host}:8001/api/v2/"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8", "replace"))
    except Exception:  # noqa: BLE001 - unreachable host / not a TV
        return None

    device = data.get("device", {}) if isinstance(data, dict) else {}
    dev_type = str(device.get("type", ""))
    if "Samsung SmartTV" not in dev_type and "TV" not in dev_type:
        return None
    return FoundTV(
        host=host,
        name=str(device.get("name", "Samsung TV")).strip(),
        model=str(device.get("modelName", "")).strip(),
    )


def discover(timeout: float = 0.4, max_workers: int = 128) -> list[FoundTV]:
    """Scan the local /24 subnet and return any Samsung TVs found."""
    ip = _local_ip()
    if not ip:
        return []
    prefix = ip.rsplit(".", 1)[0]
    hosts = [f"{prefix}.{i}" for i in range(1, 255)]

    found: list[FoundTV] = []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(_probe, h, timeout): h for h in hosts}
        for fut in as_completed(futures):
            tv = fut.result()
            if tv:
                found.append(tv)
    found.sort(key=lambda t: t.host)
    return found


def discover_one() -> FoundTV | None:
    tvs = discover()
    return tvs[0] if tvs else None


if __name__ == "__main__":
    print("Scanning your network for Samsung TVs…")
    results = discover()
    if not results:
        print("No Samsung TV found. Make sure the TV is ON and on this Wi-Fi.")
    for t in results:
        label = f"{t.name} ({t.model})" if t.model else t.name
        print(f"  • {t.host}\t{label}")
