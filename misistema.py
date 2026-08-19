#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import platform
import shutil
import subprocess
from pathlib import Path

SCHEMA = "desarrollamo.misistema.v1"

TOOLS = {
    "python": [["python3", "--version"], ["python", "--version"]],
    "node": [["node", "--version"]],
    "npm": [["npm", "--version"]],
    "java": [["java", "-version"]],
    "git": [["git", "--version"]],
    "powershell": [["pwsh", "--version"], ["powershell", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"]],
    "docker": [["docker", "--version"]],
    "bash": [["bash", "--version"]],
    "zsh": [["zsh", "--version"]],
    "fish": [["fish", "--version"]],
}

PACKAGE_MANAGERS = ["pkg", "apt", "apt-get", "dnf", "yum", "pacman", "brew", "winget", "choco"]


def command_version(candidates: list[list[str]]) -> dict:
    for cmd in candidates:
        if shutil.which(cmd[0]) is None:
            continue
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=3, check=False)
            text = (p.stdout or p.stderr or "").strip().splitlines()
            version = text[0].strip() if text else None
            return {"available": True, "version": version}
        except Exception as exc:
            return {"available": True, "version": None, "error": exc.__class__.__name__}
    return {"available": False, "version": None}


def disk() -> dict:
    try:
        root = Path.home().anchor or "/"
        u = shutil.disk_usage(root)
        return {"root": root, "total_bytes": u.total, "free_bytes": u.free}
    except Exception:
        return {"root": None, "total_bytes": None, "free_bytes": None}


def build_report() -> dict:
    runtimes = {name: command_version(candidates) for name, candidates in TOOLS.items()}
    package_managers = {name: bool(shutil.which(name)) for name in PACKAGE_MANAGERS}
    shell = os.environ.get("SHELL")
    system = {
        "os": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "architecture": platform.machine(),
        "shell_name": Path(shell).name if shell else None,
        "disk": disk(),
    }
    capabilities = {
        "python_automation": runtimes["python"]["available"],
        "javascript_tooling": runtimes["node"]["available"],
        "java_runtime": runtimes["java"]["available"],
        "git_workflows": runtimes["git"]["available"],
        "container_runtime": runtimes["docker"]["available"],
        "shell_automation": any(runtimes[x]["available"] for x in ("bash", "powershell", "zsh", "fish")),
    }
    return {
        "schema": SCHEMA,
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "privacy": {
            "environment_values_collected": False,
            "secret_files_read": False,
            "credentials_collected": False,
        },
        "system": system,
        "runtimes": runtimes,
        "package_managers": package_managers,
        "capabilities": capabilities,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="MiSistema: inventario local de runtimes y capacidades")
    parser.add_argument("--output", help="guarda el JSON")
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    report = build_report()
    text = json.dumps(report, ensure_ascii=False, indent=None if args.compact else 2)
    print(text)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
