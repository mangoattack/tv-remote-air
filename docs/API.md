# HTTP API

The web app uses this API, and so can Siri Shortcuts, Home Assistant, Tasker or your own scripts.
If a `token` is set, send it as header `X-Token: <token>` or as `?token=<token>`.

| Method | Path | Body | Does |
|---|---|---|---|
| GET | `/api/config` | | Title, devices (names, quick buttons), never IPs. No token needed. |
| GET | `/api/progress` | | Content of `PROGRESS.md`. No token needed. |
| GET | `/api/<dev>/status` | | `{"online": true, "power": true}` |
| GET | `/api/<dev>/apps` | | Launchable apps `[{"id", "name"}]` |
| GET | `/api/<dev>/inputs` | | HDMI and other inputs `[{"id", "name"}]` |
| GET | `/api/<dev>/key/<key>` | | Press a key (handy for voice shortcuts) |
| POST | `/api/<dev>/key` | `{"key": "volup", "count": 3}` | Press a key, optionally several times |
| POST | `/api/<dev>/app` | `{"id": "com.netflix.ninja"}` | Open an app (package or package/Activity) |
| POST | `/api/<dev>/input` | `{"id": "<input id>"}` | Switch input |
| POST | `/api/<dev>/text` | `{"text": "hello"}` | Type text |
| POST | `/api/<dev>/shortcut` | `{"index": 0}` | Run favourite number N |
| POST | `/api/<dev>/refresh` | | Forget cached apps and inputs |
| GET | `/api/admin/config` | | Full config (settings page) |
| POST | `/api/admin/config` | full config | Validate, save and reload |
| GET | `/api/admin/scan` | | Hosts with port 5555 open on the server's network |
| POST | `/api/admin/connect` | `{"host": "192.168.0.50"}` | `adb connect`, returns the adb state |

## Keys

`up down left right ok back home tv` · `playpause play pause stop rewind forward prev next` ·
`volup voldown mute` · `power on off` · `chup chdown guide info options captions input` ·
`search settings recents` · `del enter`

`power` toggles, `on` wakes (KEYCODE_WAKEUP), `off` sleeps (KEYCODE_SLEEP). `tv` does what `tvButton` says, Home by default.

## Examples

```bash
curl http://server:8080/api/tv/key/playpause?token=abc
curl -X POST -H 'Content-Type: application/json' -d '{"key":"voldown","count":5}' http://server:8080/api/tv/key?token=abc
curl -X POST -H 'Content-Type: application/json' -d '{"id":"com.netflix.ninja"}' http://server:8080/api/tv/app?token=abc
```

Errors come back as `{"error": "..."}` with status 400 (bad request), 401 (token), 404 or 502 (the TV refused or isn't reachable).
