# Configuration

Everything lives in `remote/config.json`. You can edit it in the browser at **`http://<server>:8080/settings`** (recommended) or by hand. Start from [`remote/config.example.json`](../remote/config.example.json) or one of the [examples](../examples/).
[Deutsch](CONFIG.de.md)

## The settings page

`/settings` has two parts:

| Part | Saved where | What you set |
|---|---|---|
| **On this phone** | In the phone's browser | Language, layout (Classic / Apple TV), clickpad or touchpad, touchpad speed, vibration, the access token this phone sends |
| **For everyone** | `config.json` on the server | Name, which device gets the volume, TVs and boxes (name, IP, box, ADBKeyBoard), favourites and their order, the API token, ready-to-copy addresses for Siri, Home Assistant, Alexa and Google |

**Search network** finds devices with network debugging on (port 5555). **Connect** runs `adb connect`, so the TV shows "Allow USB debugging?". **+ App / + HDMI input / + Key** list what the TV really has. Press **Save** to apply; the server reloads the devices at once.

With Docker, `config.json` must be mounted writable (the provided `docker-compose.yml` does this).

## All keys

```jsonc
{
  "title": "TV Remote",          // shown in the browser tab and app title
  "port": 8080,                  // web port (env PORT overrides it)
  "token": "",                   // optional API password, see "Token" below
  "volumeDevice": "tv",          // device that gets volume and mute
  "devices": {
    "tv": {                      // id: a-z, 0-9, - and _
      "name": "Living room TV",
      "host": "192.168.0.50",    // IP, or IP:port for Wireless debugging
      "port": 5555,              // only used when host has no port
      "box": false,              // true = no HDMI inputs (streaming box)
      "adbKeyboard": false,      // true when ADBKeyBoard is installed and active
      "tvButton": { "key": "home" },          // or {"input": "..."} or {"app": "..."}
      "names": { "com.example.app": "Nice name" },
      "inputNames": { "<input id>": "PlayStation" },
      "hideApps": ["com.example.helper"],
      "shortcuts": [             // up to 6, the first 3 show on the main screen
        { "label": "HDMI 2", "icon": "hdmi", "input": "<input id>" },
        { "label": "Browser", "icon": "web", "app": "com.phlox.tvwebbrowser/.activity.main.MainActivity" },
        { "label": "AirPlay", "icon": "airplay", "app": "io.github.jqssun.airplay" },
        { "label": "TV", "icon": "tv", "device": "tv", "key": "home" }   // acts on another device
      ]
    }
  }
}
```

Icons: `hdmi`, `web`, `airplay`, `tv`, `star`.
An `app` can be `package/Activity` (exact) or just the package (the launcher activity is started).

## Finding ids

```bash
sh tools/tv-info.sh <tv-ip>
```

prints the HDMI input ids and every launchable app, ready to paste.

## Token

Without a token, anyone on your network can press buttons through the API. With a token:

- the web app asks for it once (Settings → Access token) and sends it as `X-Token`;
- voice shortcuts and Home Assistant add `?token=<token>` to the URL.

Create one on the settings page (**Create token**) or with `openssl rand -hex 12`.

## Environment variables

| Variable | Default | Use |
|---|---|---|
| `TV_REMOTE_CONFIG` | `remote/config.json` | Path to the config file |
| `TV_REMOTE_PROGRESS` | `PROGRESS.md` in the repo | File shown under Settings → Setup progress |
| `PORT` | `port` from config | Web port |
