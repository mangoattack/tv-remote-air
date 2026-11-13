# Alles rückgängig machen

[English](UNINSTALL.md)

Auf dem TV wurde nichts gelöscht oder abgeschaltet, darum geht das schnell. In `PROGRESS.md` steht alles, was die KI installiert hat.

1. **Fernbedienung stoppen**
   ```bash
   cd remote && docker compose down            # Docker
   sudo systemctl disable --now tv-remote      # Linux-Server
   sudo rm /etc/systemd/system/tv-remote.service && sudo rm -rf /opt/tv-remote-air
   ```
   Auf deinem Computer: `run-on-pc.sh` mit Ctrl+C beenden.
2. **Installierte Apps entfernen**
   ```bash
   adb uninstall io.github.jqssun.airplay      # AirPlay Server
   adb uninstall com.android.adbkeyboard       # ADBKeyBoard, falls installiert
   ```
3. **Launcher (nur wenn der CleanYourTV-Launcher installiert wurde):** dessen README folgen, oder am TV: Einstellungen → Apps → Standard-Apps → Startbildschirm-App → die ursprüngliche.
4. **ADB-Schlüssel widerrufen:** Entwickleroptionen → **USB-Debugging-Autorisierungen aufheben**.
5. **Entwickleroptionen ausschalten** (oder mindestens USB-, Netzwerk- und Wireless-Debugging).
6. Das Symbol auf dem Home-Bildschirm des Handys löschen.
