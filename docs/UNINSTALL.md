# Undo everything

[Deutsch](UNINSTALL.de.md)

Nothing on the TV was deleted or disabled, so undoing is short. `PROGRESS.md` lists everything the AI installed.

1. **Stop the remote**
   ```bash
   cd remote && docker compose down            # Docker
   sudo systemctl disable --now tv-remote      # Linux server
   sudo rm /etc/systemd/system/tv-remote.service && sudo rm -rf /opt/tv-remote-air
   ```
   On your computer: stop `run-on-pc.sh` with Ctrl+C.
2. **Remove the apps that were installed**
   ```bash
   adb uninstall io.github.jqssun.airplay      # AirPlay Server
   adb uninstall com.android.adbkeyboard       # ADBKeyBoard, if installed
   ```
3. **Launcher (only if you installed the CleanYourTV launcher):** follow its README to switch Home back, or on the TV: Settings → Apps → Default apps → Home app → the original one.
4. **Revoke the ADB keys:** Developer options → **Revoke USB debugging authorizations**.
5. **Turn off Developer options** (or at least USB, Network and Wireless debugging).
6. Delete the home screen icon on the phone.
