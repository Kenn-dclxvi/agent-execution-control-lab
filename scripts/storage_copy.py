#!/usr/bin/env python3
"""Isolated directory materialization with an APFS copy-on-write fast path."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


COPY_MODE_ENV = "THE_CAPTION_EVAL_COPY_MODE"
COPY_MODES = {"auto", "clonefile", "copy"}


class StorageCopyError(Exception):
    pass


def requested_copy_mode() -> str:
    mode = os.environ.get(COPY_MODE_ENV, "auto")
    if mode not in COPY_MODES:
        raise StorageCopyError(
            f"{COPY_MODE_ENV} must be one of: {', '.join(sorted(COPY_MODES))}"
        )
    return mode


def _clonefile_copytree(source: Path, destination: Path) -> None:
    if sys.platform != "darwin":
        raise StorageCopyError("clonefile materialization is only available on macOS")
    completed = subprocess.run(
        ["/bin/cp", "-cRp", str(source), str(destination)],
        capture_output=True,
        check=False,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "cp -cR failed"
        raise StorageCopyError(detail)


def materialize_tree(source: Path | str, destination: Path | str) -> str:
    """Copy a tree without hardlinks and return ``clonefile`` or ``copy``.

    ``auto`` first asks macOS ``cp -cR`` for clonefile-backed copy-on-write
    files. Unsupported filesystems fall back to ``shutil.copytree``. The two
    directory trees remain independently mutable in either mode.
    """

    source_path = Path(source).resolve()
    destination_path = Path(destination).resolve()
    mode = requested_copy_mode()
    if not source_path.is_dir():
        raise StorageCopyError(f"copy source must be a directory: {source_path}")
    if destination_path.exists() or destination_path.is_symlink():
        raise StorageCopyError(f"copy destination already exists: {destination_path}")
    destination_path.parent.mkdir(parents=True, exist_ok=True)

    if mode in {"auto", "clonefile"}:
        try:
            _clonefile_copytree(source_path, destination_path)
            return "clonefile"
        except StorageCopyError:
            if destination_path.exists() or destination_path.is_symlink():
                if destination_path.is_dir() and not destination_path.is_symlink():
                    shutil.rmtree(destination_path)
                else:
                    destination_path.unlink()
            if mode == "clonefile":
                raise

    shutil.copytree(source_path, destination_path, symlinks=True)
    return "copy"
