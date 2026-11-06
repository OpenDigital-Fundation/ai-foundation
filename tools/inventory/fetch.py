"""Clone every source in catalog/sources.lock.yaml at its pinned commit into a scratch directory.

Usage: python -m tools.inventory.fetch <dest-dir>

Clones are data: nothing inside them is executed. The directory name of each clone is
<owner>_<repo>, matching what tools.inventory.build expects.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml


def fetch(lock: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for s in yaml.safe_load(lock.read_text())["sources"]:
        target = dest / s["id"].replace("/", "_")
        if (target / ".git").is_dir() and _head(target) == s["commit"]:
            print(f"ok      {s['id']}")
            continue
        target.mkdir(exist_ok=True)
        git = ["git", "-C", str(target)]
        subprocess.run(git + ["init", "-q"], check=True)
        subprocess.run(git + ["remote", "remove", "origin"], capture_output=True)
        subprocess.run(git + ["remote", "add", "origin", s["url"]], check=True)
        subprocess.run(git + ["fetch", "-q", "--depth", "1", "origin", s["commit"]], check=True)
        subprocess.run(git + ["-c", "advice.detachedHead=false", "checkout", "-q", "FETCH_HEAD"], check=True)
        print(f"fetched {s['id']} @ {s['commit'][:7]}")


def _head(repo: Path) -> str:
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()


if __name__ == "__main__":
    fetch(Path("catalog/sources.lock.yaml"), Path(sys.argv[1]))
