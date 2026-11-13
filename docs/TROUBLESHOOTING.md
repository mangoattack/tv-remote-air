# Troubleshooting

[Deutsch](TROUBLESHOOTING.de.md) · Quick checks first: `sh tools/tv-info.sh <tv-ip>` and `sh tools/test-remote.sh http://<server>:8080 tv`.

## Connecting to the TV

| Symptom | Cause and fix |
|---|---|
| `failed to connect` / `Connection refused` | Network debugging is off, or the TV only has **Wireless debugging**. Turn it on; for Wireless debugging pair first (`adb pair`), see the [manual](MANUAL.md#2-connect-once-with-adb). |
| `unauthorized` | "Allow USB debugging?" wasn't accepted on the TV. Run `adb connect` again and accept with **Always allow**. Each machine (your PC, the server, the Docker container) needs its own OK. |
| `offline` | Stale connection. `adb disconnect <ip>:5555 && adb connect <ip>:5555`. The server also retries by itself every 60 seconds. |
| `No route to host` on macOS although the port is open | macOS Local Network privacy blocks your terminal. System Settings → Privacy & Security → Local Network → allow the terminal app. |
| Works, then stops after a TV restart | Wireless debugging changes its port after every restart. Use `adb tcpip 5555` once after pairing, or update `host` in Settings. |
| Nothing found by `tools/find-tv.py` | TV off, in another network (guest Wi-Fi, VLAN), or in deep standby. Wake it and try again; type the IP by hand. |

## The remote

| Symptom | Cause and fix |
|---|---|
| Red dots, "not reachable" | See the table above. Also check the IP didn't change (give the TV a fixed IP in the router). |
| "Wrong or missing token" | A token is set on the server. Type it on the phone: Settings → Access token. |
| The page doesn't load on the phone | Wrong address or port, phone on mobile data or a guest network, or a firewall on the server (`sudo ufw allow 8080/tcp`). |
| Buttons are slow | Some TVs take 100-300 ms per key. Use a wired network for the server if you can. The touchpad already sends at most one key at a time. |
| Power on doesn't work | Many TVs turn off networking in standby. Look for "Remote start", "Network standby", "Wake on LAN" or "Quick start" in the TV settings. Some models can't be woken over the network at all. |
| Power off works, power on needs two presses | `power` toggles. Use the keys `on` and `off` in shortcuts for a clear state. |
| HDMI input list is empty | Boxes have no inputs. On TVs, some firmware hides inputs from `dumpsys tv_input`; use `tvButton`/shortcuts with the id from `tools/tv-info.sh`, or the TV's own input key (`input`). |
| Opening an input does nothing | The TV's Live TV app doesn't accept the standard passthrough intent. Try the `input` key, or open the TV's own inputs app as a shortcut. |
| Typing umlauts or emoji | Install [ADBKeyBoard](https://github.com/senzhk/ADBKeyBoard), make it the TV keyboard, turn on "ADBKeyBoard installed" in Settings. |
| Pointer in the TV browser shakes | Use Touchpad mode and lower the touchpad speed in Settings. Small drags give slow, steady movement. |
| Settings page can't save | Docker: `config.json` must be mounted without `:ro`. Linux: the service user needs write access to `remote/config.json`. |

## AirPlay

See [AIRPLAY.md](AIRPLAY.md#it-doesnt-show-up-on-the-iphone).

## Logs

```bash
docker logs -f tv-remote            # Docker
journalctl -u tv-remote -f          # Linux server
adb logcat -d | tail -200           # the TV itself
```

Still stuck? Open an issue with the output (remove IPs and tokens), or ask your AI with this file open.
