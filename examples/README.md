# Examples

| File | For |
|---|---|
| [single-tv.json](single-tv.json) | One TV with three favourite apps |
| [tv-and-box.json](tv-and-box.json) | TV plus a streaming box on HDMI, TV button switches to the box, token set |
| [google-tv-wireless-debugging.json](google-tv-wireless-debugging.json) | Google TV with Wireless debugging (fixed port 5555 after `adb tcpip 5555`) and ADBKeyBoard |
| [home-assistant.yaml](home-assistant.yaml) | rest_command, scripts and a dashboard card |
| [siri-shortcuts.md](siri-shortcuts.md) | Siri, Shortcuts, HomePod, automations |
| [tasker.md](tasker.md) | Android: HTTP Shortcuts, Tasker, Google Assistant |

Copy one to `remote/config.json`, then change names, IPs and ids (`sh tools/tv-info.sh <tv-ip>`), or do it all on the settings page.
The input ids here (`com.example.tvinput/...`) are placeholders; every TV brand has its own.
