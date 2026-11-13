#!/bin/sh
# Runs TV Remote Air in the foreground on a Mac, Linux PC or WSL. Stop with Ctrl+C.
# Needs Python 3 and adb (macOS: brew install android-platform-tools, Linux: apt install adb).
cd "$(dirname "$0")"
[ -f config.json ] || { cp config.example.json config.json; echo "Created config.json, put your TV's IP in it."; exit 1; }
adb start-server >/dev/null 2>&1
exec python3 server.py
