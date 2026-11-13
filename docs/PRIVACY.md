# Privacy

[Deutsch](PRIVACY.de.md)

- **No cloud, no account, no tracking.** The remote runs on your own machine and talks only to your TVs over your home network.
- **No internet needed** after setup. The web app loads no fonts, scripts or images from other servers.
- **What is stored:** `remote/config.json` (device names, IPs, favourites, token) on your server; language, layout and the token in your phone's browser; the ADB key in `remote/adb-keys/` or `~/.android`.
- **What the phone sees:** `/api/config` never contains IP addresses or the token.
- **Logs:** the server writes no request log. In demo mode it prints the commands it would send.
- **AirPlay Server** talks only to devices in your network. See its own repository for details.
- **The AI tool** you use for setup sees your terminal output (IPs, app lists). Check its own privacy terms.
