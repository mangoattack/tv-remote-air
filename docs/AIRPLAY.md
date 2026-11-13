# AirPlay on Android TV

[Deutsch](AIRPLAY.de.md)

AirPlay isn't built into Android TV. This project uses **[AirPlay Server](https://github.com/jqssun/android-airplay-server)** by jqssun: free, open source (GPL-3.0), no ads, no Pro version. It is not made by Apple.

## What works

| | |
|---|---|
| Screen mirroring from iPhone, iPad, Mac | Yes (H.264 and H.265) |
| Videos with the AirPlay button (Safari, Photos, many apps) | Yes |
| Music with cover and track info | Yes |
| Copy-protected apps (Apple TV+, Netflix, Disney+ ...) | **No**, no receiver that isn't Apple's can do this. Use the TV's own app or Chromecast. |
| Android version | 7.0 or newer |

## Install

1. **Play Store on the TV (best, updates itself):** search "AirPlay Server" (by jqssun) and install.
2. **No Play Store:** [F-Droid](https://f-droid.org/packages/io.github.jqssun.airplay) or the latest APK from the [releases](https://github.com/jqssun/android-airplay-server/releases):
   ```bash
   sh tools/airplay-setup.sh <tv-ip> "Living room"
   ```
   The script downloads the latest release, installs it, opens it once and sets the name.
3. Open it once on the TV and allow what it asks for.

## Settings over ADB

```bash
# Name shown on the iPhone
adb shell am broadcast -n io.github.jqssun.airplay/.SettingsReceiver -a io.github.jqssun.airplay.SET_SETTING --es key server_name --es value "Living room"
# List all settings as JSON
adb shell am broadcast -n io.github.jqssun.airplay/.SettingsReceiver -a io.github.jqssun.airplay.LIST_SETTINGS
```

Optional PIN, resolution, overscan, audio latency and more are in the app's own settings.

## Quick button

Add it on the settings page (**+ App** → AirPlay Server) or in `config.json`:

```json
{ "label": "AirPlay", "icon": "airplay", "app": "io.github.jqssun.airplay" }
```

## It doesn't show up on the iPhone

1. Open AirPlay Server on the TV. Some TVs stop background apps; open it again after a restart, or add the quick button.
2. Same network: iPhone and TV must be in the same network and subnet. Not a guest Wi-Fi, no "client isolation" / "AP isolation".
3. mDNS (Bonjour): AirPlay is found by multicast. Mesh systems and some routers block it. Look for "multicast", "IGMP snooping", "mDNS" or "Bonjour" settings, or try with the iPhone on the same access point as the TV.
4. VPN on the iPhone or a Pi-hole/AdGuard with strict rules can also hide it.
5. Restart the app, then the TV.

## Alternatives

If AirPlay Server doesn't work on your TV, there are other receiver apps (for example AirScreen). Their free versions often have ads, time limits or a Pro upsell. Try them only if you're fine with that.
