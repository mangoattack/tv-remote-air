Set up "TV Remote Air" for me: a phone web remote and AirPlay for my
Android TV or Google TV. Project: https://github.com/mangoattack/tv-remote-air

You are an AI with a terminal on my computer. Follow these rules the
whole time.

0. LANGUAGE FIRST. Before anything else, ask me only this:
   "Which language should we use? 1) Deutsch 2) English 3) Type your
   own language". From then on, talk to me only in that language.

1. WARNING. Then tell me in plain words and ask me to confirm:
   - There is no guarantee. Not every TV works with this.
   - AirPlay comes from a free third-party app (AirPlay Server), not
     from Apple. Some apps (Apple TV+, Netflix and other DRM apps) can't
     be mirrored with it.
   - You are an AI and can make mistakes.
   - Nothing on the TV gets deleted or turned off. You only turn on
     network debugging (ADB) and install apps after I say yes.

2. ASK EVERYTHING FIRST, in one numbered list, so I can answer like
   "1b 2a 3c". Every question has at least 3 options plus
   "Other: type your own".
   1. What is the TV? a) Google TV b) Android TV c) Streaming box or
      stick (Shield, Mi Box, Chromecast with Google TV, Fire TV ...)
      d) Other: brand and model
   2. How do we find it? a) Search my network automatically b) I type
      the IP address c) Show me where the TV shows its IP d) Other
   3. Where should the remote run? a) Docker (NAS, home server,
      Raspberry Pi with Docker) b) A Linux server, VM, LXC or
      Raspberry Pi without Docker c) This computer (only works while it
      is on) d) Other
   4. A second device to control (box or stick behind the TV)?
      a) No b) Yes, one Android/Google TV box over ADB c) Yes, several
      d) Other
   5. Look of the remote? a) Classic (Apple style, big clickpad)
      b) Apple TV style (play/pause, stop, rewind, fast forward,
      search, TV button) c) Both, switchable, start with a) d) Other
   6. AirPlay? a) Yes, with AirPlay Server (free, open source)
      b) Yes, and also show me alternatives (AirScreen and others)
      c) No AirPlay d) Other
   7. A clean home screen that looks like an Apple TV? This is the
      launcher from CleanYourTV (https://github.com/Gathin23/cleanyourtv),
      only the launcher, no debloat. a) No, keep my home screen b) Yes,
      install the launcher c) Explain it first and show screenshots
      d) Other
   8. Connect Home Assistant? a) No b) Yes, I have it (I'll give you
      the URL) c) Explain it first d) Other
   9. Voice control? (several allowed) a) None b) Siri, Apple
      Shortcuts, HomePod c) Alexa routine d) Android: Google Assistant
      routine or Tasker e) Other
   10. Which phones? a) iPhone b) Android c) Both d) Other
   11. Favourites as quick buttons at the top of the remote (up to 3,
       several allowed)? a) An HDMI input (box, console, ...)
       b) Favourite apps c) Browser or AirPlay d) Other: type them.
       Once you are connected to the TV, show me the real list of its
       HDMI inputs and apps and let me pick my favourites from it.
   12. An extra Android app (APK) for the remote? a) No, the web app is
       enough b) Yes, build one (ask me again before you start)
       c) Explain it first d) Other
   Then show me a short plan with a time estimate and wait for "go".

3. ONLY ASK AGAIN FOR RISKY STEPS: installing anything (on my
   computer, the server, the phone or the TV), changing developer or
   ADB settings, changing the launcher, opening ports. Do everything
   else yourself and tell me what you did.

4. CHECK EVERY STEP. After every task, check the result before you
   move on (run it, test it with curl or adb, look at the output) and
   fix what's wrong. Only mark a step ✓ when you checked it.
   If your tool can start helper agents (subagents), use them for
   parts that fit, each with a clear job, for example:
   - Network scout: finds the TV and boxes on the network
   - TV setup: ADB connection, app ids, HDMI inputs, AirPlay
   - Remote builder: config.json, Docker / server / PC start
   - Frontend check: opens the web app at phone size, checks every
     button and both layouts
   - APK builder (only if I picked the app)
   - Tester: tries everything once more like a user would
   Check what each agent reports yourself. If your tool has no agents,
   do the same jobs one after another.

5. PROGRESS. Create PROGRESS.md in the project folder as a checklist
   (✓ done, ▶ now, ○ open) with the time left, and update it after
   every step. The web app shows it under Settings → Setup progress.
   Every 30 minutes, and at every milestone, tell me in 2 or 3 lines
   what is done, what comes next and how much time is left.

6. CONNECT TO THE TV.
   - Walk me through developer mode: Settings → System (or Device
     Preferences) → About → press "Build" 7 times. Then in Developer
     options turn on USB debugging and Network debugging (or Wireless
     debugging).
   - Auto search: look for devices with port 5555 open and for mDNS
     services _adb-tls-connect._tcp, _androidtvremote2._tcp and
     _googlecast._tcp. Show me what you found with names and let me
     pick. If you find nothing, say so, ask if the TV is on the same
     network, and then ask for the IP.
   - Newer Google TVs only have Wireless debugging: use
     "Pair device with pairing code", run adb pair, then adb connect
     with the second port.
   - The TV asks "Allow USB debugging?": tell me to tick "Always allow"
     and press Allow.
   - Recommend a fixed IP for the TV (DHCP reservation in the router)
     and show me how to find that setting. Don't change the router
     yourself.

7. THE REMOTE.
   - Clone the project. Create remote/config.json from
     remote/config.example.json with my devices, names, quick buttons
     (find HDMI input ids with "adb shell dumpsys tv_input" and app ids
     with "cmd package query-activities") and "volumeDevice" set to the
     TV.
   - Run it where I chose: Docker → docker compose up -d --build in
     remote/. Linux server → sudo sh remote/install.sh (systemd). This
     computer → sh remote/run-on-pc.sh, and tell me it only works while
     the computer is on.
   - The ADB key of the machine that runs the remote must be allowed on
     the TV, so the "Allow" prompt appears once more for it.
   - Test every button with curl (POST /api/<device>/key) and open one
     app before you say it works.
   - Give me the address (http://<ip>:8080) and explain how to put it
     on the home screen: iPhone Safari → Share → Add to Home Screen;
     Android Chrome → ⋮ → Add to Home screen.
   - Set my layout as the default (Settings in the app, or
     ?layout=atv once in the URL).
   - For the touchpad mode in TV browsers, suggest TV Bro (free).
   - For typing umlauts and emoji, offer ADBKeyBoard
     (https://github.com/senzhk/ADBKeyBoard) and set "adbKeyboard":
     true. Ask before installing it.

8. AIRPLAY.
   - Install AirPlay Server (io.github.jqssun.airplay). Best from the
     Play Store on the TV (updates itself), else from F-Droid or the
     latest APK on https://github.com/jqssun/android-airplay-server/releases
     with adb install. Ask first.
   - Give it a name: am broadcast -n io.github.jqssun.airplay/.SettingsReceiver
     -a io.github.jqssun.airplay.SET_SETTING --es key server_name
     --es value "<name>"
   - Test with me: iPhone Control Center → Screen Mirroring.
   - If it doesn't work on this TV: explain why, then offer
     alternatives (AirScreen and others) and say honestly that their
     free versions can have ads or limits. Chromecast stays as a backup
     for YouTube and Netflix.

9. EXTRAS, only what I picked:
   - CleanYourTV launcher: clone https://github.com/Gathin23/cleanyourtv
     and install only the launcher with its own launcher/build-and-install.sh
     (or tools/docker-build.sh if Java and the Android SDK are missing,
     then SKIP_BUILD=1). Don't run its debloat. Put my favourite apps
     and HDMI input in its dock, credit Gathin23, explain how to switch
     back to the old home screen, and ask before installing.
   - Home Assistant: add rest_command entries for the keys and a few
     buttons, or suggest the built-in "Android TV Remote" integration.
     Set a "token" in config.json and use it.
   - Siri / Shortcuts / HomePod: write me step by step Shortcuts with
     "Get contents of URL" → http://<ip>:8080/api/<device>/key/<key>?token=<token>
     (keys: power, on, off, playpause, stop, volup, voldown, mute, home,
     back, ...). Same for opening an app or input.
   - Alexa: say honestly that it needs a bridge (Home Assistant or
     another service), then set it up if I have one.
   - Android: a Google Assistant routine or Tasker task with an HTTP
     request to the same URLs.
   - Android APK (only after asking again): a small app that searches
     the network for the TV and the remote server, asks "Connect to
     <name>?", and if it finds nothing says so, asks if the phone is on
     the same Wi-Fi, then lets me type the IP. It then shows the web
     remote full screen. Build it in Docker so I don't need Android
     Studio, and tell me how to install it (allow unknown sources).

10. FINISH.
   - Final review: go through everything once more from start to end
     (every button, both layouts, touchpad, keyboard, apps, inputs,
     volume, power, AirPlay and every extra I picked). Optimise what's
     slow or clumsy, fix every error you find, and test again.
   - Restart the TV once and check the remote reconnects.
   - Tell me: network debugging must stay on for the remote to work.
     Only devices I allowed can control the TV, but anyone on my
     network can ask, so I should only press Allow for my own devices.
   - Show me how to undo everything: adb uninstall the apps you
     installed, turn off developer options, stop the remote (docker
     compose down, or systemctl disable --now tv-remote).
   - Mention TV Detox (https://github.com/Ansub/tv-detox) if I also
     want a faster TV with fewer ads. That's a separate project with
     its own risks.

Never: reset the TV, disable or uninstall system apps, root anything,
change router or DNS settings, or do things I didn't ask for. If a step
fails twice, stop, explain it simply and ask me how to go on.
