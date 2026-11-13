#!/bin/sh
# Prints what the setup needs to know about a TV, read-only: model, Android version, storage,
# HDMI inputs and launchable apps, plus ready-to-paste config.json snippets.
# Usage: sh tools/tv-info.sh <tv-ip>[:port]
set -e
[ -n "$1" ] || { echo "Usage: sh tools/tv-info.sh <tv-ip>[:port]"; exit 1; }
T=$1; case $T in *:*) ;; *) T=$T:5555;; esac
adb connect "$T" >/dev/null 2>&1 || true
A="adb -s $T shell"
state=$(adb -s "$T" get-state 2>&1 || true)
[ "$state" = device ] || { echo "Not connected ($state). Accept 'Allow USB debugging?' on the TV and run again."; exit 2; }
echo "== Device"
echo "Model:     $($A getprop ro.product.manufacturer | tr -d '\r') $($A getprop ro.product.model | tr -d '\r')"
echo "Android:   $($A getprop ro.build.version.release | tr -d '\r') (SDK $($A getprop ro.build.version.sdk | tr -d '\r'))"
echo "Google TV: $($A pm list packages com.google.android.apps.tv.launcherx | grep -q launcherx && echo yes || echo no)"
echo "Storage:   $($A df -h /data | tail -1 | awk '{print $4" free of "$2}')"
echo "AirPlay:   $($A pm list packages io.github.jqssun.airplay | grep -q airplay && echo 'AirPlay Server installed' || echo 'not installed')"
echo
echo "== HDMI and other inputs (for \"shortcuts\" or \"tvButton\": {\"input\": \"<id>\"})"
$A dumpsys tv_input 2>/dev/null | grep -o 'TvInputInfo{id=[^,}]*[^}]*type=[A-Z_]*' | sed 's/TvInputInfo{id=//; s/,.*type=/   type=/' | sort -u || echo "(none, probably a box)"
echo
echo "== Apps (for \"shortcuts\": {\"app\": \"<id>\"})"
$A cmd package query-activities --brief -a android.intent.action.MAIN -c android.intent.category.LEANBACK_LAUNCHER | grep / | sed "s/^ *//" | sort -u
