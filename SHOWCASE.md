# Showcase

Setups from people who use TV Remote Air. Add yours with a pull request: one row, and a screenshot without personal photos in `docs/showcase/` if you like.

| TV / box | Runs on | Layout | AirPlay | Extras | Notes |
|---|---|---|---|---|---|
| Example: Google TV 55" + streaming box | Raspberry Pi 4, Docker | Apple TV | ✅ AirPlay Server | Siri, Home Assistant | Power on works with "Remote start" on |

**Tips that worked for others**

- Give the TV a fixed IP before anything else.
- Put the box's HDMI input as the first favourite and as the TV button.
- On Google TV, run `adb tcpip 5555` once after pairing Wireless debugging so the port stays the same.
