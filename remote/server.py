#!/usr/bin/env python3
"""TV Remote Air: an iPhone/Android web remote for Android TV and Google TV.

Talks to every TV or streaming box over network ADB and serves the web app on the LAN.
Only the Python standard library and the `adb` command are needed. Devices live in config.json.

    python3 server.py              # uses config.json next to this file
    python3 server.py --demo       # fake devices, for screenshots and UI work
"""
import concurrent.futures
import ipaddress
import json
import os
import re
import shlex
import socket
import subprocess
import sys
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(HERE, "static")
DEMO = "--demo" in sys.argv
CONFIG_PATH = os.environ.get("TV_REMOTE_CONFIG", os.path.join(HERE, "config.json"))
if DEMO:
    CONFIG_PATH = os.path.join(HERE, "config.example.json")
with open(CONFIG_PATH, encoding="utf-8") as f:
    CONFIG = json.load(f)
PROGRESS = os.environ.get("TV_REMOTE_PROGRESS", os.path.join(HERE, "..", "PROGRESS.md"))


class DeviceError(Exception):
    pass


# Friendly names for common packages that show up without a readable label.
KNOWN_APPS = {
    "com.google.android.youtube.tv": "YouTube",
    "com.google.android.youtube.tvkids": "YouTube Kids",
    "com.google.android.youtube.tvmusic": "YouTube Music",
    "com.netflix.ninja": "Netflix",
    "com.disney.disneyplus": "Disney+",
    "com.amazon.amazonvideo.livingroom": "Prime Video",
    "com.apple.atve.androidtv.appletv": "Apple TV",
    "com.spotify.tv.android": "Spotify",
    "org.jellyfin.androidtv": "Jellyfin",
    "com.plexapp.android": "Plex",
    "org.xbmc.kodi": "Kodi",
    "com.wbd.stream": "Max",
    "tv.pluto.android": "Pluto TV",
    "com.crunchyroll.crunchyroid": "Crunchyroll",
    "com.phlox.tvwebbrowser": "TV Bro",
    "io.github.jqssun.airplay": "AirPlay Server",
    "com.ionitech.airscreen": "AirScreen",
    "com.android.tv.settings": "Settings",
    "com.google.android.tv.settings": "Settings",
}


# --------------------------------------------------------------------------- Android TV over ADB

class AdbDevice:
    # Our button names -> Android key codes. Several codes in one string are sent as one event list.
    KEYS = {
        "up": "DPAD_UP", "down": "DPAD_DOWN", "left": "DPAD_LEFT", "right": "DPAD_RIGHT",
        "ok": "DPAD_CENTER", "back": "BACK", "home": "HOME", "volup": "VOLUME_UP",
        "voldown": "VOLUME_DOWN", "mute": "VOLUME_MUTE", "play": "MEDIA_PLAY", "pause": "MEDIA_PAUSE",
        "playpause": "MEDIA_PLAY_PAUSE", "stop": "MEDIA_STOP", "rewind": "MEDIA_REWIND",
        "forward": "MEDIA_FAST_FORWARD", "prev": "MEDIA_PREVIOUS", "next": "MEDIA_NEXT",
        "chup": "CHANNEL_UP", "chdown": "CHANNEL_DOWN", "power": "POWER", "on": "WAKEUP",
        "off": "SLEEP", "options": "MENU", "guide": "GUIDE", "info": "INFO", "search": "SEARCH",
        "settings": "SETTINGS", "recents": "APP_SWITCH", "input": "TV_INPUT", "captions": "CAPTIONS",
        "del": "DEL", "enter": "ENTER",
    }

    def __init__(self, dev_id, cfg):
        self.id = dev_id
        self.cfg = cfg
        self.name = cfg.get("name", dev_id)
        host = cfg["host"]
        self.serial = host if ":" in host else f"{host}:{cfg.get('port', 5555)}"
        self.lock = threading.Lock()
        self._shell = None
        self._apps = None
        self._inputs = None

    # ---- plumbing

    def _adb(self, *args, timeout=8):
        cmd = ["adb", "-s", self.serial, *args]
        for attempt in range(2):
            try:
                p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            except subprocess.TimeoutExpired:
                raise DeviceError(f"{self.name} does not answer")
            except FileNotFoundError:
                raise DeviceError("adb is not installed on the server")
            err = (p.stderr + p.stdout).lower()
            if p.returncode == 0 and "error:" not in err:
                return p.stdout
            if "unauthorized" in err:
                raise DeviceError(f"{self.name}: allow USB debugging for this server on the TV screen")
            if attempt == 0 and ("not found" in err or "offline" in err or "closed" in err or "no devices" in err):
                self.connect()
                continue
            raise DeviceError(f"{self.name} not reachable: " + (p.stderr or p.stdout).strip()[:120])

    def connect(self):
        subprocess.run(["adb", "disconnect", self.serial], capture_output=True, timeout=5)
        subprocess.run(["adb", "connect", self.serial], capture_output=True, timeout=10)
        self._close_shell()

    def _close_shell(self):
        if self._shell:
            try:
                self._shell.kill()
            except OSError:
                pass
        self._shell = None

    def _fast(self, command):
        """Run a shell command through one long-lived `adb shell`, without waiting for it.

        Starting a fresh adb process per key adds 50-150 ms of jitter, which makes the touchpad shaky.
        A persistent shell keeps keys in order and quick. Falls back to a normal call on failure.
        """
        with self.lock:
            for attempt in range(2):
                if self._shell is None or self._shell.poll() is not None:
                    try:
                        self._shell = subprocess.Popen(["adb", "-s", self.serial, "shell"], stdin=subprocess.PIPE,
                                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True)
                    except FileNotFoundError:
                        raise DeviceError("adb is not installed on the server")
                try:
                    self._shell.stdin.write(command + "\n")
                    self._shell.stdin.flush()
                    return
                except (BrokenPipeError, OSError, ValueError):
                    self._close_shell()
                    if attempt == 0:
                        self.connect()
        self._adb("shell", command)

    # ---- actions

    def key(self, key, count=1):
        code = self.KEYS.get(key)
        if key == "tv" and self.cfg.get("tvButton"):
            return self._open_target(self.cfg["tvButton"])
        if key == "tv":
            code = "HOME"
        if not code:
            raise DeviceError(f"{self.name} has no key {key}")
        count = max(1, min(int(count), 100))
        self._fast("input keyevent " + " ".join(["KEYCODE_" + code] * count))

    def apps(self):
        if self._apps is None:
            out = self._adb("shell", "cmd", "package", "query-activities", "--brief", "-a",
                            "android.intent.action.MAIN", "-c", "android.intent.category.LEANBACK_LAUNCHER")
            names = self.cfg.get("names", {})
            hidden = set(self.cfg.get("hideApps", []))
            seen, apps = set(), []
            for line in out.splitlines():
                line = line.strip()
                if "/" not in line or line in seen:
                    continue
                seen.add(line)
                pkg = line.split("/")[0]
                if pkg in hidden or line in hidden:
                    continue
                name = names.get(line) or names.get(pkg) or KNOWN_APPS.get(pkg) or self._pretty(pkg)
                apps.append({"id": line, "name": name, "icon": None})
            apps.sort(key=lambda a: a["name"].lower())
            self._apps = apps
        return self._apps

    @staticmethod
    def _pretty(pkg):
        parts = [p for p in pkg.split(".") if p not in ("com", "tv", "android", "androidtv", "app", "application",
                                                           "org", "net", "de", "ch", "io")]
        word = parts[-1] if parts else pkg
        return re.sub(r"(?<!^)(?=[A-Z])", " ", word).replace("_", " ").title()

    def open_app(self, component):
        if re.fullmatch(r"[\w.]+/[\w.$]+", component):
            self._adb("shell", "am", "start", "-n", component)
        elif re.fullmatch(r"[\w.]+", component):
            self._adb("shell", "monkey", "-p", component, "-c", "android.intent.category.LEANBACK_LAUNCHER", "1")
        else:
            raise DeviceError("Invalid app")

    def inputs(self):
        """HDMI and other inputs from the TV input framework. Empty on boxes without inputs."""
        if self._inputs is None:
            try:
                out = self._adb("shell", "dumpsys", "tv_input", timeout=10)
            except DeviceError:
                out = ""
            names = self.cfg.get("inputNames", {})
            seen, inputs = set(), []
            for m in re.finditer(r"TvInputInfo\{id=([^,}\s]+)(?:,\s*type=(\w+))?", out):
                iid, kind = m.group(1), (m.group(2) or "").upper()
                if iid in seen or kind in ("TUNER", "OTHER") and iid not in names:
                    continue
                seen.add(iid)
                hw = re.search(r"HW(\d+)$", iid)
                inputs.append({"id": iid, "name": names.get(iid) or (f"{kind or 'Input'} {hw.group(1)}" if hw else iid.split("/")[-1]),
                               "connected": True})
            self._inputs = inputs
        return self._inputs

    def set_input(self, iid):
        if not re.fullmatch(r"[\w.$/]+", iid):
            raise DeviceError("Invalid input")
        uri = "content://android.media.tv/passthrough/" + urllib.parse.quote(iid, safe="")
        self._adb("shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", uri)

    def _open_target(self, target):
        """A shortcut target: {"app": "pkg/Activity"}, {"input": "<tv input id>"} or {"key": "home"}."""
        if "input" in target:
            return self.set_input(target["input"])
        if "app" in target:
            return self.open_app(target["app"])
        if "key" in target:
            return self.key(target["key"])
        raise DeviceError("Shortcut without a target")

    def text(self, text):
        if self.cfg.get("adbKeyboard"):
            # ADBKeyBoard (github.com/senzhk/ADBKeyBoard) types any character, umlauts and emoji included.
            self._fast("am broadcast -a ADB_INPUT_TEXT --es msg " + shlex.quote(text))
            return
        # Plain `input text` only handles ASCII; spaces must be %s.
        safe = re.sub(r"[^\w .,@:/?=&+\-_!#*()]", "", text.encode("ascii", "ignore").decode())
        if safe:
            self._fast("input text " + shlex.quote(safe.replace(" ", "%s")))

    def status(self):
        try:
            out = self._adb("shell", "dumpsys", "power", "|", "grep", "-m1", "mWakefulness=", timeout=4)
            return {"online": True, "power": "Awake" in out}
        except DeviceError as e:
            return {"online": False, "error": str(e)}


class DemoDevice(AdbDevice):
    """Pretends to be a TV, so the web app can be tried and screenshotted without hardware."""

    def _adb(self, *args, timeout=8):
        return ""

    def _fast(self, command):
        print(f"[demo] {self.name}: {command}", flush=True)

    def apps(self):
        names = ["YouTube", "Netflix", "Disney+", "Prime Video", "Apple TV", "Spotify", "Jellyfin", "Kodi",
                 "TV Bro", "AirPlay Server", "Plex", "Settings"]
        return [{"id": f"demo.{i}/.Main", "name": n, "icon": None} for i, n in enumerate(names)]

    def inputs(self):
        return [] if self.cfg.get("box") else [{"id": f"demo/HW{i}", "name": f"HDMI {i}", "connected": i < 3}
                                               for i in range(1, 5)]

    def open_app(self, component):
        print(f"[demo] {self.name}: open {component}", flush=True)

    def set_input(self, iid):
        print(f"[demo] {self.name}: input {iid}", flush=True)

    def status(self):
        return {"online": True, "power": True}


DEVICES = {}


def load_devices():
    """(Re)builds the device objects from CONFIG, e.g. after the settings page saved a change."""
    DEVICES.clear()
    for dev_id, cfg in CONFIG["devices"].items():
        DEVICES[dev_id] = (DemoDevice if DEMO else AdbDevice)(dev_id, cfg)


load_devices()


# --------------------------------------------------------------------------- settings page backend

ID_RE = re.compile(r"[a-z0-9_-]{1,32}")
HOST_RE = re.compile(r"[A-Za-z0-9.-]{1,253}(:\d{1,5})?")
SHORTCUT_KEYS = {"label", "icon", "app", "input", "key", "device"}


def validate_config(new):
    """Checks a config from the settings page; returns a clean copy or raises DeviceError."""
    if not isinstance(new, dict) or not isinstance(new.get("devices"), dict) or not new["devices"]:
        raise DeviceError("At least one device is needed")
    out = {"title": str(new.get("title") or "TV Remote")[:40],
           "port": int(new.get("port") or CONFIG.get("port", 8080)),
           "token": str(new.get("token") or "")[:64],
           "volumeDevice": str(new.get("volumeDevice") or ""),
           "devices": {}}
    for dev_id, d in list(new["devices"].items())[:8]:
        if not ID_RE.fullmatch(dev_id) or not isinstance(d, dict):
            raise DeviceError(f"Invalid device id {dev_id!r} (a-z, 0-9, - and _ only)")
        host = str(d.get("host", "")).strip()
        if not HOST_RE.fullmatch(host):
            raise DeviceError(f"Invalid IP or host for {dev_id}")
        dev = {"name": str(d.get("name") or dev_id)[:30], "host": host}
        if not ":" in host and d.get("port"):
            dev["port"] = int(d["port"])
        for flag in ("box", "adbKeyboard"):
            if d.get(flag):
                dev[flag] = True
        for key in ("names", "inputNames"):
            if isinstance(d.get(key), dict):
                dev[key] = {str(k)[:200]: str(v)[:40] for k, v in d[key].items()}
        if isinstance(d.get("hideApps"), list):
            dev["hideApps"] = [str(x)[:200] for x in d["hideApps"]][:100]
        if isinstance(d.get("tvButton"), dict):
            dev["tvButton"] = {k: str(v)[:200] for k, v in d["tvButton"].items() if k in SHORTCUT_KEYS}
        shortcuts = []
        for s in (d.get("shortcuts") or [])[:6]:
            if isinstance(s, dict) and ({"app", "input", "key"} & set(s)):
                shortcuts.append({k: str(v)[:200] for k, v in s.items() if k in SHORTCUT_KEYS})
        dev["shortcuts"] = shortcuts
        out["devices"][dev_id] = dev
    if out["volumeDevice"] not in out["devices"]:
        out["volumeDevice"] = next(iter(out["devices"]))
    return out


def save_config(new):
    global CONFIG
    clean = validate_config(new)
    if not DEMO:                    # demo mode keeps changes in memory only
        text = json.dumps(clean, indent=2, ensure_ascii=False) + "\n"
        tmp = CONFIG_PATH + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(text)
            os.replace(tmp, CONFIG_PATH)
        except OSError:
            # A single bind-mounted file (Docker) can't be replaced, only rewritten.
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                f.write(text)
    CONFIG = clean
    load_devices()
    if not DEMO:
        for d in DEVICES.values():
            threading.Thread(target=d.connect, daemon=True).start()
    return clean


def scan_network():
    """Hosts on the server's /24 network with network debugging (port 5555) open."""
    if DEMO:
        return [{"host": "192.168.0.50", "name": "Demo TV"}, {"host": "192.168.0.51", "name": "Demo box"}]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("192.0.2.1", 9))            # TEST-NET address; nothing is sent
        net = ipaddress.ip_network(s.getsockname()[0] + "/24", strict=False)
    finally:
        s.close()

    def probe(ip):
        try:
            with socket.create_connection((str(ip), 5555), timeout=0.5):
                return str(ip)
        except OSError:
            return None

    with concurrent.futures.ThreadPoolExecutor(64) as pool:
        found = [ip for ip in pool.map(probe, net.hosts()) if ip]
    known = {d.serial.split(":")[0]: d.name for d in DEVICES.values()}
    return [{"host": ip, "name": known.get(ip, "")} for ip in found]


def connect_host(host):
    """adb connect once, so the TV shows "Allow USB debugging?"; returns the adb state."""
    if not HOST_RE.fullmatch(host):
        raise DeviceError("Invalid IP or host")
    if DEMO:
        return "device"
    serial = host if ":" in host else host + ":5555"
    subprocess.run(["adb", "connect", serial], capture_output=True, timeout=10)
    p = subprocess.run(["adb", "-s", serial, "get-state"], capture_output=True, text=True, timeout=10)
    return (p.stdout or p.stderr).strip().split("\n")[-1][:80]


def public_device(dev):
    return {"id": dev.id, "name": dev.name, "box": bool(dev.cfg.get("box")),
            "shortcuts": [{"label": s.get("label", "?"), "icon": s.get("icon", "")} for s in dev.cfg.get("shortcuts", [])]}


# --------------------------------------------------------------------------- HTTP

TYPES = {".html": "text/html; charset=utf-8", ".js": "text/javascript", ".css": "text/css",
         ".png": "image/png", ".json": "application/json", ".webmanifest": "application/manifest+json",
         ".svg": "image/svg+xml", ".md": "text/markdown; charset=utf-8"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _json(self, obj, code=200):
        data = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _authorized(self, url):
        # Optional shared token, for voice shortcuts and Home Assistant. The web app sends it as a header.
        token = CONFIG.get("token")
        if not token:
            return True
        given = self.headers.get("X-Token") or urllib.parse.parse_qs(url.query).get("token", [""])[0]
        return given == token

    def _device(self, dev_id):
        dev = DEVICES.get(dev_id)
        if not dev:
            raise DeviceError("Unknown device")
        return dev

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        parts = url.path.strip("/").split("/")
        try:
            if url.path == "/api/config":
                return self._json({"title": CONFIG.get("title", "TV Remote"), "tokenRequired": bool(CONFIG.get("token")),
                                   "volumeDevice": CONFIG.get("volumeDevice"),
                                   "devices": [public_device(d) for d in DEVICES.values()]})
            if url.path == "/api/progress":
                text = open(PROGRESS, encoding="utf-8").read() if os.path.isfile(PROGRESS) else ""
                return self._json({"text": text})
            if parts[0] == "api" and not self._authorized(url):
                return self._json({"error": "Wrong or missing token"}, 401)
            if url.path == "/api/admin/config":
                return self._json(CONFIG)
            if url.path == "/api/admin/scan":
                return self._json(scan_network())
            if len(parts) == 3 and parts[0] == "api":
                dev = self._device(parts[1])
                if parts[2] == "status":
                    return self._json(dev.status())
                if parts[2] == "apps":
                    return self._json(dev.apps())
                if parts[2] == "inputs":
                    return self._json(dev.inputs())
            # GET /api/<device>/key/<key> so a voice shortcut can call a plain URL.
            if len(parts) == 4 and parts[0] == "api" and parts[2] == "key":
                self._device(parts[1]).key(parts[3])
                return self._json({"ok": True})
            return self._static(url.path)
        except DeviceError as e:
            return self._json({"error": str(e)}, 502)

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        parts = url.path.strip("/").split("/")
        length = int(self.headers.get("Content-Length") or 0)
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except ValueError:
            return self._json({"error": "Invalid request"}, 400)
        if not self._authorized(url):
            return self._json({"error": "Wrong or missing token"}, 401)
        try:
            if url.path == "/api/admin/config":
                return self._json(save_config(body))
            if url.path == "/api/admin/connect":
                return self._json({"state": connect_host(str(body.get("host", "")))})
            if len(parts) != 3 or parts[0] != "api":
                return self._json({"error": "Not found"}, 404)
            dev, action = self._device(parts[1]), parts[2]
            if action == "key":
                dev.key(str(body.get("key", "")), body.get("count", 1))
            elif action == "app":
                dev.open_app(str(body.get("id", "")))
            elif action == "input":
                dev.set_input(str(body.get("id", "")))
            elif action == "text":
                dev.text(str(body.get("text", ""))[:500])
            elif action == "shortcut":
                shortcuts = dev.cfg.get("shortcuts", [])
                i = int(body.get("index", -1))
                if not 0 <= i < len(shortcuts):
                    raise DeviceError("Unknown shortcut")
                target = shortcuts[i]
                (self._device(target["device"]) if target.get("device") else dev)._open_target(target)
            elif action == "refresh":
                dev._apps = dev._inputs = None
            else:
                return self._json({"error": "Not found"}, 404)
            return self._json({"ok": True})
        except (DeviceError, ValueError, TypeError) as e:
            return self._json({"error": str(e)}, 502 if isinstance(e, DeviceError) else 400)

    def _static(self, path):
        if path in ("", "/"):
            path = "/index.html"
        elif path in ("/settings", "/settings/"):
            path = "/settings.html"
        full = os.path.realpath(os.path.join(STATIC, path.lstrip("/")))
        if not full.startswith(STATIC + os.sep) or not os.path.isfile(full):
            self.send_error(404)
            return
        with open(full, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", TYPES.get(os.path.splitext(full)[1], "application/octet-stream"))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def keep_connected():
    # TVs drop idle ADB connections and change state on standby; reconnect quietly in the background.
    while True:
        for d in DEVICES.values():
            try:
                out = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=5).stdout
                if f"{d.serial}\tdevice" not in out:
                    subprocess.run(["adb", "connect", d.serial], capture_output=True, timeout=10)
            except (OSError, subprocess.TimeoutExpired):
                pass
        time.sleep(60)


if __name__ == "__main__":
    if not DEMO:
        for d in DEVICES.values():
            subprocess.run(["adb", "connect", d.serial], capture_output=True, timeout=15)
        threading.Thread(target=keep_connected, daemon=True).start()
    port = int(os.environ.get("PORT") or CONFIG.get("port", 8080))
    print(f"TV Remote Air on http://0.0.0.0:{port}" + (" (demo)" if DEMO else ""), flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
