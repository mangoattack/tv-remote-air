# Häufige Fragen

[English](FAQ.md)

**Kostet es etwas?** Nein. Die Fernbedienung steht unter MIT-Lizenz, AirPlay Server ist kostenlos und Open Source. Du brauchst ein KI-Werkzeug, das du schon hast (Claude Code, Codex, Gemini CLI ...), oder machst es von Hand.

**Verändert es meinen TV?** Es schaltet Netzwerk-Debugging ein und installiert, wenn du willst, AirPlay Server (und optional ADBKeyBoard oder den CleanYourTV-Launcher). Nichts wird gelöscht oder abgeschaltet. [Rückgängig machen](UNINSTALL.de.md) dauert ein paar Minuten.

**Ist das dasselbe wie TV Detox oder CleanYourTV?** Nein. Die räumen den TV auf (Debloat). Dieses Projekt bringt eine Handy-Fernbedienung und AirPlay. Sie passen gut zusammen.

**Warum nicht einfach die Google-TV-App auf dem Handy?** Geht auch. Diese Fernbedienung bringt dazu ein echtes Touchpad für TV-Browser, Live-Tippen, HDMI-Favoriten, ein zweites Gerät, ein Layout wie Apple TV, Anschlüsse für Sprache und Home Assistant, und sie braucht kein Google-Konto auf dem Handy.

**Geht es auch unterwegs?** Nicht absichtlich. Lass es im Heimnetz. Brauchst du Fernzugriff, nimm ein VPN nach Hause (WireGuard, Tailscale), nie eine Portfreigabe.

**iPhone, Android, iPad?** Alle. Es ist eine Web-App; leg sie auf den Home-Bildschirm. Die Layouts sind vom kleinen iPhone SE bis zum Pro Max getestet.

**Mehrere Handys?** Ja, alle im Heimnetz können die Adresse öffnen. Die Einstellungen "Auf diesem Handy" gelten pro Handy, der Rest für alle.

**Mehrere TVs?** Ja, bis zu 8 Geräte. Oben in der Fernbedienung umschalten.

**Fire TV?** Die Fernbedienung geht über ADB. AirPlay Server kann gehen. Der CleanYourTV-Launcher kann den Fire-OS-Startbildschirm nicht ersetzen.

**Braucht der Server viel Strom?** Nein. Ein Python-Prozess mit ein paar MB RAM; ein Raspberry Pi Zero 2 reicht.

**Welche KI soll ich nehmen?** Jede, die auf deinem Computer Befehle ausführen kann. Der Prompt geht auch mit Werkzeugen, die keine Helfer-Agents starten können.
