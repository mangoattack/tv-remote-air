# Datenschutz

[English](PRIVACY.md)

- **Keine Cloud, kein Konto, kein Tracking.** Die Fernbedienung läuft auf deiner eigenen Maschine und spricht nur über dein Heimnetz mit deinen TVs.
- **Kein Internet nötig** nach der Einrichtung. Die Web-App lädt keine Schriften, Skripte oder Bilder von fremden Servern.
- **Was gespeichert wird:** `remote/config.json` (Gerätenamen, IPs, Favoriten, Token) auf deinem Server; Sprache, Layout und Token im Browser deines Handys; der ADB-Schlüssel in `remote/adb-keys/` oder `~/.android`.
- **Was das Handy sieht:** `/api/config` enthält nie IP-Adressen oder das Token.
- **Logs:** Der Server schreibt kein Anfrage-Log. Im Demo-Modus zeigt er die Befehle, die er schicken würde.
- **AirPlay Server** spricht nur mit Geräten in deinem Netz. Details stehen in seinem eigenen Repository.
- **Das KI-Werkzeug**, mit dem du einrichtest, sieht die Ausgaben im Terminal (IPs, App-Listen). Prüf seine eigenen Datenschutzbedingungen.
