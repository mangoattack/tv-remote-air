# Siri, Shortcuts and HomePod

[Deutsch below](#deutsch)

Every button is an address. The settings page (`/settings` → Voice assistants → Siri) shows the exact address for every key and favourite, with a copy button.

## One shortcut

1. Open the **Shortcuts** app → **+**.
2. Add the action **Get Contents of URL**.
3. Paste the address, e.g. `http://192.168.0.10:8080/api/tv/key/playpause?token=abc123`.
4. Tap the name at the top and call it what you will say, e.g. **"TV pause"**.
5. Say "Hey Siri, TV pause".

For a favourite (HDMI input, app): method **POST**, request body **JSON**, field `index` = number of the favourite (0 = first), address `.../api/tv/shortcut?token=...`.

## Good ones to make

| Name to say | Address ends with |
|---|---|
| TV off | `/api/tv/key/off` |
| TV on | `/api/tv/key/on` |
| TV pause | `/api/tv/key/playpause` |
| TV louder | `/api/tv/key` POST `{"key":"volup","count":5}` |
| TV quieter | `/api/tv/key` POST `{"key":"voldown","count":5}` |
| TV mute | `/api/tv/key/mute` |
| TV Netflix | `/api/tv/app` POST `{"id":"com.netflix.ninja"}` |

## HomePod

HomePod runs your personal shortcuts once **Personal Requests** is on: Home app → Home settings → your user → Personal Requests. Your iPhone must be in the home network.

## Automations

Shortcuts → Automation: e.g. "When I arrive home" → TV on; "At 23:30" → TV off.

---

## Deutsch

Jede Taste ist eine Adresse. Die Einstellungsseite (`/settings` → Sprachassistenten → Siri) zeigt die genaue Adresse für jede Taste und jeden Favoriten mit Kopier-Knopf.

1. App **Kurzbefehle** öffnen → **+**.
2. Aktion **Inhalte von URL abrufen** hinzufügen.
3. Adresse einfügen, z. B. `http://192.168.0.10:8080/api/tv/key/playpause?token=abc123`.
4. Oben auf den Namen tippen und so nennen, wie du es sagst, z. B. **"TV Pause"**.
5. "Hey Siri, TV Pause" sagen.

Für einen Favoriten (HDMI-Eingang, App): Methode **POST**, Anfragetext **JSON**, Feld `index` = Nummer des Favoriten (0 = erster), Adresse `.../api/tv/shortcut?token=...`.

**HomePod:** startet persönliche Kurzbefehle, wenn **Persönliche Anfragen** an ist: Home-App → Einstellungen des Zuhauses → dein Benutzer → Persönliche Anfragen.

**Automationen:** Kurzbefehle → Automation, z. B. "Wenn ich nach Hause komme" → TV an; "Um 23:30" → TV aus.
