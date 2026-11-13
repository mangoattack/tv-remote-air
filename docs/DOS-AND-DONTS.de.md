# Was man tun und lassen soll

[English](DOS-AND-DONTS.md) · Regeln für Menschen und für die KI, die einrichtet.

| ✅ Tun | ❌ Lassen |
|---|---|
| Dem TV eine feste IP geben (DHCP-Reservierung im Router) | Router-, DNS- oder Firewall-Einstellungen ohne Nachfrage ändern |
| **Zulassen** nur für den eigenen Computer und Server drücken | Debugging für unbekannte Geräte erlauben |
| Ein Token setzen, wenn Sprachsteuerung oder Home Assistant die API nutzen | Port 8080 oder 5555 ins Internet freigeben |
| AirPlay Server aus dem Play Store installieren, wenn der TV einen hat | APKs von zufälligen Download-Seiten installieren |
| Die Skripte in `tools/` nutzen, sie prüfen, bevor sie handeln | System-Apps, Google-Play-Dienste oder die Eingangs-Apps des TVs abschalten oder löschen |
| Jeden Schritt testen (`tools/test-remote.sh`) | Werkseinstellungen, Root oder Firmware flashen |
| `PROGRESS.md` aktuell halten | Den TV mitten in einer Installation neu starten |
| Ehrlich sagen, wenn etwas auf diesem TV nicht geht | Denselben fehlerhaften Schritt immer wieder versuchen |
| TV Detox oder CleanYourTV fürs Aufräumen nutzen, bewusst und getrennt | Einen Debloat in diese Einrichtung mischen |
| Commits ohne IPs, Tokens, Namen und private Fotos | `remote/config.json` oder `remote/adb-keys/` committen |
