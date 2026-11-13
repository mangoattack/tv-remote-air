<div align="center">

# TV Remote Air

### Your phone becomes the remote. Your iPhone gets AirPlay. On any Android TV or Google TV.

Claude Code, Codex or any AI with a terminal does the setup. You just answer a few questions and press OK on the TV.

[![License](https://img.shields.io/badge/license-MIT-black)](LICENSE)
[![Works with](https://img.shields.io/badge/works_with-Android_TV_%7C_Google_TV-3DDC84?logo=androidtv&logoColor=white)](#help)
[![Deutsch](https://img.shields.io/badge/Sprache-Deutsch-lightgrey)](README.de.md)

<img src="docs/images/hero.png" alt="TV Remote Air on three phones: classic layout, Apple TV layout and touchpad" width="100%">

</div>

> [!CAUTION]
> **No guarantee.** This is a hobby project that worked for us. Not every TV works, and the AI that sets it up can make mistakes. AirPlay comes from a free third-party app ([AirPlay Server](https://github.com/jqssun/android-airplay-server)), not from Apple. You are responsible for your own TV. Read the [notes and warnings](#notes-and-warnings) first.

<table>
<tr>
<td width="33%" valign="top"><b>📱 A real remote on your phone</b><br>Clickpad, touchpad for TV browsers, live keyboard, all apps, HDMI inputs, volume and power.</td>
<td width="33%" valign="top"><b>📡 AirPlay on Android TV</b><br>Mirror your iPhone, iPad or Mac with a free, open-source AirPlay receiver.</td>
<td width="33%" valign="top"><b>🗣️ Voice and smart home</b><br>Siri Shortcuts, HomePod, Home Assistant, Alexa (via a bridge), Google Assistant or Tasker.</td>
</tr>
</table>

## What you get

| Classic | Apple TV style | Touchpad |
|:-:|:-:|:-:|
| <img src="docs/images/classic.png" width="230"> | <img src="docs/images/atv.png" width="230"> | <img src="docs/images/touchpad.png" width="230"> |
| **All apps** | **Live keyboard** | **Settings** |
| <img src="docs/images/apps.png" width="230"> | <img src="docs/images/keyboard.png" width="230"> | <img src="docs/images/settings.png" width="230"> |

- **Two looks, switchable:** a classic Apple-style remote, or one like the Apple TV remote with play/pause, stop, rewind, fast forward, search and a TV button.
- **Touchpad mode** that moves the pointer in TV browsers smoothly, without shaking.
- **Keyboard** that types on the TV live while you type on the phone.
- **App switcher** with every app on the TV, plus quick buttons for HDMI inputs, a browser or AirPlay.
- **Second device:** control a streaming box behind the TV too; volume always goes to the TV.
- **Made for iPhone** (13 to 17, Pro and Pro Max) and Android phones. Add it to the home screen and it opens like an app.
- **English and German** in the app, everything else in the language you pick at the start.
- **Live setup progress** in the app while the AI works.
- **Small:** one Python file plus `adb`. Runs in Docker, on a Linux server or Raspberry Pi, or on your computer.

## Get started

**1. Turn on developer mode on the TV.**
Settings → System (or Device Preferences) → About → press **Build** 7 times. Then turn on **USB debugging** and **Network debugging** (or **Wireless debugging**) in **Developer options**. [Stuck?](#help)

**2. Open [Claude Code](https://claude.com/claude-code), [Codex](https://openai.com/codex) or another AI with a terminal on your computer.**
The computer and the TV must be on the same network.

**3. Paste this in.**

```text
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
   7. Should the TV wake up with an Apple TV? This uses the launcher
      from https://github.com/Gauthier-Huguenin/appletv-wake-android-tv
      a) No b) Yes, I have an Apple TV c) Explain it first d) Other
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
   - Apple TV wake launcher: follow the README of
     appletv-wake-android-tv, credit Gauthier Huguenin, explain its
     limits, ask before every install.
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
```

The AI asks for your language first, then everything else in one go, then works and tells you every 30 minutes how far it is. It only asks again before installing something or changing a setting.

Prefer to do it yourself? Follow the **[manual setup](docs/MANUAL.md)**.

> [!TIP]
> Want a faster TV with fewer ads as well? Have a look at **[TV Detox](https://github.com/Ansub/tv-detox)**. It's a separate project with its own risks, and it works well next to this one.

### Notes and warnings

> [!WARNING]
> **Do it at your own risk.** There is no guarantee that it works on your TV. The AI can make mistakes. Nothing on the TV is deleted or turned off, and everything can be undone (see [How do I undo everything?](#how-do-i-undo-everything)).

> [!WARNING]
> **Network debugging stays on.** The remote talks to the TV over ADB, so debugging must stay on. Only devices you allowed on the TV screen can control it, but anyone on your network can ask. Only press **Allow** for your own devices, and put guests on a guest network.

> [!NOTE]
> **AirPlay is a third-party app.** [AirPlay Server](https://github.com/jqssun/android-airplay-server) is free and open source (GPL-3.0), not made by Apple. Apps with copy protection (Apple TV+, Netflix and others) can't be mirrored with it. For those, use the TV's own app or Chromecast.

> [!NOTE]
> **The remote only works in your home network.** Don't forward its port to the internet. Set a `token` in `config.json` if you use voice shortcuts or Home Assistant.

## Help

<details>
<summary><b>How do I turn on developer mode?</b></summary>
<br>

1. On the TV, open **Settings**, then **System** (or **Device Preferences**), then **About**.
2. Press OK on **Build** 7 times until you see "You are now a developer."
3. Go back, open **Developer options** and turn on **USB debugging**. If you see **Network debugging** or **Wireless debugging**, turn that on too.
4. The first time a computer connects, the TV asks "Allow USB debugging?" Tick **Always allow** and press **Allow**.

**Newer Google TVs** (Chromecast with Google TV, Google TV Streamer and many 2023+ TVs) usually only have **Wireless debugging**:
open it, choose **Pair device with pairing code**, run `adb pair <ip>:<pairing port>`, type the code, then `adb connect <ip>:<port>` with the port shown on the Wireless debugging screen.

Menus differ by brand. If you're stuck, ask your AI: *"I have a \<brand and model\> TV. How do I turn on network debugging?"*
</details>

<details>
<summary><b>Which TVs does it work on?</b></summary>
<br>

Anything that runs Android TV or Google TV and lets you turn on network debugging: TVs from many brands, and boxes or sticks like Nvidia Shield, Xiaomi Mi Box, Chromecast with Google TV and Fire TV. AirPlay Server needs Android 7 or newer.
It does **not** work on TVs without Android (Tizen, webOS, Roku and others).
Please open an issue with your model, working or not.
</details>

<details>
<summary><b>The remote says "not reachable" or the dots are red.</b></summary>
<br>

- Check the TV is on and on the same network. Many TVs drop network debugging in deep standby. Turning off "Eco" or "Quick start off" modes often helps.
- The TV's IP may have changed. Give it a fixed IP in your router (DHCP reservation) and update `config.json`.
- Run `adb connect <ip>:5555` on the machine that runs the remote. If the TV shows "Allow USB debugging?", allow it.
- "unauthorized" means the prompt on the TV was not accepted yet.
</details>

<details>
<summary><b>The pointer in the TV browser shakes or jumps.</b></summary>
<br>

Use **Touchpad** mode: hold your finger and drag a little in the direction you want, the further the faster. Lift to stop, tap to click. TV browsers move their pointer with arrow keys, so this works best with browsers like [TV Bro](https://github.com/truefedex/tv-bro).
</details>

<details>
<summary><b>Typing umlauts or emoji doesn't work.</b></summary>
<br>

Android's built-in `input text` only handles plain letters. Install [ADBKeyBoard](https://github.com/senzhk/ADBKeyBoard), set it as the keyboard on the TV and set `"adbKeyboard": true` in `config.json`.
</details>

<details>
<summary><b>AirPlay doesn't show up on my iPhone.</b></summary>
<br>

- Open **AirPlay Server** on the TV once, and check iPhone and TV are on the same network (not a guest network, no "client isolation").
- Some routers block the mDNS (Bonjour) traffic AirPlay needs. Look for "multicast" or "IGMP snooping" settings.
- Copy-protected apps can't be mirrored. That's a limit of every AirPlay receiver that isn't from Apple.
- Still nothing? Try an alternative like AirScreen. Its free version can have limits.
</details>

<details>
<summary><b>How do I use Siri, HomePod, Alexa, Google Assistant or Home Assistant?</b></summary>
<br>

Every button is a URL: `http://<server>:8080/api/<device>/key/<key>?token=<token>`
Keys: `power on off playpause play pause stop rewind forward volup voldown mute home back up down left right ok search tv`.

- **Siri / HomePod:** Shortcuts app → new shortcut → **Get contents of URL** with that address → name it ("TV pause"). Siri and HomePod run it by name.
- **Home Assistant:** a `rest_command` per key, or use HA's built-in **Android TV Remote** integration.
- **Alexa:** needs a bridge such as Home Assistant. Then an Alexa routine triggers the HA script.
- **Android:** a Google Assistant routine or a **Tasker** "HTTP Request" with the same URL.

See the [manual](docs/MANUAL.md#voice-and-home-assistant) for examples.
</details>

<details>
<summary><b>How do I undo everything?</b></summary>
<br>

1. Stop the remote: `docker compose down` in `remote/`, or `sudo systemctl disable --now tv-remote`.
2. Remove apps that were installed: `adb uninstall io.github.jqssun.airplay` (and any other the AI lists in `PROGRESS.md`).
3. On the TV, turn off **Developer options**.
</details>

## How it works

The remote is a small web server (`remote/server.py`, Python standard library only). It sends key presses, text and app starts to the TV over ADB, the same tool Android developers use. Your phone opens it as a web app. No cloud, no account, no tracking.

```
iPhone / Android  ──Wi-Fi──▶  remote server (Docker / Linux / PC)  ──ADB──▶  Android TV, box
iPhone            ─────────────────────AirPlay──────────────────────────▶  AirPlay Server app on the TV
```

## Contributing

Issues and pull requests are welcome, especially reports of which TVs work. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Credits

- [AirPlay Server](https://github.com/jqssun/android-airplay-server) by jqssun, the open-source AirPlay receiver for Android (GPL-3.0).
- [AppleTV Wake for Android TV](https://github.com/Gauthier-Huguenin/appletv-wake-android-tv) by Gauthier Huguenin, the optional launcher that wakes the TV with an Apple TV.
- [TV Detox](https://github.com/Ansub/tv-detox) by Ansub Khan, for the idea of letting an AI set up the TV, and the README layout.
- [ADBKeyBoard](https://github.com/senzhk/ADBKeyBoard) for typing any character over ADB.

MIT License. Not affiliated with Apple, Google or any TV maker. AirPlay and Apple TV are trademarks of Apple Inc. Android TV and Google TV are trademarks of Google LLC.
