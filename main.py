"""Friday 20 November 2026: copy the finished broadsheet to the output dir.

The broadsheet is poster.html rendered to entry.png with headless Chrome
at 1024x1024. This program only copies that image, then proves the copy
is byte-identical by comparing sha256 digests.
"""
import hashlib
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "entry.png"
TARGET_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
TARGET = TARGET_DIR / "entry.png"


def _digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def publish_verified_copy(source, target_dir):
    """Copy source into target_dir, then prove the copy matches by digest."""
    target = target_dir / source.name
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)

    src = _digest(source)
    dst = _digest(target)
    if src != dst:
        raise SystemExit(f"copy mismatch: {src} != {dst}")
    return src, target


def main():
    digest, target = publish_verified_copy(SOURCE, TARGET_DIR)
    print(f"copied entry.png {digest[:12]} -> {target} (44 stories, Friday 20 November 2026)")


if __name__ == "__main__":
    main()
