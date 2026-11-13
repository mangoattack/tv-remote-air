#!/bin/sh
# Installs TV Remote Air as a systemd service on Debian/Ubuntu/Raspberry Pi OS.
# Usage: sudo sh install.sh        (run from the cloned repo; config.json must exist next to server.py)
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
[ "$(id -u)" = 0 ] || { echo "Please run with sudo."; exit 1; }
[ -f "$HERE/config.json" ] || { echo "Create remote/config.json first (copy config.example.json)."; exit 1; }
command -v adb >/dev/null || { apt-get update && apt-get install -y adb python3; }
mkdir -p /opt/tv-remote-air
rsync -a --delete "$HERE/../" /opt/tv-remote-air/ 2>/dev/null || cp -r "$HERE/../." /opt/tv-remote-air/
cp "$HERE/tv-remote.service" /etc/systemd/system/tv-remote.service
systemctl daemon-reload
systemctl enable --now tv-remote
PORT=$(python3 -c "import json;print(json.load(open('$HERE/config.json')).get('port',8080))")
echo "Done. Open http://$(hostname -I | awk '{print $1}'):$PORT on your phone."
