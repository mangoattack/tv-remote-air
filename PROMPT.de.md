Richte mir "TV Remote Air" ein: eine Handy-Fernbedienung im Browser und
AirPlay für meinen Android TV oder Google TV.
Projekt: https://github.com/mangoattack/tv-remote-air

Du bist eine KI mit Terminal auf meinem Computer. Halte dich die ganze
Zeit an diese Regeln.

0. ZUERST DIE SPRACHE. Frag mich vor allem anderen nur das:
   "Welche Sprache sollen wir sprechen? 1) Deutsch 2) English
   3) Eigene Sprache eintippen". Ab dann sprichst du nur noch in dieser
   Sprache mit mir.

1. WARNUNG. Sag mir dann in einfachen Worten und lass es mich bestätigen:
   - Es gibt keine Garantie. Nicht jeder TV funktioniert damit.
   - AirPlay kommt von einer kostenlosen Drittanbieter-App (AirPlay
     Server), nicht von Apple. Manche Apps (Apple TV+, Netflix und
     andere mit Kopierschutz) lassen sich damit nicht spiegeln.
   - Du bist eine KI und kannst Fehler machen.
   - Auf dem TV wird nichts gelöscht oder abgeschaltet. Du schaltest nur
     Netzwerk-Debugging (ADB) ein und installierst Apps erst nach
     meinem Ja.

2. FRAG ZUERST ALLES AB, in einer nummerierten Liste, damit ich so
   antworten kann: "1b 2a 3c". Jede Frage hat mindestens 3 Optionen und
   "Sonstiges: selber eintippen".
   1. Was für ein TV? a) Google TV b) Android TV c) Streaming-Box oder
      Stick (Shield, Mi Box, Chromecast mit Google TV, Fire TV ...)
      d) Sonstiges: Marke und Modell
   2. Wie finden wir ihn? a) Netzwerk automatisch durchsuchen b) Ich
      tippe die IP-Adresse ein c) Zeig mir, wo der TV seine IP anzeigt
      d) Sonstiges
   3. Wo soll die Fernbedienung laufen? a) Docker (NAS, Heimserver,
      Raspberry Pi mit Docker) b) Linux-Server, VM, LXC oder Raspberry
      Pi ohne Docker c) Dieser Computer (geht nur, wenn er läuft)
      d) Sonstiges
   4. Ein zweites Gerät steuern (Box oder Stick am TV)? a) Nein b) Ja,
      eine Android-/Google-TV-Box per ADB c) Ja, mehrere d) Sonstiges
   5. Aussehen der Fernbedienung? a) Klassisch (Apple-Stil, grosses
      Steuerkreuz) b) Wie Apple TV (Play/Pause, Stop, Spulen, Suche,
      TV-Taste) c) Beides umschaltbar, Start mit a) d) Sonstiges
   6. AirPlay? a) Ja, mit AirPlay Server (gratis, Open Source) b) Ja,
      und zeig mir auch Alternativen (AirScreen und andere) c) Kein
      AirPlay d) Sonstiges
   7. Ein schlichter Startbildschirm, der wie Apple TV aussieht? Das
      ist der Launcher von CleanYourTV
      (https://github.com/Gathin23/cleanyourtv), nur der Launcher, ohne
      Debloat. a) Nein, mein Startbildschirm bleibt b) Ja, Launcher
      installieren c) Erst erklären und Bilder zeigen d) Sonstiges
   8. Home Assistant verbinden? a) Nein b) Ja, habe ich (URL gebe ich
      dir) c) Erklär es mir zuerst d) Sonstiges
   9. Sprachsteuerung? (mehrere möglich) a) Keine b) Siri, Apple
      Kurzbefehle, HomePod c) Alexa-Routine d) Android: Google
      Assistant-Routine oder Tasker e) Sonstiges
   10. Welche Handys? a) iPhone b) Android c) Beides d) Sonstiges
   11. Favoriten als Schnelltasten oben in der Fernbedienung (bis zu
       3, mehrere möglich)? a) Ein HDMI-Eingang (Box, Konsole, ...)
       b) Lieblings-Apps c) Browser oder AirPlay d) Sonstiges: selber
       eintippen. Sobald du mit dem TV verbunden bist, zeig mir die
       echte Liste seiner HDMI-Eingänge und Apps und lass mich meine
       Favoriten daraus wählen.
   12. Eine eigene Android-App (APK) für die Fernbedienung? a) Nein,
       die Web-App reicht b) Ja, bau eine (frag mich vor dem Start noch
       einmal) c) Erklär es mir zuerst d) Sonstiges
   Zeig mir dann einen kurzen Plan mit Zeitschätzung und warte auf "go".

3. FRAG NUR BEI RISKANTEN SCHRITTEN NOCHMALS NACH: Installationen (auf
   meinem Computer, dem Server, dem Handy oder dem TV), Änderungen an
   Entwickler- oder ADB-Einstellungen, Launcher-Wechsel, Ports öffnen.
   Alles andere machst du selbst und sagst mir, was du gemacht hast.

4. JEDEN SCHRITT PRÜFEN. Prüf nach jeder Aufgabe das Ergebnis, bevor
   du weitermachst (ausführen, mit curl oder adb testen, Ausgabe
   anschauen), und behebe, was nicht stimmt. Hak einen Schritt erst ab,
   wenn du ihn geprüft hast.
   Kann dein Werkzeug Helfer-Agents (Subagents) starten, setz sie für
   passende Teile ein, jeden mit einer klaren Aufgabe, zum Beispiel:
   - Netzwerk-Sucher: findet TV und Boxen im Netz
   - TV-Einrichtung: ADB-Verbindung, App-IDs, HDMI-Eingänge, AirPlay
   - Fernbedienungs-Bauer: config.json, Start in Docker / Server / PC
   - Frontend-Prüfer: öffnet die Web-App in Handygrösse, prüft jede
     Taste und beide Layouts
   - APK-Bauer (nur, wenn ich die App gewählt habe)
   - Tester: probiert am Schluss alles noch einmal wie ein Nutzer
   Prüf selbst, was jeder Agent meldet. Hat dein Werkzeug keine Agents,
   erledige dieselben Aufgaben nacheinander.

5. FORTSCHRITT. Leg PROGRESS.md im Projektordner als Checkliste an
   (✓ erledigt, ▶ gerade, ○ offen) mit der Restzeit und aktualisiere
   sie nach jedem Schritt. Die Web-App zeigt sie unter Einstellungen →
   Einrichtungs-Fortschritt. Alle 30 Minuten und bei jedem
   Zwischenziel sagst du mir in 2 bis 3 Zeilen, was fertig ist, was als
   Nächstes kommt und wie lange es noch dauert.

6. MIT DEM TV VERBINDEN.
   - Führ mich durch den Entwicklermodus: Einstellungen → System (oder
     Geräteeinstellungen) → Info → 7-mal auf "Build" drücken. Dann in
     den Entwickleroptionen USB-Debugging und Netzwerk-Debugging (oder
     Wireless-Debugging) einschalten.
   - Automatische Suche: such Geräte mit offenem Port 5555 und die
     mDNS-Dienste _adb-tls-connect._tcp, _androidtvremote2._tcp und
     _googlecast._tcp. Zeig mir die Funde mit Namen und lass mich
     wählen. Findest du nichts, sag das, frag, ob der TV im gleichen
     Netz ist, und frag dann nach der IP.
   - Neuere Google TVs haben nur Wireless-Debugging: "Gerät mit
     Kopplungscode koppeln", adb pair, dann adb connect mit dem zweiten
     Port.
   - Der TV fragt "USB-Debugging zulassen?": sag mir, ich soll "Immer
     zulassen" anhaken und OK drücken.
   - Empfiehl mir eine feste IP für den TV (DHCP-Reservierung im
     Router) und zeig mir, wo das geht. Ändere den Router nicht selbst.

7. DIE FERNBEDIENUNG.
   - Klon das Projekt. Erstell remote/config.json aus
     remote/config.example.json mit meinen Geräten, Namen, Schnelltasten
     (HDMI-Eingänge mit "adb shell dumpsys tv_input", Apps mit
     "cmd package query-activities") und "volumeDevice" auf den TV.
   - Starte sie dort, wo ich gewählt habe: Docker → docker compose up
     -d --build in remote/. Linux-Server → sudo sh remote/install.sh
     (systemd). Dieser Computer → sh remote/run-on-pc.sh, und sag mir,
     dass sie nur läuft, solange der Computer an ist.
   - Der ADB-Schlüssel der Maschine, auf der die Fernbedienung läuft,
     muss am TV erlaubt werden. Die Frage "Zulassen?" kommt dafür noch
     einmal.
   - Teste jede Taste mit curl (POST /api/<gerät>/key) und öffne eine
     App, bevor du sagst, dass es geht.
   - Gib mir die Adresse (http://<ip>:8080) und erklär, wie sie auf den
     Home-Bildschirm kommt: iPhone Safari → Teilen → Zum Home-Bildschirm;
     Android Chrome → ⋮ → Zum Startbildschirm hinzufügen.
   - Stell mein Layout als Standard ein (Einstellungen in der App oder
     einmal ?layout=atv in der Adresse).
   - Für den Touchpad-Modus im TV-Browser empfiehl TV Bro (gratis).
   - Für Umlaute und Emoji biete ADBKeyBoard an
     (https://github.com/senzhk/ADBKeyBoard) und setz "adbKeyboard":
     true. Frag vor der Installation.

8. AIRPLAY.
   - Installier AirPlay Server (io.github.jqssun.airplay). Am besten
     aus dem Play Store auf dem TV (aktualisiert sich selbst), sonst
     von F-Droid oder die neueste APK von
     https://github.com/jqssun/android-airplay-server/releases mit adb
     install. Frag vorher.
   - Gib ihm einen Namen: am broadcast -n io.github.jqssun.airplay/.SettingsReceiver
     -a io.github.jqssun.airplay.SET_SETTING --es key server_name
     --es value "<name>"
   - Teste mit mir: iPhone Kontrollzentrum → Bildschirmsynchronisierung.
   - Geht es auf diesem TV nicht: erklär warum, biete Alternativen an
     (AirScreen und andere) und sag ehrlich, dass deren Gratis-Versionen
     Werbung oder Grenzen haben können. Chromecast bleibt als Reserve
     für YouTube und Netflix.

9. EXTRAS, nur was ich gewählt habe:
   - CleanYourTV-Launcher: klon https://github.com/Gathin23/cleanyourtv
     und installier nur den Launcher mit dessen eigenem
     launcher/build-and-install.sh (oder tools/docker-build.sh, wenn
     Java und Android-SDK fehlen, danach SKIP_BUILD=1). Führ den Debloat
     nicht aus. Leg meine Lieblings-Apps und meinen HDMI-Eingang in
     sein Dock, nenne Gathin23 als Urheber, erklär, wie ich zum alten
     Startbildschirm zurückkomme, und frag vor der Installation.
   - Home Assistant: rest_command-Einträge für die Tasten und ein paar
     Knöpfe anlegen, oder die eingebaute Integration "Android TV
     Remote" empfehlen. Setz ein "token" in config.json und nutze es.
   - Siri / Kurzbefehle / HomePod: schreib mir Schritt für Schritt
     Kurzbefehle mit "Inhalte von URL abrufen" →
     http://<ip>:8080/api/<gerät>/key/<taste>?token=<token>
     (Tasten: power, on, off, playpause, stop, volup, voldown, mute,
     home, back, ...). Genauso für App oder Eingang öffnen.
   - Alexa: sag ehrlich, dass es eine Brücke braucht (Home Assistant
     oder einen anderen Dienst), und richte es ein, wenn ich eine habe.
   - Android: eine Google Assistant-Routine oder ein Tasker-Task mit
     HTTP-Anfrage an dieselben Adressen.
   - Android-APK (nur nach erneuter Rückfrage): eine kleine App, die
     das Netz nach dem TV und dem Fernbedienungs-Server durchsucht,
     fragt "Mit <Name> verbinden?", und wenn sie nichts findet, das
     sagt, fragt, ob das Handy im gleichen WLAN ist, und mich dann die
     IP eintippen lässt. Danach zeigt sie die Web-Fernbedienung im
     Vollbild. Bau sie in Docker, damit ich kein Android Studio brauche,
     und erklär mir die Installation (unbekannte Quellen erlauben).

10. ABSCHLUSS.
   - Schlussprüfung: geh alles noch einmal von Anfang bis Ende durch
     (jede Taste, beide Layouts, Touchpad, Tastatur, Apps, Eingänge,
     Lautstärke, Ein/Aus, AirPlay und jedes Extra, das ich gewählt
     habe). Optimiere, was langsam oder umständlich ist, behebe jeden
     Fehler, den du findest, und teste nochmals.
   - Starte den TV einmal neu und prüf, ob sich die Fernbedienung
     wieder verbindet.
   - Sag mir: Netzwerk-Debugging muss an bleiben, damit die
     Fernbedienung geht. Nur Geräte, die ich erlaubt habe, können den TV
     steuern, aber jeder in meinem Netz kann fragen. Ich soll also nur
     für meine eigenen Geräte "Zulassen" drücken.
   - Zeig mir, wie ich alles rückgängig mache: installierte Apps mit
     adb uninstall entfernen, Entwickleroptionen ausschalten,
     Fernbedienung stoppen (docker compose down oder systemctl disable
     --now tv-remote).
   - Erwähne TV Detox (https://github.com/Ansub/tv-detox), falls ich
     zusätzlich einen schnelleren TV mit weniger Werbung will. Das ist
     ein eigenes Projekt mit eigenen Risiken.

Niemals: den TV zurücksetzen, System-Apps abschalten oder löschen,
etwas rooten, Router- oder DNS-Einstellungen ändern oder Dinge tun, die
ich nicht verlangt habe. Klappt ein Schritt zweimal nicht, hör auf,
erklär es einfach und frag mich, wie es weitergeht.
