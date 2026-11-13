# Security

## How TV Remote Air is meant to run

- Only inside your home network. Never forward port 8080 (the remote) or 5555 (ADB) to the internet. For remote access use a VPN to your home.
- Network debugging on the TV must stay on for the remote to work. The TV only accepts devices that were allowed on its screen, but any device on the network can ask, and on some firmware (`ro.adb.secure=0`) ADB is open to everyone. Keep untrusted devices on a guest network.
- Set a `token` when you use the API from voice assistants or Home Assistant, or when other people share your network.

## What the code does to stay safe

- Every value that reaches the TV's shell is validated (strict patterns for app ids, input ids and hosts) or shell-quoted; key names come from a fixed list.
- `/api/config` never returns IP addresses or the token.
- Static files are served only from `remote/static/`.
- The settings page validates the whole config before saving and writes it atomically where possible.

## Reporting a problem

Please don't open a public issue for a security problem. Use GitHub's **private vulnerability reporting** (Security tab → Report a vulnerability) on this repository. Include what you found, how to reproduce it and what it affects. You'll get an answer as soon as possible.
