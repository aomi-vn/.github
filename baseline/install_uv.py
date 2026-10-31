from __future__ import annotations

import os
import platform
import shutil
import stat
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request
from pathlib import Path


def _arch() -> str:
    machine = platform.machine().lower()
    if machine in {"x86_64", "amd64"}:
        return "x86_64-unknown-linux-gnu"
    if machine in {"aarch64", "arm64"}:
        return "aarch64-unknown-linux-gnu"
    raise RuntimeError(f"unsupported machine: {machine}")


def _download_url(version: str, arch: str) -> str:
    return f"https://github.com/astral-sh/uv/releases/download/{version}/uv-{arch}.tar.gz"


def install_uv(version: str, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    arch = _arch()
    url = _download_url(version, arch)
    with tempfile.TemporaryDirectory() as tmp:
        archive = Path(tmp) / "uv.tar.gz"
        try:
            with urllib.request.urlopen(url, timeout=120) as response:
                archive.write_bytes(response.read())
        except urllib.error.URLError as exc:
            raise RuntimeError(f"uv download failed: {url}") from exc
        with tarfile.open(archive, "r:gz") as tar:
            tar.extractall(path=tmp, filter="data")
        candidates = list(Path(tmp).rglob("uv"))
        src = next((path for path in candidates if path.is_file() and path.name == "uv"), None)
        if src is None:
            raise RuntimeError("uv binary missing from release archive")
        target = dest_dir / "uv"
        shutil.copy2(src, target)
        target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return target


def main() -> int:
    version = os.environ.get("UV_VERSION", "0.13.6").strip()
    dest = Path(os.environ.get("RUNNER_TEMP", tempfile.gettempdir())) / "aomi-uv"
    binary = install_uv(version, dest)
    github_path = os.environ.get("GITHUB_PATH")
    if github_path:
        with open(github_path, "a", encoding="utf-8") as handle:
            handle.write(f"{binary.parent}\n")
    print(f"uv={binary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
