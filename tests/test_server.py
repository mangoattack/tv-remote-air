"""Tests for remote/server.py. Run: python3 -m unittest discover -s tests"""
import json
import os
import subprocess
import sys
import time
import unittest
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REMOTE = os.path.join(ROOT, "remote")
sys.argv.append("--demo")              # import the server with the fake devices
sys.path.insert(0, REMOTE)
import server                          # noqa: E402

PORT = 18999


class Parsing(unittest.TestCase):
    def setUp(self):
        self.dev = server.AdbDevice("tv", {"name": "TV", "host": "10.0.0.2", "inputNames": {}})

    def test_inputs_from_dumpsys(self):
        fixture = open(os.path.join(ROOT, "tests", "fixtures", "dumpsys_tv_input.txt")).read()
        self.dev._adb = lambda *a, **k: fixture
        inputs = self.dev.inputs()
        self.assertEqual([i["name"] for i in inputs], ["HDMI 2", "HDMI 3"])   # tuner skipped, no duplicates
        self.assertTrue(inputs[0]["id"].endswith("/HW2"))

    def test_serial_gets_default_port(self):
        self.assertEqual(self.dev.serial, "10.0.0.2:5555")
        self.assertEqual(server.AdbDevice("x", {"host": "10.0.0.3:41234"}).serial, "10.0.0.3:41234")

    def test_pretty_names(self):
        self.assertEqual(self.dev._pretty("com.example.myCoolApp"), "My Cool App")

    def test_key_commands(self):
        sent = []
        self.dev._fast = sent.append
        self.dev.key("up")
        self.dev.key("del", 3)
        self.dev.key("tv")
        self.assertEqual(sent, ["input keyevent KEYCODE_DPAD_UP",
                                "input keyevent KEYCODE_DEL KEYCODE_DEL KEYCODE_DEL",
                                "input keyevent KEYCODE_HOME"])
        with self.assertRaises(server.DeviceError):
            self.dev.key("selfdestruct")

    def test_text_is_quoted_and_ascii(self):
        sent = []
        self.dev._fast = sent.append
        self.dev.text("hi there; rm -rf /")
        self.assertEqual(len(sent), 1)
        self.assertTrue(sent[0].startswith("input text "))
        self.assertIn("hi%sthere", sent[0])            # spaces become %s for Android's input text
        self.assertNotIn(";", sent[0])

    def test_invalid_app_and_input_rejected(self):
        with self.assertRaises(server.DeviceError):
            self.dev.open_app("pkg; reboot")
        with self.assertRaises(server.DeviceError):
            self.dev.set_input("x y")


class Http(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        env = dict(os.environ, PORT=str(PORT))
        cls.proc = subprocess.Popen([sys.executable, os.path.join(REMOTE, "server.py"), "--demo"], env=env,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(50):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{PORT}/api/config", timeout=1)
                return
            except OSError:
                time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        cls.proc.wait()

    def req(self, path, body=None):
        data = json.dumps(body).encode() if body is not None else None
        r = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", data=data,
                                   headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(r, timeout=5) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    def test_config_hides_targets(self):
        code, body = self.req("/api/config")
        cfg = json.loads(body)
        self.assertEqual(code, 200)
        self.assertEqual([d["id"] for d in cfg["devices"]], ["tv", "box"])
        self.assertNotIn("host", json.dumps(cfg))          # IPs never go to the phone

    def test_keys_apps_inputs_shortcuts(self):
        self.assertEqual(self.req("/api/tv/key", {"key": "ok"})[0], 200)
        self.assertEqual(self.req("/api/tv/key/playpause")[0], 200)
        self.assertEqual(self.req("/api/tv/shortcut", {"index": 2})[0], 200)
        self.assertEqual(self.req("/api/box/shortcut", {"index": 0})[0], 200)
        self.assertGreater(len(json.loads(self.req("/api/tv/apps")[1])), 3)
        self.assertEqual(len(json.loads(self.req("/api/tv/inputs")[1])), 4)

    def test_errors(self):
        self.assertEqual(self.req("/api/nope/key", {"key": "ok"})[0], 502)
        self.assertEqual(self.req("/api/tv/key", {"key": "nope"})[0], 502)
        self.assertEqual(self.req("/api/tv/shortcut", {"index": 99})[0], 502)
        self.assertEqual(self.req("/../../etc/passwd")[0], 404)

    def test_static(self):
        code, body = self.req("/")
        self.assertEqual(code, 200)
        self.assertIn(b"TV Remote", body)
        self.assertEqual(self.req("/manifest.webmanifest")[0], 200)


if __name__ == "__main__":
    unittest.main()
