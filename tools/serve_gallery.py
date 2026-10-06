"""Serve the local gallery, or start a detached server if none is running.

Usage: .venv/bin/python tools/serve_gallery.py --start
"""
import argparse
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import subprocess
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import ProxyHandler, build_opener


ROOT = Path(__file__).resolve().parents[1]
HEALTH_PATH = "/__gallery_health__"
IDENTITY = {"service": "bio-manim-gallery", "root": str(ROOT)}
LOCAL_HTTP = build_opener(ProxyHandler({}))


class GalleryHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        path = urlsplit(self.path).path
        if path.endswith(("/", ".html")) or path == HEALTH_PATH:
            self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

    def health(self, head=False):
        body = json.dumps(IDENTITY).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if not head:
            self.wfile.write(body)

    def do_GET(self):
        if urlsplit(self.path).path == HEALTH_PATH:
            self.health()
        else:
            super().do_GET()

    def do_HEAD(self):
        if urlsplit(self.path).path == HEALTH_PATH:
            self.health(head=True)
        else:
            super().do_HEAD()


def healthy(base):
    """Only reuse a server that identifies this exact project."""
    try:
        with LOCAL_HTTP.open(base + HEALTH_PATH, timeout=.5) as response:
            payload = response.read(4096)
    except HTTPError as exc:
        raise RuntimeError("This port serves another application; choose --port.") from exc
    except (URLError, OSError):
        return False
    try:
        matching = json.loads(payload) == IDENTITY
    except (ValueError, UnicodeDecodeError):
        matching = False
    if not matching:
        raise RuntimeError("This port serves another application; choose --port.")
    return True


def start(port):
    base = f"http://127.0.0.1:{port}"
    if not healthy(base):
        log_path = ROOT / ".preview" / "server.log"
        log_path.parent.mkdir(exist_ok=True)
        with log_path.open("ab") as log:
            process = subprocess.Popen(
                [sys.executable, str(Path(__file__).resolve()), "--serve", "--port", str(port)],
                cwd=ROOT, stdin=subprocess.DEVNULL, stdout=log,
                stderr=subprocess.STDOUT, start_new_session=True, close_fds=True,
            )
        deadline = time.monotonic() + 6
        while time.monotonic() < deadline:
            if healthy(base):
                break
            if process.poll() is not None:
                raise RuntimeError(f"Gallery server did not start. See {log_path}")
            time.sleep(.1)
        else:
            raise RuntimeError(f"Gallery server did not become ready. See {log_path}")
    print(base + "/previews/", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--start", action="store_true", help="Reuse or start a detached local server")
    mode.add_argument("--serve", action="store_true", help="Run the server in this terminal")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")
    if not (ROOT / "previews" / "index.html").is_file():
        parser.error("Build the gallery first with tools/build_gallery.py")
    try:
        if args.start:
            start(args.port)
        else:
            with ThreadingHTTPServer(("127.0.0.1", args.port), GalleryHandler) as server:
                print(f"http://127.0.0.1:{args.port}/previews/", flush=True)
                server.serve_forever()
    except KeyboardInterrupt:
        pass
    except (OSError, RuntimeError) as exc:
        parser.exit(1, f"Gallery server: {exc}\n")


if __name__ == "__main__":
    main()
