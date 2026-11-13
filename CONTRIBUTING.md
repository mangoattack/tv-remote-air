# Contributing

Thanks for helping! The most useful thing you can do is tell us which TVs work.

## Report your TV

Open an issue with:

- TV or box brand and model, Android / Google TV version
- What works (remote, touchpad, keyboard, apps, inputs, power on/off, AirPlay)
- What doesn't, and any error the remote or the AI showed

## Code

- The server is one file, `remote/server.py`, Python standard library only. Please keep it that way.
- The web app is one file, `remote/static/index.html`, no build step and no frameworks.
- Try your change without a TV: `python3 remote/server.py --demo`, then open `http://localhost:8080`.
- New texts in the app go into both languages (`TEXT.en` and `TEXT.de`).
- Never commit your own `config.json`, IP addresses, tokens or ADB keys.

## Prompt

`PROMPT.md` (English) and `PROMPT.de.md` (German) are the same prompt. Change both, and keep the README copies in sync.
