#!/usr/bin/env python3
"""Launch a build headless on a fresh profile and report UI, JS errors and network hosts.

Usage: smoke.py <firefox-binary> <output-dir> [--wait SECONDS]
"""
import argparse
import base64
import json
import os
import re
import shutil
import socket
import subprocess
import tempfile
import time

PORT = 2829
GONE_IDS = [
    "sidebar-main",
    "sidebar-box",
    "sidebar-button",
    "fxa-toolbar-menu-button",
    "ipprotection-button",
    "firefox-view-button",
    "appMenu-fxa-status2",
    "PanelUI-fxa",
]
KEPT_IDS = ["urlbar", "tabbrowser-tabs", "PanelUI-menu-button"]
PAGES = ["about:newtab", "about:preferences", "about:home"]


class Marionette:
    def __init__(self, port):
        for _ in range(120):
            try:
                self.sock = socket.create_connection(("127.0.0.1", port))
                break
            except OSError:
                time.sleep(0.5)
        else:
            raise RuntimeError("marionette never came up")
        self.id = 0
        self._recv()

    def _recv(self):
        size = b""
        while (c := self.sock.recv(1)) != b":":
            size += c
        size = int(size)
        data = b""
        while len(data) < size:
            data += self.sock.recv(size - len(data))
        return json.loads(data)

    def cmd(self, name, params=None):
        self.id += 1
        body = json.dumps([0, self.id, name, params or {}]).encode()
        self.sock.sendall(str(len(body)).encode() + b":" + body)
        _, _, error, result = self._recv()
        if error:
            raise RuntimeError(f"{name}: {error.get('message', error)}")
        return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("binary")
    ap.add_argument("out")
    ap.add_argument("--wait", type=int, default=45)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    profile = tempfile.mkdtemp(prefix="lightfox-smoke-")
    with open(os.path.join(profile, "user.js"), "w") as f:
        f.write('user_pref("devtools.console.stdout.chrome", true);\n')
        f.write('user_pref("browser.dom.window.dump.enabled", true);\n')
        f.write(f'user_pref("marionette.port", {PORT});\n')
        f.write('user_pref("remote.prefs.recommended", false);\n')
    env = dict(os.environ, MOZ_LOG="nsHttp:3,nsHostResolver:5,timestamp", MOZ_HEADLESS="1", MOZ_HEADLESS_WIDTH="1280", MOZ_HEADLESS_HEIGHT="800", MOZ_REMOTE_ALLOW_SYSTEM_ACCESS="1")
    env["MOZ_LOG_FILE"] = os.path.join(args.out, "net")
    log = open(os.path.join(args.out, "stdout.log"), "w")
    proc = subprocess.Popen(
        [args.binary, "--headless", "--marionette", "--no-remote", "--profile", profile],
        stdout=log, stderr=subprocess.STDOUT, env=env)
    report = {"gone_but_present": [], "kept_but_missing": [], "pages": {}}
    try:
        m = Marionette(PORT)
        m.cmd("WebDriver:NewSession", {"capabilities": {}})
        m.cmd("Marionette:SetContext", {"value": "chrome"})
        time.sleep(args.wait)
        check = "return arguments[0].filter(i => { let e = document.getElementById(i); return e && !e.hidden && e.getBoundingClientRect().width > 0; });"
        report["gone_but_present"] = m.cmd("WebDriver:ExecuteScript", {"script": check, "args": [GONE_IDS]})["value"]
        visible = m.cmd("WebDriver:ExecuteScript", {"script": check, "args": [KEPT_IDS]})["value"]
        report["kept_but_missing"] = [i for i in KEPT_IDS if i not in visible]
        report["toolbar_items"] = m.cmd("WebDriver:ExecuteScript", {"script":
            "return [...document.querySelectorAll('#nav-bar-customization-target > *, #TabsToolbar-customization-target > *')].filter(e => e.getBoundingClientRect().width > 0).map(e => e.id);", "args": []})["value"]
        report["console_errors"] = m.cmd("WebDriver:ExecuteScript", {"script":
            "return Services.console.getMessageArray().filter(c => c instanceof Ci.nsIScriptError && !(c.flags & Ci.nsIScriptError.warningFlag) && !(c.flags & Ci.nsIScriptError.infoFlag)).map(c => (c.errorMessage + ' @ ' + c.sourceName + ':' + c.lineNumber).slice(0, 300));", "args": []})["value"]
        shot = m.cmd("WebDriver:TakeScreenshot", {"full": False})["value"]
        open(os.path.join(args.out, "chrome.png"), "wb").write(base64.b64decode(shot))
        m.cmd("Marionette:SetContext", {"value": "content"})
        for page in PAGES:
            try:
                m.cmd("WebDriver:Navigate", {"url": page})
                time.sleep(3)
                text = m.cmd("WebDriver:ExecuteScript", {"script": "return document.documentElement.innerText || '';", "args": []})["value"]
                report["pages"][page] = {"ok": True, "chars": len(text)}
                shot = m.cmd("WebDriver:TakeScreenshot", {"full": False})["value"]
                name = page.replace(":", "_") + ".png"
                open(os.path.join(args.out, name), "wb").write(base64.b64decode(shot))
            except Exception as e:
                report["pages"][page] = {"ok": False, "error": str(e)[:300]}
        try:
            m.cmd("Marionette:Quit")
        except Exception:
            pass
    except Exception as e:
        report["fatal"] = str(e)[:500]
    finally:
        try:
            proc.wait(15)
        except subprocess.TimeoutExpired:
            proc.kill()
        log.close()
        shutil.rmtree(profile, ignore_errors=True)

    hosts = set()
    for name in os.listdir(args.out):
        if name.startswith("net"):
            with open(os.path.join(args.out, name), errors="replace") as f:
                for line in f:
                    for hit in re.finditer(r"(?:https?://|host=|Host: |Resolving host \[|ResolveHost\(?\s*\[?)([a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z]{2,})", line):
                        hosts.add(hit.group(1))
    report["hosts"] = sorted(hosts)
    errors = []
    with open(os.path.join(args.out, "stdout.log"), errors="replace") as f:
        for line in f:
            if re.search(r"console\.error|JavaScript error|TypeError|ReferenceError|SyntaxError|NS_ERROR|Failed to|not found|missing", line):
                errors.append(line.strip()[:260])
    report["error_lines"] = len(errors)
    with open(os.path.join(args.out, "errors.txt"), "w") as f:
        f.write("\n".join(sorted(set(errors))))
    report["exit"] = proc.returncode
    with open(os.path.join(args.out, "report.json"), "w") as f:
        json.dump(report, f, indent=1)
    print(json.dumps(report, indent=1))


main()
