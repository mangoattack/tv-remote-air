# Do's and don'ts

[Deutsch](DOS-AND-DONTS.de.md) · Rules for people and for the AI doing the setup.

| ✅ Do | ❌ Don't |
|---|---|
| Give the TV a fixed IP (DHCP reservation in the router) | Change router, DNS or firewall settings without asking |
| Press **Allow** only for your own computer and server | Allow debugging for devices you don't know |
| Set a token if voice control or Home Assistant uses the API | Forward port 8080 or 5555 to the internet |
| Install AirPlay Server from the Play Store if the TV has it | Install APKs from random download sites |
| Use `tools/` scripts, they check before they act | Disable or uninstall system apps, Google Play services or the TV's input apps |
| Test every step (`tools/test-remote.sh`) | Factory reset, root, or flash firmware |
| Keep `PROGRESS.md` up to date | Restart the TV in the middle of an install |
| Tell the user honestly when a feature doesn't work on their TV | Retry the same failing step again and again |
| Use the TV Detox or CleanYourTV projects for cleanup, on purpose and separately | Mix a debloat into this setup |
| Keep commits free of IPs, tokens, names and private photos | Commit `remote/config.json` or `remote/adb-keys/` |
