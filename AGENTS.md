# Guide for AI agents

You are working on **TV Remote Air**: a phone web remote and AirPlay for Android TV / Google TV, set up by an AI with a terminal. This file is for you, whether you are setting up a user's TV or changing the code. Claude Code reads it through `CLAUDE.md`, Gemini CLI through `GEMINI.md`, Codex and others read it directly.

## If you are setting up someone's TV

Follow **[PROMPT.md](PROMPT.md)** (or [PROMPT.de.md](PROMPT.de.md)) exactly; the user usually pasted it. In short:

1. Ask for the language first, then the warning, then all questions in one list. Wait for "go".
2. Ask again only before risky steps: installs, developer/ADB settings, launcher, ports, restarts.
3. Check every step yourself before marking it ✓ in `PROGRESS.md`. Report every 30 minutes.
4. Use the tools in `tools/` instead of writing your own:
   | Tool | Use |
   |---|---|
   | `python3 tools/find-tv.py [--json]` | Find TVs, boxes and running servers on the network |
   | `sh tools/tv-info.sh <ip>` | Model, Android version, storage, HDMI input ids, app ids (read-only) |
   | `sh tools/test-remote.sh <url> <dev> [token]` | Press a safe set of keys through the server, report failures |
   | `sh tools/airplay-setup.sh <ip> "<name>"` | Install and name AirPlay Server |
   | `python3 tools/check-readme.py [--fix]` | Keep the prompt copies in the READMEs in sync |
5. Never: factory reset, disable or uninstall system apps, root, change router or DNS settings, mix in a debloat, forward ports to the internet.
6. If a step fails twice, stop and explain.

### Helper agents

If you can start subagents, split the work by job and give each only what it needs: network scout, TV inspector, remote builder, AirPlay installer, frontend checker, integrations, APK builder (only on a second yes), final tester. You stay responsible: check their results.

## If you are changing the code

### Layout

```
PROMPT.md, PROMPT.de.md     the prompt (source of truth; READMEs embed it between <!-- prompt:start/end -->)
README.md, README.de.md     landing pages
remote/server.py            the server: Python standard library only, talks to devices with `adb`
remote/static/index.html    the remote (one file, no build step, no frameworks)
remote/static/settings.html the settings page (/settings)
remote/config.example.json  example config; examples/ has more
remote/Dockerfile, docker-compose.yml, install.sh, run-on-pc.sh, tv-remote.service
tools/                      setup helpers (stdlib Python and POSIX sh)
tests/                      unittest; HTTP tests run the server in --demo mode
docs/                       user docs, English and German (*.de.md)
.github/                    issue and PR templates, CI
```

### Rules

- **Server:** standard library only. Every value that reaches a shell is validated with a strict regex or `shlex.quote`d. `/api/config` must never return IPs or the token.
- **Web app:** one HTML file each, vanilla JS, no CDN, no external fonts. Works offline in the home network. Test at 375×667 (iPhone SE) up to 430×932 (Pro Max). Every text exists in `TEXT.en` and `TEXT.de`.
- **Languages:** English and German only, everywhere (docs, prompt, app).
- **Prompt:** change `PROMPT.md` and `PROMPT.de.md` together, then `python3 tools/check-readme.py --fix`. Every question keeps ≥3 options plus "Other".
- **Privacy:** no real IPs (use 192.168.0.50/.51 or placeholders), no tokens, names, brand-specific private details or personal photos in commits or screenshots. Screenshots come from `--demo` mode.
- **Brands:** the project is for all Android TV / Google TV devices. Don't make it about one TV maker.
- **Credits:** AirPlay Server (jqssun), CleanYourTV (Gathin23), TV Detox (Ansub), ADBKeyBoard (senzhk). Link, don't copy their code.

### Check before you finish

```bash
python3 -m unittest discover -s tests -v
python3 tools/check-readme.py
for f in remote/*.sh tools/*.sh; do sh -n "$f"; done
python3 remote/server.py --demo        # then open http://localhost:8080 and /settings at phone size
```

### Screenshots

Run the demo server, open it at 393×852 with device pixel ratio 3, both layouts, touchpad, apps sheet, keyboard, settings sheet and `/settings`. Save 590×1278 PNGs to `docs/images/`.
