# Probleme lösen

[English](TROUBLESHOOTING.md) · Zuerst schnell prüfen: `sh tools/tv-info.sh <tv-ip>` und `sh tools/test-remote.sh http://<server>:8080 tv`.

## Verbindung zum TV

| Was passiert | Ursache und Lösung |
|---|---|
| `failed to connect` / `Connection refused` | Netzwerk-Debugging ist aus, oder der TV hat nur **Wireless-Debugging**. Einschalten; bei Wireless-Debugging zuerst koppeln (`adb pair`), siehe [Anleitung](MANUAL.de.md#2-einmal-mit-adb-verbinden). |
| `unauthorized` | "USB-Debugging zulassen?" wurde am TV nicht bestätigt. `adb connect` nochmals ausführen und mit **Immer zulassen** bestätigen. Jede Maschine (dein PC, der Server, der Docker-Container) braucht ihr eigenes OK. |
| `offline` | Alte Verbindung. `adb disconnect <ip>:5555 && adb connect <ip>:5555`. Der Server versucht es auch alle 60 Sekunden selbst. |
| `No route to host` auf macOS, obwohl der Port offen ist | Der macOS-Schutz "Lokales Netzwerk" blockiert dein Terminal. Systemeinstellungen → Datenschutz & Sicherheit → Lokales Netzwerk → Terminal erlauben. |
| Geht, dann nach einem TV-Neustart nicht mehr | Wireless-Debugging wechselt nach jedem Neustart den Port. Einmal nach dem Koppeln `adb tcpip 5555` ausführen oder `host` in den Einstellungen anpassen. |
| `tools/find-tv.py` findet nichts | TV aus, in einem anderen Netz (Gäste-WLAN, VLAN) oder im tiefen Standby. Aufwecken und nochmals versuchen; IP von Hand eintippen. |

## Die Fernbedienung

| Was passiert | Ursache und Lösung |
|---|---|
| Rote Punkte, "nicht erreichbar" | Siehe Tabelle oben. Prüf auch, ob sich die IP geändert hat (feste IP im Router vergeben). |
| "Wrong or missing token" | Auf dem Server ist ein Token gesetzt. Am Handy eintippen: Einstellungen → Zugangs-Token. |
| Seite lädt nicht auf dem Handy | Falsche Adresse oder Port, Handy im Mobilnetz oder Gäste-WLAN, oder eine Firewall auf dem Server (`sudo ufw allow 8080/tcp`). |
| Tasten sind langsam | Manche TVs brauchen 100-300 ms pro Taste. Den Server wenn möglich per Kabel anschliessen. Das Touchpad schickt schon nur eine Taste aufs Mal. |
| Einschalten geht nicht | Viele TVs schalten im Standby das Netz ab. Such in den TV-Einstellungen nach "Fernstart", "Netzwerk-Standby", "Wake on LAN" oder "Schnellstart". Manche Modelle lassen sich gar nicht übers Netz wecken. |
| Ausschalten geht, Einschalten braucht zwei Drücke | `power` schaltet um. Nimm in Schnelltasten die Tasten `on` und `off` für einen klaren Zustand. |
| HDMI-Liste ist leer | Boxen haben keine Eingänge. Bei TVs verstecken manche Firmwares die Eingänge vor `dumpsys tv_input`; nutze `tvButton`/Schnelltasten mit der ID aus `tools/tv-info.sh` oder die Eingangs-Taste des TVs (`input`). |
| Eingang öffnen macht nichts | Die Live-TV-App des TVs nimmt den Standard-Befehl nicht an. Probier die Taste `input` oder leg die Eingangs-App des TVs als Schnelltaste an. |
| Umlaute oder Emoji tippen | [ADBKeyBoard](https://github.com/senzhk/ADBKeyBoard) installieren, als TV-Tastatur einstellen, in den Einstellungen "ADBKeyBoard installiert" einschalten. |
| Zeiger im TV-Browser wackelt | Touchpad-Modus nehmen und in den Einstellungen das Touchpad-Tempo senken. Kleine Bewegungen geben langsames, ruhiges Ziehen. |
| Einstellungsseite kann nicht speichern | Docker: `config.json` ohne `:ro` einbinden. Linux: der Dienst-Benutzer braucht Schreibrecht auf `remote/config.json`. |

## AirPlay

Siehe [AIRPLAY.de.md](AIRPLAY.de.md#erscheint-nicht-auf-dem-iphone).

## Logs

```bash
docker logs -f tv-remote            # Docker
journalctl -u tv-remote -f          # Linux-Server
adb logcat -d | tail -200           # der TV selbst
```

Kommst du nicht weiter? Öffne ein Issue mit der Ausgabe (IPs und Tokens entfernen) oder frag deine KI mit dieser Datei offen.
