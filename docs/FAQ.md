# FAQ

[Deutsch](FAQ.de.md)

**Is it free?** Yes. The remote is MIT licensed, AirPlay Server is free and open source. You need an AI tool you already have (Claude Code, Codex, Gemini CLI ...) or do it by hand.

**Does it change my TV?** It turns on network debugging and, if you agree, installs AirPlay Server (and optionally ADBKeyBoard or the CleanYourTV launcher). Nothing is deleted or disabled. [Undo](UNINSTALL.md) takes a few minutes.

**Is it the same as TV Detox or CleanYourTV?** No. Those clean up the TV (debloat). This project adds a phone remote and AirPlay. They work well together.

**Why not just use the Google TV app on my phone?** That works too. This remote adds a real touchpad for TV browsers, live typing, HDMI favourites, a second device, an Apple TV-style layout, voice and Home Assistant hooks, and runs without a Google account on the phone.

**Does it work outside my home?** Not on purpose. Keep it in your home network. If you need remote access, use a VPN to your home (WireGuard, Tailscale), never port forwarding.

**iPhone, Android, iPad?** All of them. It's a web app; add it to the home screen. Layouts are tested from the small iPhone SE to the Pro Max.

**Several phones?** Yes, everyone in the home network can open the address. "On this phone" settings are per phone, the rest is shared.

**Several TVs?** Yes, up to 8 devices. Switch at the top of the remote.

**Fire TV?** The remote works over ADB. AirPlay Server may work. The CleanYourTV launcher can't replace Fire OS's home screen.

**Does the server need much power?** No. One Python process with a few MB of RAM; a Raspberry Pi Zero 2 is enough.

**Which AI should I use?** Any that can run commands on your computer. The prompt is written so it also works with tools that can't start helper agents.
