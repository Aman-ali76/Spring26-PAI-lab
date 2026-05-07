"""
Step 1 — Clone Pakistani-law-mcp GitHub repo
Repo contains 1030 federal Pakistani statutes as JSON seed files
"""

import os
import sys
import subprocess

REPO_URL = "https://github.com/Ansvar-Systems/Pakistani-law-mcp.git"
REPO_DIR = "./Pakistani-law-mcp"


def clone_repo():
    print("\n[STEP 1] Cloning repo...")

    if os.path.exists(REPO_DIR):
        print(f"  ✅ Repo already exists at {REPO_DIR} — skipping clone")
        return

    result = subprocess.run(
        ["git", "clone", "--depth", "1", REPO_URL, REPO_DIR],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print(f"  ✅ Cloned → {REPO_DIR}")
    else:
        print(f"  ❌ Clone failed:\n{result.stderr}")
        print("  Fix: make sure git is installed → sudo apt install git")
        sys.exit(1)
