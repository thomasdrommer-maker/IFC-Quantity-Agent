#!/usr/bin/env python3
from pathlib import Path
import os
import sys

PACKAGE_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKAGE_ROOT / "src"))

import errno
import socket
import threading
import time
import urllib.request
import webbrowser


def reserve_listener(host: str, preferred_port: int):
    """Reserve a free port; never open an older application on a busy port."""
    for port in range(preferred_port, min(preferred_port + 20, 65536)):
        try:
            return socket.create_server((host, port))
        except OSError as exc:
            if exc.errno != errno.EADDRINUSE:
                raise
    raise RuntimeError("Kein freier Port gefunden. Bitte bisherigen Agenten beenden.")


def open_when_ready(url: str):
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status == 200:
                    webbrowser.open(url)
                    return
        except OSError:
            pass
        time.sleep(0.2)
    print("Browser bitte manuell oeffnen: " + url, flush=True)


def main():
    import uvicorn
    host = os.getenv("IQA_API_HOST", "127.0.0.1")
    listener = reserve_listener(host, int(os.getenv("IQA_API_PORT", "8000")))
    port = listener.getsockname()[1]
    browser_host = "127.0.0.1" if host == "0.0.0.0" else host
    url = f"http://{browser_host}:{port}/?v=0.3.5"
    print(f"IFC Quantity Agent UI v0.3.5\nPaket: {PACKAGE_ROOT}\nBrowser: {url}", flush=True)
    if os.getenv("IQA_OPEN_BROWSER", "1") != "0":
        threading.Thread(target=open_when_ready, args=(url,), daemon=True).start()
    try:
        uvicorn.Server(uvicorn.Config("ifc_quantity_agent_mvp1.api:app", host=host, port=port)).run(sockets=[listener])
    finally:
        listener.close()


if __name__ == "__main__":
    main()

