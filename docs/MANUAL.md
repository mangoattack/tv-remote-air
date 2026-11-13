# Manual setup

Everything the AI does, step by step, if you'd rather do it yourself. Takes about 30 to 60 minutes.
[Deutsch](MANUAL.de.md)

> [!CAUTION]
> No guarantee: not every TV works. AirPlay comes from a third-party app, not from Apple. You are responsible for your own TV.

## What you need

| | |
|---|---|
| **TV** | Android TV or Google TV (or a box/stick with it). Android 7+ for AirPlay. |
| **Phone** | iPhone or Android phone with a browser. |
| **A machine that runs the remote** | Docker host (NAS, home server, Raspberry Pi), a Linux server/VM/LXC, or your computer. It needs Python 3 and `adb`. |
| **Network** | TV, phone and that machine in the same network (no guest Wi-Fi, no client isolation). |

Install `adb` on the machine (not needed for Docker, the image has it):

```bash
sudo apt install adb python3          # Debian, Ubuntu, Raspberry Pi OS
brew install android-platform-tools   # macOS
```

## 1. Settings on the TV

1. **Developer mode:** Settings → System (or Device Preferences) → About → press **Build** 7 times.
2. **Debugging:** Settings → System → Developer options → turn on **USB debugging** and **Network debugging** (on some TVs called **ADB over network**). Newer Google TVs only have **Wireless debugging**, see step 2.
3. **Fixed IP:** find the TV's IP under Settings → Network → your network. Then give it a fixed address in your router (often called *DHCP reservation*, *static lease* or *always use this IP*), so the remote always finds it.
4. **Wake over network (optional):** if your TV has *Remote start*, *Wake on LAN*, *Network standby* or *Quick start*, turn it on. Without it, many TVs can't be switched on from the phone.
5. **Power saving:** if the TV drops off the network in standby, turn off deep standby / Eco modes.

## 2. Connect once with adb

```bash
adb connect <tv-ip>:5555
```

The TV shows **"Allow USB debugging?"** → tick **Always allow** → **Allow**. Then check:

```bash
adb devices          # shows <tv-ip>:5555  device
```

**Wireless debugging only (newer Google TVs):** open Developer options → Wireless debugging → **Pair device with pairing code**. Then:

```bash
adb pair <tv-ip>:<pairing-port>     # type the 6-digit code
adb connect <tv-ip>:<port>          # the port on the Wireless debugging screen
```

That port changes after a restart. Use it in `config.json` as `"host": "<tv-ip>:<port>"`.

## 3. Configure the remote

```bash
git clone https://github.com/mangoattack/tv-remote-air
cd tv-remote-air/remote
cp config.example.json config.json
```

Edit `config.json`:

| Key | What it does |
|---|---|
| `title` | Name shown in the browser tab. |
| `port` | Web port, default `8080`. |
| `token` | Optional password for the API. Needed in the app (Settings) and in voice URLs. Recommended with Siri or Home Assistant. |
| `volumeDevice` | Which device gets volume and mute (usually the TV). |
| `devices.<id>.host` | IP of the TV or box (`ip` or `ip:port`). |
| `devices.<id>.box` | `true` for a box without HDMI inputs. |
| `devices.<id>.adbKeyboard` | `true` if [ADBKeyBoard](https://github.com/senzhk/ADBKeyBoard) is installed (umlauts, emoji). |
| `devices.<id>.tvButton` | What the TV button does, e.g. `{"input": "<hdmi id>"}` or `{"app": "<package/Activity>"}`. Default: Home. |
| `devices.<id>.names` | Nicer names for apps: `{"com.example.app": "My App"}`. |
| `devices.<id>.hideApps` | Packages to hide from the app list. |
| `devices.<id>.inputNames` | Names for HDMI inputs. |
| `devices.<id>.shortcuts` | Up to 3 quick buttons: `{"label", "icon": "hdmi/web/airplay/tv/star", "app" or "input" or "key", "device"}`. |

Find the ids you need:

```bash
adb -s <tv-ip>:5555 shell dumpsys tv_input | grep -o 'TvInputInfo{id=[^,]*'      # HDMI inputs
adb -s <tv-ip>:5555 shell cmd package query-activities --brief -a android.intent.action.MAIN -c android.intent.category.LEANBACK_LAUNCHER   # apps
```

## 4. Start the remote

Pick one:

**Docker** (NAS, home server, Raspberry Pi with Docker)

```bash
cd remote
docker compose up -d --build
```

The ADB key is kept in `remote/adb-keys`, so the TV asks for permission once. Watch the TV when the container starts.

**Linux server, VM, LXC or Raspberry Pi** (systemd)

```bash
sudo sh remote/install.sh
```

**Your computer** (only works while it's on)

```bash
sh remote/run-on-pc.sh
```

Open `http://<ip-of-that-machine>:8080` on your phone. Try a button. If the dots in the header are red, see [Help](../README.md#help).

**Try it without a TV:** `python3 remote/server.py --demo` starts with fake devices.

## 5. Put it on the home screen

- **iPhone:** open the address in **Safari** → Share button → **Add to Home Screen**. It then opens full screen like an app.
- **Android:** open it in **Chrome** → ⋮ → **Add to Home screen** (or **Install app**).

In the app, tap the sliders icon for **Settings**: layout (Classic or Apple TV style), clickpad or touchpad, language, token.

## 6. AirPlay

1. On the TV, install **AirPlay Server** from the Play Store (search "AirPlay Server" by jqssun). No Play Store? Get the APK from [F-Droid](https://f-droid.org/packages/io.github.jqssun.airplay) or the [GitHub releases](https://github.com/jqssun/android-airplay-server/releases) and run `adb install app-release.apk`.
2. Open it once on the TV and allow what it asks for.
3. Optional, set the name your iPhone sees:
   ```bash
   adb shell am broadcast -n io.github.jqssun.airplay/.SettingsReceiver -a io.github.jqssun.airplay.SET_SETTING --es key server_name --es value "Living room"
   ```
4. On the iPhone: Control Center → **Screen Mirroring** → pick the TV.

Add an AirPlay quick button: `{"label": "AirPlay", "icon": "airplay", "app": "io.github.jqssun.airplay"}`.

**Alternatives** if it doesn't work on your TV: AirScreen and similar apps. Their free versions can have ads or limits. Apps with copy protection can't be mirrored by any of them.

## 7. Optional: an Apple TV-style home screen

The launcher from [CleanYourTV](https://github.com/Gathin23/cleanyourtv) by Gathin23 replaces the busy home screen with a calm one that looks like an Apple TV. You can install **only the launcher**, without its debloat:

```bash
git clone https://github.com/Gathin23/cleanyourtv && cd cleanyourtv
export TV_HOST=<tv-ip>
launcher/build-and-install.sh          # needs JDK 17-22 and Android SDK 34, or use tools/docker-build.sh first
```

Read its README for themes, the dock and how to switch back to the stock home screen.

## Voice and Home Assistant

Every key is a URL (add `?token=...` if you set a token):

```
GET  http://<server>:8080/api/<device>/key/<key>
POST http://<server>:8080/api/<device>/key      {"key": "volup", "count": 3}
POST http://<server>:8080/api/<device>/app      {"id": "com.netflix.ninja"}
POST http://<server>:8080/api/<device>/input    {"id": "<hdmi id>"}
POST http://<server>:8080/api/<device>/text     {"text": "hello"}
```

Keys: `power on off playpause play pause stop rewind forward prev next volup voldown mute home back up down left right ok search tv chup chdown options guide info settings recents input captions del enter`.

**Siri, Shortcuts, HomePod:** Shortcuts → **+** → *Get contents of URL* → `http://<server>:8080/api/tv/key/playpause?token=<token>` → name it "TV pause". Say "Hey Siri, TV pause". HomePod runs personal shortcuts once *Personal Requests* is on in the Home app.

**Home Assistant** (`configuration.yaml`):

```yaml
rest_command:
  tv_key:
    url: "http://<server>:8080/api/tv/key/{{ key }}?token=<token>"
    method: GET
```

Then call `rest_command.tv_key` with `key: playpause` from a script or button. HA also has a built-in **Android TV Remote** integration you can use next to this.

**Alexa:** Alexa can't call a local URL by itself. Use a bridge like Home Assistant (with Nabu Casa or the Alexa skill), then trigger the HA script from an Alexa routine.

**Android:** the **HTTP Shortcuts** app, a **Tasker** task with *HTTP Request*, or a Google Assistant routine that runs one of them.

## Security

- The remote has no login by default. It only belongs in your home network. Never forward port 8080 to the internet.
- Set a `token` if other people use your network.
- Network debugging must stay on for the remote. Only devices you allowed on the TV screen can use it, so only press **Allow** for your own devices.

## Undo everything

```bash
docker compose down                          # or: sudo systemctl disable --now tv-remote
adb uninstall io.github.jqssun.airplay       # and any other app you installed
```

Then turn off **Developer options** on the TV.
