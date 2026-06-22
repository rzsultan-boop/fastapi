#!/bin/bash
# One-shot installer for macOS. Run it once:
#
#     bash install-mac.sh
#
# It does everything by itself:
#   • creates a Python virtualenv and installs dependencies
#   • scans your Wi-Fi and finds the Samsung TV automatically
#   • generates an API key and writes the .env config
#   • installs a LaunchAgent so the server auto-starts at every login
#     (and restarts itself if it ever crashes), kept awake with caffeinate
#   • opens the control page with the key already filled in
#
# After this, the only thing left for you is to accept the one-time
# "allow" popup that appears ON THE TV the first time you press a button.

set -e
cd "$(dirname "$0")"
PROJ="$(pwd)"
LABEL="com.tvvolume.control"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"

echo "▶ Samsung TV volume control — setting up on this Mac"

# --- Python + dependencies ---------------------------------------------------
PY="$(command -v python3 || true)"
if [ -z "$PY" ]; then
  echo "❌ python3 not found. Install from https://www.python.org/downloads/ then re-run."
  exit 1
fi
if [ ! -d ".venv" ]; then
  echo "  • creating virtualenv + installing dependencies (first run only)…"
  "$PY" -m venv .venv
  ./.venv/bin/pip install --quiet --upgrade pip
  ./.venv/bin/pip install --quiet -r requirements.txt
fi
VENV_PY="$PROJ/.venv/bin/python"
UVICORN="$PROJ/.venv/bin/uvicorn"

# --- Find the TV automatically ----------------------------------------------
echo "  • scanning your network for the Samsung TV…"
TV_HOST="$("$VENV_PY" -c "from app.discover import discover_one; t=discover_one(); print(t.host if t else '')")"
if [ -n "$TV_HOST" ]; then
  echo "    ✔ found TV at $TV_HOST"
else
  echo "    ⚠ no TV found right now (is it ON and on this Wi-Fi?)."
  echo "      Continuing — the server will keep trying to discover it at startup."
fi

# --- Config (.env): reuse existing API key if present, else generate --------
if [ -f ".env" ] && grep -q '^API_KEY=.\+' .env; then
  API_KEY="$(grep '^API_KEY=' .env | head -1 | cut -d= -f2-)"
else
  API_KEY="$("$VENV_PY" -c "import secrets; print(secrets.token_urlsafe(24))")"
fi

cat > .env <<EOF
TV_METHOD=ws
TV_HOST=$TV_HOST
TV_NAME=HomeVolumeControl
TV_TOKEN_FILE=$PROJ/tv_token.txt
API_KEY=$API_KEY
PANIC_STEPS=5
EOF
echo "  • wrote config (.env)"

# --- Auto-start via LaunchAgent ---------------------------------------------
mkdir -p "$HOME/Library/LaunchAgents"
launchctl unload "$PLIST" 2>/dev/null || true
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL</string>
  <key>WorkingDirectory</key><string>$PROJ</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/caffeinate</string>
    <string>-i</string>
    <string>$UVICORN</string>
    <string>app.main:app</string>
    <string>--host</string><string>0.0.0.0</string>
    <string>--port</string><string>8000</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>$PROJ/server.log</string>
  <key>StandardErrorPath</key><string>$PROJ/server.log</string>
</dict>
</plist>
EOF
launchctl load "$PLIST"
echo "  • installed auto-start service (runs at every login)"

# --- Open the control page ---------------------------------------------------
sleep 2
MAC_IP="$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo localhost)"
open "http://localhost:8000/?key=$API_KEY" 2>/dev/null || true

echo ""
echo "✅ Done. The control page just opened in your browser."
echo "   On this Mac:     http://localhost:8000/"
echo "   From your phone: http://$MAC_IP:8000/  (same Wi-Fi; API key prompt once)"
echo ""
echo "   👉 One thing only you can do: the FIRST time you tap a button, the TV"
echo "      shows an 'allow HomeVolumeControl' popup — accept it with the TV"
echo "      remote. After that it just works, forever, whenever this Mac is awake."
echo ""
echo "   Your API key (saved already in the opened page): $API_KEY"
