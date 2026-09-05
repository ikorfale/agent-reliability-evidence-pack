#!/usr/bin/env python3
"""Durably replace one local state file without exposing partial content."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import stat
import sys
import tempfile
from typing import BinaryIO, Callable

Hook = Callable[[str], None]
MAX_STDIN_BYTES = 64 * 1024 * 1024
COPY_CHUNK_BYTES = 1024 * 1024


def _replacement_mode(path: Path, default: int) -> int:
    """Return the existing regular file's mode without following symlinks."""
    try:
        existing = path.lstat()
    except FileNotFoundError:
        return default
    if not stat.S_ISREG(existing.st_mode):
        raise ValueError("destination must be absent or a regular file")
    return stat.S_IMODE(existing.st_mode)


def durable_replace(path: Path, payload: bytes, *, mode: int = 0o600,
                    hook: Hook | None = None) -> None:
    """Write, fsync, rename, and fsync the containing directory.

    The destination and temporary file must share a directory/filesystem.
    `hook` exists solely for deterministic fault-injection tests.
    """
    path = Path(path)
    if not path.name or path.name in {".", ".."}:
        raise ValueError("path must name a file")
    path.parent.mkdir(parents=False, exist_ok=True)
    chosen_mode = _replacement_mode(path, mode)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp",
                                     dir=path.parent)
    replaced = False
    try:
        os.fchmod(fd, chosen_mode)
        with os.fdopen(fd, "wb", closefd=True) as stream:
            stream.write(payload)
            stream.flush()
            if hook:
                hook("after-write")
            os.fsync(stream.fileno())
            if hook:
                hook("after-file-fsync")
        os.replace(temporary, path)
        replaced = True
        if hook:
            hook("after-replace")
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        directory_fd = os.open(path.parent, flags)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
        if hook:
            hook("after-directory-fsync")
    finally:
        if not replaced:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass


def durable_replace_stream(path: Path, source: BinaryIO, *,
                           limit: int = MAX_STDIN_BYTES, mode: int = 0o600,
                           hook: Hook | None = None) -> None:
    """Replace *path* from a binary stream while bounding input memory use.

    One byte beyond *limit* is consumed to detect oversized input. The
    destination is not replaced when the limit is exceeded.
    """
    if limit < 0:
        raise ValueError("limit must be non-negative")
    path = Path(path)
    if not path.name or path.name in {".", ".."}:
        raise ValueError("path must name a file")
    path.parent.mkdir(parents=False, exist_ok=True)
    chosen_mode = _replacement_mode(path, mode)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp",
                                     dir=path.parent)
    replaced = False
    try:
        os.fchmod(fd, chosen_mode)
        total = 0
        with os.fdopen(fd, "wb", closefd=True) as stream:
            while True:
                chunk = source.read(min(COPY_CHUNK_BYTES, limit - total + 1))
                if not chunk:
                    break
                total += len(chunk)
                if total > limit:
                    raise ValueError(f"input exceeds {limit} byte limit")
                stream.write(chunk)
            stream.flush()
            if hook:
                hook("after-write")
            os.fsync(stream.fileno())
            if hook:
                hook("after-file-fsync")
        os.replace(temporary, path)
        replaced = True
        if hook:
            hook("after-replace")
        flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
        directory_fd = os.open(path.parent, flags)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
        if hook:
            hook("after-directory-fsync")
    finally:
        if not replaced:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--mode", type=lambda value: int(value, 8), default=0o600)
    args = parser.parse_args()
    try:
        durable_replace_stream(args.path, sys.stdin.buffer, mode=args.mode)
    except ValueError as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
