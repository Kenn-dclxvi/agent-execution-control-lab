from __future__ import annotations

import os
import tempfile
import unittest
import sys
from pathlib import Path
from unittest import mock

from scripts import storage_copy


class StorageCopyTest(unittest.TestCase):
    @unittest.skipUnless(sys.platform == "darwin", "clonefile is a macOS facility")
    def test_clonefile_mode_preserves_file_modes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            destination = root / "destination"
            source.mkdir()
            protected = source / "protected.txt"
            protected.write_text("value\n", encoding="utf-8")
            protected.chmod(0o700)
            with mock.patch.dict(os.environ, {storage_copy.COPY_MODE_ENV: "clonefile"}):
                used = storage_copy.materialize_tree(source, destination)
            self.assertEqual(used, "clonefile")
            self.assertEqual((destination / "protected.txt").stat().st_mode & 0o777, 0o700)

    def test_copy_mode_preserves_symlinks_and_isolates_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            destination = root / "destination"
            source.mkdir()
            (source / "value.txt").write_text("source\n", encoding="utf-8")
            (source / "link.txt").symlink_to("value.txt")
            with mock.patch.dict(os.environ, {storage_copy.COPY_MODE_ENV: "copy"}):
                used = storage_copy.materialize_tree(source, destination)
            self.assertEqual(used, "copy")
            self.assertTrue((destination / "link.txt").is_symlink())
            (destination / "value.txt").write_text("changed\n", encoding="utf-8")
            self.assertEqual((source / "value.txt").read_text(), "source\n")

    def test_auto_falls_back_after_clonefile_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            destination = root / "destination"
            source.mkdir()
            (source / "value.txt").write_text("value\n", encoding="utf-8")
            with (
                mock.patch.dict(os.environ, {storage_copy.COPY_MODE_ENV: "auto"}),
                mock.patch.object(
                    storage_copy,
                    "_clonefile_copytree",
                    side_effect=storage_copy.StorageCopyError("unsupported"),
                ),
            ):
                used = storage_copy.materialize_tree(source, destination)
            self.assertEqual(used, "copy")
            self.assertEqual((destination / "value.txt").read_text(), "value\n")

    def test_invalid_mode_is_rejected(self) -> None:
        with mock.patch.dict(os.environ, {storage_copy.COPY_MODE_ENV: "hardlink"}):
            with self.assertRaises(storage_copy.StorageCopyError):
                storage_copy.requested_copy_mode()
