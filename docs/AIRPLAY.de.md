# AirPlay auf Android TV

[English](AIRPLAY.md)

AirPlay ist in Android TV nicht eingebaut. Dieses Projekt nutzt **[AirPlay Server](https://github.com/jqssun/android-airplay-server)** von jqssun: kostenlos, Open Source (GPL-3.0), keine Werbung, keine Pro-Version. Es ist nicht von Apple.

## Was geht

| | |
|---|---|
| Bildschirm spiegeln von iPhone, iPad, Mac | Ja (H.264 und H.265) |
| Videos über die AirPlay-Taste (Safari, Fotos, viele Apps) | Ja |
| Musik mit Cover und Titel | Ja |
| Apps mit Kopierschutz (Apple TV+, Netflix, Disney+ ...) | **Nein**, das kann kein Empfänger, der nicht von Apple ist. Nimm die App auf dem TV oder Chromecast. |
| Android-Version | 7.0 oder neuer |

## Installieren

1. **Play Store auf dem TV (am besten, aktualisiert sich selbst):** "AirPlay Server" (von jqssun) suchen und installieren.
2. **Kein Play Store:** [F-Droid](https://f-droid.org/packages/io.github.jqssun.airplay) oder die neueste APK aus den [Releases](https://github.com/jqssun/android-airplay-server/releases):
   ```bash
   sh tools/airplay-setup.sh <tv-ip> "Wohnzimmer"
   ```
   Das Skript lädt die neueste Version, installiert sie, öffnet sie einmal und setzt den Namen.
3. Einmal am TV öffnen und erlauben, was er fragt.

## Einstellungen über ADB

```bash
# Name, den das iPhone sieht
adb shell am broadcast -n io.github.jqssun.airplay/.SettingsReceiver -a io.github.jqssun.airplay.SET_SETTING --es key server_name --es value "Wohnzimmer"
# Alle Einstellungen als JSON
adb shell am broadcast -n io.github.jqssun.airplay/.SettingsReceiver -a io.github.jqssun.airplay.LIST_SETTINGS
```

PIN, Auflösung, Overscan, Audio-Verzögerung und mehr findest du in den Einstellungen der App.

## Schnelltaste

Auf der Einstellungsseite (**+ App** → AirPlay Server) oder in `config.json`:

```json
{ "label": "AirPlay", "icon": "airplay", "app": "io.github.jqssun.airplay" }
```

## Erscheint nicht auf dem iPhone

1. AirPlay Server am TV öffnen. Manche TVs stoppen Hintergrund-Apps; nach einem Neustart nochmals öffnen oder die Schnelltaste nutzen.
2. Gleiches Netz: iPhone und TV im gleichen Netz und Subnetz. Kein Gäste-WLAN, keine "Client-Isolation" / "AP-Isolation".
3. mDNS (Bonjour): AirPlay wird per Multicast gefunden. Mesh-Systeme und manche Router blockieren das. Such nach "Multicast", "IGMP Snooping", "mDNS" oder "Bonjour" oder probier es mit dem iPhone am gleichen Access Point wie der TV.
4. Ein VPN auf dem iPhone oder ein Pi-hole/AdGuard mit strengen Regeln kann ihn auch verstecken.
5. App neu starten, dann den TV.

## Alternativen

Geht AirPlay Server auf deinem TV nicht, gibt es andere Empfänger-Apps (zum Beispiel AirScreen). Deren Gratis-Versionen haben oft Werbung, Zeitlimits oder ein Pro-Angebot. Probier sie nur, wenn dich das nicht stört.
