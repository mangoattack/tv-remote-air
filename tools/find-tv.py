#!/usr/bin/env python3
"""Find Android TVs, Google TVs and TV Remote Air servers on the local network.

Scans the /24 network of this computer for the ports Android TVs open, reads the friendly name
from the Cast endpoint where it answers, and adds what mDNS knows (avahi-browse or dns-sd).
Only the Python standard library. Changes nothing anywhere; it only opens TCP connections.

    python3 tools/find-tv.py              # table
    python3 tools/find-tv.py --json       # for scripts and AIs
    python3 tools/find-tv.py 10.0.0.0/24  # another network
"""
import concurrent.futures
import ipaddress
import json
import shutil
import socket
import subprocess
import sys
import urllib.request

PORTS = {
    5555: "adb",              # network debugging
    6466: "tv-remote",        # Android TV Remote service (pairing port 6467)
    8008: "cast",             # Chromecast built-in
    8080: "tv-remote-air",    # this project's server (default port)
}


def own_network():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("192.0.2.1", 9))   # TEST-NET address; nothing is sent
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ipaddress.ip_network(f"{ip}/24", strict=False)


def open_ports(host):
    found = []
    for port in PORTS:
        try:
            with socket.create_connection((str(host), port), timeout=0.6):
                found.append(port)
        except OSError:
            pass
    return str(host), found


def cast_name(host):
    try:
        with urllib.request.urlopen(f"http://{host}:8008/setup/eureka_info?params=name,device_info", timeout=2) as r:
            d = json.load(r)
            info = d.get("device_info", {})
            model = " ".join(x for x in (info.get("manufacturer"), info.get("model_name")) if x)
            return d.get("name"), model or None
    except (OSError, ValueError):
        return None, None


def is_remote_air(host):
    try:
        with urllib.request.urlopen(f"http://{host}:8080/api/config", timeout=2) as r:
            return "devices" in json.load(r)
    except (OSError, ValueError):
        return False


def mdns():
    """Names and addresses from mDNS, if avahi-browse is installed (Linux)."""
    out = {}
    if not shutil.which("avahi-browse"):
        return out
    for svc in ("_googlecast._tcp", "_androidtvremote2._tcp", "_adb-tls-connect._tcp", "_airplay._tcp"):
        try:
            res = subprocess.run(["avahi-browse", "-rtp", svc], capture_output=True, text=True, timeout=8).stdout
        except (OSError, subprocess.TimeoutExpired):
            continue
        for line in res.splitlines():
            f = line.split(";")
            if f[0] == "=" and len(f) > 8 and f[2] == "IPv4":
                entry = out.setdefault(f[7], {"mdns": set(), "port": {}})
                entry["mdns"].add(svc)
                entry["port"][svc] = f[8]
                entry.setdefault("name", f[3].replace("\\032", " "))
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    net = ipaddress.ip_network(args[0], strict=False) if args else own_network()
    with concurrent.futures.ThreadPoolExecutor(128) as pool:
        hits = {h: p for h, p in pool.map(open_ports, net.hosts()) if p}
    names = mdns()
    results = []
    for host in sorted(set(hits) | set(names), key=lambda h: ipaddress.ip_address(h)):
        ports = hits.get(host, [])
        name, model = cast_name(host) if 8008 in ports else (None, None)
        m = names.get(host, {})
        kind = "tv-remote-air" if 8080 in ports and is_remote_air(host) else (
            "android-tv" if {5555, 6466} & set(ports) or m.get("mdns", set()) & {"_androidtvremote2._tcp", "_adb-tls-connect._tcp"}
            else "cast" if 8008 in ports else "other")
        if kind == "other":
            continue
        results.append({"ip": host, "kind": kind, "name": name or m.get("name"), "model": model,
                        "adb": 5555 in ports, "wireless_debugging_port": m.get("port", {}).get("_adb-tls-connect._tcp"),
                        "airplay": "_airplay._tcp" in m.get("mdns", set()), "ports": ports})
    if "--json" in sys.argv:
        print(json.dumps(results, indent=2))
        return
    if not results:
        print(f"Nothing found on {net}. Is the TV on, and on the same network as this computer?")
        return
    print(f"{'IP':16} {'KIND':14} {'ADB':4} {'AIRPLAY':8} NAME / MODEL")
    for r in results:
        label = " · ".join(x for x in (r["name"], r["model"]) if x) or "-"
        adb = "yes" if r["adb"] else ("wd" if r["wireless_debugging_port"] else "no")
        print(f"{r['ip']:16} {r['kind']:14} {adb:4} {'yes' if r['airplay'] else 'no':8} {label}")
    print("\nADB 'no' on a TV: turn on Network debugging, or pair Wireless debugging (wd).")


if __name__ == "__main__":
    main()
