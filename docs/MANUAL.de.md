# Anleitung von Hand

Alles, was die KI macht, Schritt für Schritt, falls du es lieber selber machst. Dauert etwa 30 bis 60 Minuten.
[English](MANUAL.md)

> [!CAUTION]
> Keine Garantie: Nicht jeder TV funktioniert. AirPlay kommt von einer Drittanbieter-App, nicht von Apple. Für deinen TV bist du selbst verantwortlich.

## Was du brauchst

| | |
|---|---|
| **TV** | Android TV oder Google TV (oder eine Box/ein Stick damit). Android 7+ für AirPlay. |
| **Handy** | iPhone oder Android-Handy mit Browser. |
| **Eine Maschine für die Fernbedienung** | Docker-Host (NAS, Heimserver, Raspberry Pi), ein Linux-Server/VM/LXC oder dein Computer. Braucht Python 3 und `adb`. |
| **Netzwerk** | TV, Handy und diese Maschine im gleichen Netz (kein Gäste-WLAN, keine Client-Isolation). |

`adb` auf der Maschine installieren (bei Docker nicht nötig, das Image hat es):

```bash
sudo apt install adb python3          # Debian, Ubuntu, Raspberry Pi OS
brew install android-platform-tools   # macOS
```

## 1. Einstellungen am TV

1. **Entwicklermodus:** Einstellungen → System (oder Geräteeinstellungen) → Info → 7-mal auf **Build** drücken.
2. **Debugging:** Einstellungen → System → Entwickleroptionen → **USB-Debugging** und **Netzwerk-Debugging** einschalten (heisst bei manchen TVs **ADB über Netzwerk**). Neuere Google TVs haben nur **Wireless-Debugging**, siehe Schritt 2.
3. **Feste IP:** Die IP des TVs steht unter Einstellungen → Netzwerk → dein Netz. Gib ihm im Router eine feste Adresse (heisst oft *DHCP-Reservierung*, *statische Zuweisung* oder *immer dieselbe IP zuweisen*), damit die Fernbedienung ihn immer findet.
4. **Einschalten übers Netz (optional):** Hat dein TV *Fernstart*, *Wake on LAN*, *Netzwerk-Standby* oder *Schnellstart*, schalte es ein. Ohne das lassen sich viele TVs nicht vom Handy aus einschalten.
5. **Energiesparen:** Fällt der TV im Standby aus dem Netz, schalte tiefen Standby oder Eco-Modi aus.

## 2. Einmal mit adb verbinden

```bash
adb connect <tv-ip>:5555
```

Der TV zeigt **"USB-Debugging zulassen?"** → **Immer zulassen** anhaken → **Zulassen**. Dann prüfen:

```bash
adb devices          # zeigt <tv-ip>:5555  device
```

**Nur Wireless-Debugging (neuere Google TVs):** Entwickleroptionen → Wireless-Debugging → **Gerät mit Kopplungscode koppeln**. Dann:

```bash
adb pair <tv-ip>:<kopplungs-port>   # 6-stelligen Code eintippen
adb connect <tv-ip>:<port>          # der Port auf dem Wireless-Debugging-Bildschirm
```

Dieser Port ändert sich nach einem Neustart. Trag ihn in `config.json` als `"host": "<tv-ip>:<port>"` ein.

## 3. Fernbedienung einstellen

```bash
git clone https://github.com/mangoattack/tv-remote-air
cd tv-remote-air/remote
cp config.example.json config.json
```

`config.json` anpassen:

| Feld | Was es macht |
|---|---|
| `title` | Name im Browser-Tab. |
| `port` | Web-Port, Standard `8080`. |
| `token` | Optionales Passwort für die API. Wird in der App (Einstellungen) und in Sprach-URLs gebraucht. Empfohlen mit Siri oder Home Assistant. |
| `volumeDevice` | Welches Gerät Lautstärke und Stumm bekommt (meist der TV). |
| `devices.<id>.host` | IP des TVs oder der Box (`ip` oder `ip:port`). |
| `devices.<id>.box` | `true` für eine Box ohne HDMI-Eingänge. |
| `devices.<id>.adbKeyboard` | `true`, wenn [ADBKeyBoard](https://github.com/senzhk/ADBKeyBoard) installiert ist (Umlaute, Emoji). |
| `devices.<id>.tvButton` | Was die TV-Taste macht, z. B. `{"input": "<hdmi-id>"}` oder `{"app": "<paket/Activity>"}`. Standard: Home. |
| `devices.<id>.names` | Schönere App-Namen: `{"com.example.app": "Meine App"}`. |
| `devices.<id>.hideApps` | Pakete, die in der App-Liste fehlen sollen. |
| `devices.<id>.inputNames` | Namen für HDMI-Eingänge. |
| `devices.<id>.shortcuts` | Bis zu 3 Schnelltasten: `{"label", "icon": "hdmi/web/airplay/tv/star", "app" oder "input" oder "key", "device"}`. |

Die nötigen IDs findest du so:

```bash
adb -s <tv-ip>:5555 shell dumpsys tv_input | grep -o 'TvInputInfo{id=[^,]*'      # HDMI-Eingänge
adb -s <tv-ip>:5555 shell cmd package query-activities --brief -a android.intent.action.MAIN -c android.intent.category.LEANBACK_LAUNCHER   # Apps
```

## 4. Fernbedienung starten

Wähl eins:

**Docker** (NAS, Heimserver, Raspberry Pi mit Docker)

```bash
cd remote
docker compose up -d --build
```

Der ADB-Schlüssel bleibt in `remote/adb-keys`, darum fragt der TV nur einmal. Schau beim Start des Containers auf den TV.

**Linux-Server, VM, LXC oder Raspberry Pi** (systemd)

```bash
sudo sh remote/install.sh
```

**Dein Computer** (läuft nur, solange er an ist)

```bash
sh remote/run-on-pc.sh
```

Öffne `http://<ip-dieser-maschine>:8080` auf dem Handy und probier eine Taste. Sind die Punkte oben rot, schau in die [Hilfe](../README.de.md#hilfe).

**Ohne TV ausprobieren:** `python3 remote/server.py --demo` startet mit Test-Geräten.

## 5. Auf den Home-Bildschirm

- **iPhone:** Adresse in **Safari** öffnen → Teilen-Knopf → **Zum Home-Bildschirm**. Danach öffnet sie sich im Vollbild wie eine App.
- **Android:** in **Chrome** öffnen → ⋮ → **Zum Startbildschirm hinzufügen** (oder **App installieren**).

In der App öffnet das Regler-Symbol die schnellen **Einstellungen** (Aussehen, Steuerung, Sprache, Token). **Alle Einstellungen** öffnet `/settings`: Geräte und IPs mit Netz-Suche, Favoriten und ihre Reihenfolge, Touchpad-Tempo, Vibration, Token und Adressen für Sprachassistenten. Siehe [CONFIG.de.md](CONFIG.de.md).

## 6. AirPlay

1. Installier am TV **AirPlay Server** aus dem Play Store (Suche "AirPlay Server" von jqssun). Kein Play Store? Hol die APK von [F-Droid](https://f-droid.org/packages/io.github.jqssun.airplay) oder aus den [GitHub-Releases](https://github.com/jqssun/android-airplay-server/releases) und führ `adb install app-release.apk` aus.
2. Einmal am TV öffnen und erlauben, was er fragt.
3. Optional den Namen setzen, den das iPhone sieht:
   ```bash
   adb shell am broadcast -n io.github.jqssun.airplay/.SettingsReceiver -a io.github.jqssun.airplay.SET_SETTING --es key server_name --es value "Wohnzimmer"
   ```
4. Am iPhone: Kontrollzentrum → **Bildschirmsynchronisierung** → TV wählen.

AirPlay-Schnelltaste: `{"label": "AirPlay", "icon": "airplay", "app": "io.github.jqssun.airplay"}`.

**Alternativen**, falls es auf deinem TV nicht geht: AirScreen und ähnliche Apps. Deren Gratis-Versionen können Werbung oder Grenzen haben. Apps mit Kopierschutz kann keine davon spiegeln.

## 7. Optional: Startbildschirm im Apple-TV-Stil

Der Launcher von [CleanYourTV](https://github.com/Gathin23/cleanyourtv) (von Gathin23) ersetzt den vollen Startbildschirm durch einen ruhigen, der wie Apple TV aussieht. Du kannst **nur den Launcher** installieren, ohne den Debloat:

```bash
git clone https://github.com/Gathin23/cleanyourtv && cd cleanyourtv
export TV_HOST=<tv-ip>
launcher/build-and-install.sh          # braucht JDK 17-22 und Android SDK 34, oder zuerst tools/docker-build.sh
```

Im README dort stehen Themes, Dock und wie du zum alten Startbildschirm zurückkommst.

## Sprache und Home Assistant

Jede Taste ist eine Adresse (mit `?token=...`, wenn du ein Token gesetzt hast):

```
GET  http://<server>:8080/api/<gerät>/key/<taste>
POST http://<server>:8080/api/<gerät>/key      {"key": "volup", "count": 3}
POST http://<server>:8080/api/<gerät>/app      {"id": "com.netflix.ninja"}
POST http://<server>:8080/api/<gerät>/input    {"id": "<hdmi-id>"}
POST http://<server>:8080/api/<gerät>/text     {"text": "hallo"}
```

Tasten: `power on off playpause play pause stop rewind forward prev next volup voldown mute home back up down left right ok search tv chup chdown options guide info settings recents input captions del enter`.

**Siri, Kurzbefehle, HomePod:** Kurzbefehle → **+** → *Inhalte von URL abrufen* → `http://<server>:8080/api/tv/key/playpause?token=<token>` → "TV Pause" nennen. Sag "Hey Siri, TV Pause". Der HomePod startet persönliche Kurzbefehle, wenn in der Home-App *Persönliche Anfragen* an ist.

**Home Assistant** (`configuration.yaml`):

```yaml
rest_command:
  tv_key:
    url: "http://<server>:8080/api/tv/key/{{ key }}?token=<token>"
    method: GET
```

Dann `rest_command.tv_key` mit `key: playpause` aus einem Skript oder Knopf aufrufen. HA hat ausserdem die eingebaute Integration **Android TV Remote**, die du daneben nutzen kannst.

**Alexa:** Alexa kann keine lokale Adresse direkt aufrufen. Nimm eine Brücke wie Home Assistant (mit Nabu Casa oder dem Alexa-Skill) und starte das HA-Skript aus einer Alexa-Routine.

**Android:** die App **HTTP Shortcuts**, ein **Tasker**-Task mit *HTTP Request* oder eine Google Assistant-Routine, die eins davon startet.

## Sicherheit

- Die Fernbedienung hat standardmässig kein Login. Sie gehört nur ins Heimnetz. Gib Port 8080 nie ins Internet frei.
- Setz ein `token`, wenn andere Leute dein Netz nutzen.
- Netzwerk-Debugging muss für die Fernbedienung an bleiben. Nur Geräte, die du am TV erlaubt hast, können es nutzen. Drück **Zulassen** also nur für deine eigenen Geräte.

## Alles rückgängig machen

```bash
docker compose down                          # oder: sudo systemctl disable --now tv-remote
adb uninstall io.github.jqssun.airplay       # und jede andere App, die du installiert hast
```

Dann am TV die **Entwickleroptionen** ausschalten.
