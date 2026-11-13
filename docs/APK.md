# Optional Android app (APK)

The web app is enough for most people. If you want a real app icon on Android that finds the TV by itself, the AI can build a small wrapper app. **It builds it only if you picked it and said yes a second time.** Nothing is published to the Play Store.

## What the app does

1. **First start:** searches the Wi-Fi for TV Remote Air servers (port 8080, `GET /api/config`) and for TVs (port 5555, mDNS `_androidtvremote2._tcp`).
2. **Found something:** "Living room TV found. Connect?" → **Connect** / **Other device**.
3. **Found nothing:** "No TV found." → "Is your phone on the same Wi-Fi as the TV?" → **Search again** / **Type the IP**.
4. **Connected:** shows the web remote full screen (WebView), keeps the screen on while open, remembers the address.
5. **Settings** (long press on the app icon or a menu): change server, search again.

The app contains no remote logic of its own; it shows the server's web app, so it always matches the server version.

## Spec for the AI

- Kotlin, single Activity, `WebView` with JavaScript and DOM storage on, `minSdk 24`, `targetSdk 34`.
- Network permissions only: `INTERNET`, `ACCESS_NETWORK_STATE`, `ACCESS_WIFI_STATE`, `CHANGE_WIFI_MULTICAST_STATE` (for mDNS via `NsdManager`). `usesCleartextTraffic="true"` limited to private addresses through a network security config.
- Scan: the phone's /24, TCP connect with 300 ms timeout, 64 in parallel; then `GET /api/config` on hits with port 8080.
- Texts in English and German, following the phone language.
- Icon: `remote/static/icon-512.png`.
- Build in Docker so no Android Studio is needed (an image with JDK 17 and Android SDK 34, `./gradlew assembleRelease`), sign with a new local debug or release key that stays on the user's machine.
- Output: `android-app/dist/tv-remote-air.apk`. Install: copy to the phone, open it, allow "Install unknown apps" for the file manager or browser, or `adb install` with the phone connected.

Keep the source in `android-app/` in the user's own copy. Don't commit keystores.
