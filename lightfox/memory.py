#!/usr/bin/env python3
"""Report total PSS of a browser with three tabs on three different sites.

Usage: memory.py <binary> <label> [--pref name=value ...] [--wait SECONDS]
"""
import argparse
import http.server
import json
import os
import shutil
import subprocess
import tempfile
import threading
import time

PAGE = b"<!doctype html><title>t</title><p>memory test</p>"


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(PAGE)

    def log_message(self, *args):
        pass


def tree(root):
    pids, frontier = [], [root]
    while frontier:
        pid = frontier.pop()
        pids.append(pid)
        try:
            for task in os.listdir(f"/proc/{pid}/task"):
                with open(f"/proc/{pid}/task/{task}/children") as f:
                    frontier += [int(c) for c in f.read().split()]
        except OSError:
            pass
    return pids


def pss_kb(pid):
    try:
        with open(f"/proc/{pid}/smaps_rollup") as f:
            for line in f:
                if line.startswith("Pss:"):
                    return int(line.split()[1])
    except OSError:
        pass
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("binary")
    ap.add_argument("label")
    ap.add_argument("--pref", action="append", default=[])
    ap.add_argument("--wait", type=int, default=40)
    args = ap.parse_args()

    server = http.server.ThreadingHTTPServer(("0.0.0.0", 0), Handler)
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()

    profile = tempfile.mkdtemp(prefix="lightfox-mem-")
    with open(os.path.join(profile, "user.js"), "w") as f:
        for pref in args.pref:
            name, value = pref.split("=", 1)
            f.write(f'user_pref("{name}", {value});\n')
    urls = [f"http://{host}:{port}/" for host in ("127.0.0.1", "localhost", "127.0.0.2")]
    proc = subprocess.Popen(
        [args.binary, "--headless", "--no-remote", "--profile", profile, *urls],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(args.wait)
    pids = tree(proc.pid)
    total = sum(pss_kb(p) for p in pids)
    proc.terminate()
    try:
        proc.wait(20)
    except subprocess.TimeoutExpired:
        proc.kill()
    shutil.rmtree(profile, ignore_errors=True)
    print(json.dumps({"label": args.label, "pss_mb": round(total / 1024), "processes": len(pids)}))


main()
