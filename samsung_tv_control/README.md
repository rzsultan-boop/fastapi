# Samsung TV Volume Control

A tiny [FastAPI](https://fastapi.tiangolo.com) service that lets you control a
Samsung TV's **volume**, **mute**, and **power** from your phone — including
from outside the house — with big tap-friendly buttons and a one-press
**"Turn it DOWN"** panic button.

Built because a certain younger family member keeps cranking the volume. 🙂

---

## How it works (read this first)

Samsung TVs only accept remote commands from a device on the **same home
Wi-Fi / LAN**. They are *not* reachable directly from the internet, and that's a
good thing. So the setup is:

```
   Your phone (anywhere)            Your home network
   ┌───────────────┐               ┌──────────────────────────┐
   │  web page /   │   secure      │  always-on device         │
   │  API call     │──tunnel──────▶│  (Pi / old laptop / NAS)  │
   └───────────────┘  (Tailscale)  │  running THIS service     │
                                    │            │ LAN          │
                                    │            ▼              │
                                    │     📺  Samsung TV         │
                                    └──────────────────────────┘
```

1. Run this service on a small **always-on device at home** (Raspberry Pi, an
   old laptop, a NAS that runs Docker, etc.).
2. It talks to the TV over your LAN.
3. You reach the service from your phone via a **secure tunnel** (see
   [Access from afar](#access-from-afar)).

> You can't run it on this cloud machine and have it reach your TV — it must be
> on the same network as the TV.

---

## Which TV do you have?

Your two TVs use **different protocols**, selected with `TV_METHOD`:

| TV (from your screenshots)      | Era   | `TV_METHOD` | Port   |
|---------------------------------|-------|-------------|--------|
| **Samsung 8 Series (65)**       | 2016+ | `ws`        | `8002` |
| **UA46ES6200**                  | 2012  | `legacy`    | `55000`|

The modern **8 Series** is almost certainly the one you want (it was "Previously
connected" in Smart View). Start with `TV_METHOD=ws`.

> Note: the UA46ES6200 showed **"Not available"** in your screenshot — that
> usually means it was powered off / asleep, or on a different network. Legacy
> TVs also can't be powered *on* over the network (Wi-Fi radio is off when the
> TV is off); volume/mute/off work while it's on.

---

## Quick start on a Mac (recommended for most people)

If a MacBook on the same Wi-Fi as the TV will be your always-on host:

1. In Finder, open the `samsung_tv_control` folder and **double-click
   `run-mac.command`**. (First time: right-click → Open to get past Gatekeeper.)
2. The first run installs everything, then creates a `.env` and stops. Open it
   with `open -e .env`, set **`TV_HOST`** (your TV's IP) and an **`API_KEY`**,
   save, and double-click `run-mac.command` again.
3. Leave that Terminal window open. The script uses `caffeinate` so the Mac
   won't idle-sleep the server while it runs.
4. Control it:
   - On the Mac: <http://localhost:8000/>
   - From your phone on the same Wi-Fi: `http://<mac-ip>:8000/` (the script
     prints the address). macOS may ask to **allow incoming connections** —
     click Allow.

> macOS sleep: the server only answers while the Mac is awake. `caffeinate`
> stops *idle* sleep, but **closing the lid still sleeps the Mac.** To control
> the TV with the lid closed, keep it plugged in and either run with the lid
> open, or use a tool like Amphetamine / `caffeinate -s`. When the Mac is fully
> asleep or off, control stops — that's expected.

For phone access from *outside* the house, add Tailscale — see
[Access from afar](#access-from-afar).

---

## Setup (manual / non-Mac)

On the home device:

```bash
cd samsung_tv_control
python -m venv .venv && source .venv/bin/activate    # optional but recommended
pip install -r requirements.txt

cp .env.example .env
# Edit .env: set TV_METHOD, TV_HOST (your TV's IP), and an API_KEY.
```

**Find your TV's IP:** on the TV go to
`Settings → General → Network → Network Status → IP Settings`, or look in your
router's list of connected devices.

**Generate an API key** (required if you'll reach it from outside the LAN):

```bash
python -c "import secrets; print(secrets.token_urlsafe(24))"
```

Put that value in `.env` as `API_KEY=...`.

### Run it

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open `http://<home-device-ip>:8000/` on your phone (on the same Wi-Fi to start).
Paste your API key into the box once and tap **Save** — it's stored only in your
browser.

### First connection to a modern (ws) TV

The **first** time you send a command, the TV shows a popup asking to allow
"HomeVolumeControl". **Accept it** (grab the TV remote once). A token is saved to
`TV_TOKEN_FILE` so you won't be asked again. Use port **8002** (encrypted).

Tip: on the TV, `General → External Device Manager → Device Connect Manager →
Access Notification → First Time Only` avoids repeat prompts.

---

## Access from afar

You need to reach the home device's port 8000 from your phone. **Recommended:**

### Tailscale (easiest, most secure)
1. Install [Tailscale](https://tailscale.com) on the home device **and** your
   phone, sign in to the same account on both.
2. From your phone, open `http://<tailscale-ip-of-home-device>:8000/`.
3. No router config, no ports open to the internet. Traffic is encrypted.

Other options: a self-hosted VPN (WireGuard), or Cloudflare Tunnel. **Avoid**
plain router port-forwarding unless you keep the `API_KEY` set and ideally put
HTTPS in front of it — the API key is the only thing protecting your TV otherwise.

### Keep it running
Use a process manager so it restarts on boot, e.g. a `systemd` service or
`pm2`. (A sample systemd unit is in [Run as a service](#run-as-a-service).)

---

## API

All control endpoints are `POST` and require the API key (header `X-API-Key`
or `?key=...`) when `API_KEY` is set.

| Method & path           | What it does                                  |
|-------------------------|-----------------------------------------------|
| `POST /api/volume/down` | Volume −1 (`?steps=N`, 1–30)                   |
| `POST /api/volume/up`   | Volume +1 (`?steps=N`, 1–30)                   |
| `POST /api/volume/panic`| Volume down by `PANIC_STEPS` (default 5)       |
| `POST /api/mute`        | Toggle mute                                    |
| `POST /api/power`       | Toggle power (modern TVs) / power off (legacy) |
| `GET  /api/health`      | Status + which TV is configured (no auth)      |

Example:

```bash
curl -X POST -H "X-API-Key: YOUR_KEY" http://localhost:8000/api/volume/panic
```

Interactive docs at `http://<host>:8000/docs`.

---

## Run as a service

`/etc/systemd/system/tvvolume.service` (adjust paths/user):

```ini
[Unit]
Description=Samsung TV Volume Control
After=network-online.target

[Service]
WorkingDirectory=/home/pi/samsung_tv_control
ExecStart=/home/pi/samsung_tv_control/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now tvvolume
```

---

## Troubleshooting

- **502 / "Could not command TV"** — wrong `TV_HOST`, TV is off, or it's on a
  different subnet/VLAN than the home device (Samsung blocks cross-subnet).
- **Modern TV never shows the allow popup** — make sure you're on port `8002`,
  and that the device is on the same network. Delete the token file and retry.
- **Legacy TV "Not available"** — it must be powered on and on Wi-Fi/Ethernet;
  legacy TVs can't be woken over the network.
- **Want absolute volume ("set to 12")?** Key emulation only does relative
  up/down + mute, which covers the "turn it down" use case reliably. True
  set-to-a-number requires Samsung's SmartThings cloud API (a separate, heavier
  setup) — ask if you want that added.

---

## Libraries used
- [`samsungtvws`](https://github.com/xchwarze/samsung-tv-ws-api) — modern Tizen TVs.
- [`samsungctl`](https://github.com/Ape/samsungctl) — legacy (pre-2016) TVs.
