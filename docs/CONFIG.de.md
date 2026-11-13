# Konfiguration

Alles steht in `remote/config.json`. Du kannst es im Browser unter **`http://<server>:8080/settings`** bearbeiten (empfohlen) oder von Hand. Starte mit [`remote/config.example.json`](../remote/config.example.json) oder einem der [Beispiele](../examples/).
[English](CONFIG.md)

## Die Einstellungsseite

`/settings` hat zwei Teile:

| Teil | Gespeichert wo | Was du einstellst |
|---|---|---|
| **Auf diesem Handy** | Im Browser des Handys | Sprache, Aussehen (Klassisch / Apple TV), Steuerkreuz oder Touchpad, Touchpad-Tempo, Vibration, das Token, das dieses Handy schickt |
| **Für alle** | `config.json` auf dem Server | Name, welches Gerät die Lautstärke bekommt, TVs und Boxen (Name, IP, Box, ADBKeyBoard), Favoriten und ihre Reihenfolge, das API-Token, fertige Adressen für Siri, Home Assistant, Alexa und Google |

**Netz durchsuchen** findet Geräte mit eingeschaltetem Netzwerk-Debugging (Port 5555). **Verbinden** führt `adb connect` aus, damit der TV "USB-Debugging zulassen?" zeigt. **+ App / + HDMI-Eingang / + Taste** zeigen, was der TV wirklich hat. **Speichern** übernimmt alles; der Server lädt die Geräte sofort neu.

Mit Docker muss `config.json` beschreibbar eingebunden sein (die mitgelieferte `docker-compose.yml` macht das).

## Alle Felder

Siehe die kommentierte Liste in der [englischen Fassung](CONFIG.md#all-keys); die Feldnamen sind dieselben. Kurz:

| Feld | Bedeutung |
|---|---|
| `title` | Name im Browser-Tab |
| `port` | Web-Port (Umgebungsvariable `PORT` hat Vorrang) |
| `token` | Optionales API-Passwort |
| `volumeDevice` | Gerät für Lautstärke und Stumm |
| `devices.<id>.host` | IP oder IP:Port (Wireless-Debugging) |
| `box` | `true` = keine HDMI-Eingänge |
| `adbKeyboard` | `true`, wenn ADBKeyBoard installiert und aktiv ist |
| `tvButton` | Was die TV-Taste macht: `{"key": "home"}`, `{"input": "..."}` oder `{"app": "..."}` |
| `names`, `inputNames` | Schönere Namen für Apps und Eingänge |
| `hideApps` | Apps, die in der Liste fehlen sollen |
| `shortcuts` | Bis zu 6 Favoriten, die ersten 3 erscheinen auf dem Hauptbildschirm |

## IDs finden

```bash
sh tools/tv-info.sh <tv-ip>
```

zeigt die HDMI-Eingänge und alle startbaren Apps zum Einfügen.

## Token

Ohne Token kann jeder in deinem Netz über die API Tasten drücken. Mit Token:

- fragt die Web-App einmal danach (Einstellungen → Zugangs-Token) und schickt es als `X-Token`;
- hängen Sprach-Kurzbefehle und Home Assistant `?token=<token>` an die Adresse.

Erstell eins auf der Einstellungsseite (**Token erstellen**) oder mit `openssl rand -hex 12`.
