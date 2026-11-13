#!/bin/sh
# Installs AirPlay Server (github.com/jqssun/android-airplay-server, GPL-3.0) on a TV over ADB,
# names it and opens it once. Prefer the Play Store on the TV if it has one: it then updates itself.
# Usage: sh tools/airplay-setup.sh <tv-ip>[:port] "<name shown on the iPhone>"
set -e
[ -n "$2" ] || { echo 'Usage: sh tools/airplay-setup.sh <tv-ip>[:port] "<name>"'; exit 1; }
T=$1; case $T in *:*) ;; *) T=$T:5555;; esac
PKG=io.github.jqssun.airplay
adb connect "$T" >/dev/null 2>&1 || true
if adb -s "$T" shell pm list packages "$PKG" | grep -q "$PKG"; then
  echo "AirPlay Server is already installed."
else
  DIR=$(mktemp -d)
  URL=$(curl -s https://api.github.com/repos/jqssun/android-airplay-server/releases/latest | grep -o 'https://[^"]*app-release.apk' | head -1)
  [ -n "$URL" ] || { echo "Could not find the latest release. Install it from the Play Store on the TV instead."; exit 2; }
  echo "Downloading $URL"
  curl -sL -o "$DIR/airplay.apk" "$URL"
  adb -s "$T" install -r "$DIR/airplay.apk"
  rm -rf "$DIR"
fi
adb -s "$T" shell am start -n "$PKG/.MainActivity" >/dev/null
sleep 2
adb -s "$T" shell am broadcast -n "$PKG/.SettingsReceiver" -a "$PKG.SET_SETTING" --es key server_name --es value "$2" >/dev/null
echo "Done. On the iPhone: Control Center → Screen Mirroring → \"$2\"."
