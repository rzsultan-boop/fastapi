#!/bin/bash
# Double-click this file in Finder (or run it in Terminal) to start the
# Samsung TV volume control server on your Mac.
#
# It creates a virtual environment, installs dependencies the first time,
# and keeps your Mac awake (via `caffeinate`) so the server stays reachable
# while the MacBook is on — even if the screen would otherwise sleep.

set -e
cd "$(dirname "$0")"

PY="$(command -v python3 || true)"
if [ -z "$PY" ]; then
  echo "❌ python3 not found. Install it from https://www.python.org/downloads/ or 'brew install python'."
  read -r -p "Press Return to close." _
  exit 1
fi

# First-run setup: virtualenv + dependencies.
if [ ! -d ".venv" ]; then
  echo "📦 First run: creating virtual environment and installing dependencies…"
  "$PY" -m venv .venv
  ./.venv/bin/pip install --quiet --upgrade pip
  ./.venv/bin/pip install --quiet -r requirements.txt
  echo "✅ Dependencies installed."
fi

# Make sure config exists.
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo ""
  echo "⚠️  Created .env from the template."
  echo "    Open it and set TV_HOST (your TV's IP) and API_KEY, then run this again:"
  echo "    open -e \"$(pwd)/.env\""
  read -r -p "Press Return to close." _
  exit 0
fi

IP="$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo '<this-mac-ip>')"
echo ""
echo "🟢 Starting server. Keep this window open while you want TV control."
echo "   On this Mac:        http://localhost:8000/"
echo "   From your phone:     http://$IP:8000/   (same Wi-Fi)"
echo "   Stop the server:     press Control-C"
echo ""

# `caffeinate -i` prevents idle sleep for as long as the server runs.
exec caffeinate -i ./.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
