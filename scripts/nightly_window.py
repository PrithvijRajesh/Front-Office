"""
11:59 PM routine: start local web app, send email, keep app up until 12:10 AM.
"""

import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WINDOW_MINUTES = 11


def main():
    os.chdir(ROOT)
    python = sys.executable

    print("Starting web app on http://localhost:8000 ...")
    server = subprocess.Popen(
        [python, "-m", "web.app"],
        cwd=ROOT,
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0,
    )

    time.sleep(4)

    print("Sending nightly email...")
    subprocess.run([python, "main.py", "--email"], cwd=ROOT, check=False)

    print(f"App stays open for {WINDOW_MINUTES} minutes (until ~12:10 AM).")
    time.sleep(WINDOW_MINUTES * 60)

    print("Closing web app.")
    server.terminate()
    try:
        server.wait(timeout=15)
    except subprocess.TimeoutExpired:
        server.kill()

    print("Done.")


if __name__ == "__main__":
    main()
