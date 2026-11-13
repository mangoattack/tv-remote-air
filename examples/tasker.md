# Android: Google Assistant, Tasker, HTTP Shortcuts

[Deutsch below](#deutsch)

## HTTP Shortcuts (simplest)

1. Install **HTTP Shortcuts** (free, open source) from the Play Store or F-Droid.
2. **+** → Regular shortcut → URL `http://192.168.0.10:8080/api/tv/key/playpause?token=abc123`, method GET.
3. Name it "TV pause" and add it to the home screen, or start it from a Google Assistant routine ("Hey Google, TV pause" → run app shortcut).

## Tasker

Task → **+** → Net → **HTTP Request**: method GET, URL as above. For favourites: method POST, body `{"index":0}`, header `Content-Type: application/json`.
Trigger it with a Tasker profile (Wi-Fi connected, time, NFC tag) or from Google Assistant via the Tasker / AutoVoice integration.

## Google Assistant routine

Google Home app → Automations → **+** → Starter "When I say …" → Action "Adjust Home devices" doesn't reach local addresses, so use **"Open app"/shortcut** with an HTTP Shortcuts shortcut, or a Tasker task.

---

## Deutsch

**HTTP Shortcuts (am einfachsten):** App **HTTP Shortcuts** (gratis, Open Source) aus Play Store oder F-Droid → **+** → Normaler Shortcut → URL `http://192.168.0.10:8080/api/tv/key/playpause?token=abc123`, Methode GET → "TV Pause" nennen, auf den Startbildschirm legen oder aus einer Google Assistant-Routine starten.

**Tasker:** Task → **+** → Netz → **HTTP Request**: Methode GET, URL wie oben. Für Favoriten: POST, Body `{"index":0}`, Header `Content-Type: application/json`. Auslösen über ein Tasker-Profil (WLAN verbunden, Uhrzeit, NFC) oder per Google Assistant über Tasker/AutoVoice.

**Google Assistant-Routine:** Google-Home-App → Automationen → **+** → "Wenn ich sage …" → als Aktion einen HTTP-Shortcuts-Shortcut oder Tasker-Task öffnen, weil Routinen keine lokalen Adressen direkt aufrufen.
