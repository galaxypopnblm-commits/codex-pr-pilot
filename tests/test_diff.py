import json
import tempfile
import unittest
from pathlib import Path

from codex_pilot.diff import pull_request_number, read_diff_file


class DiffTests(unittest.TestCase):
    def test_read_diff_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.diff"
            path.write_text("diff --git a/a b/a\n", encoding="utf-8")

            self.assertIn("diff --git", read_diff_file(path))

    def test_pull_request_number_from_event(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "event.json"
            path.write_text(json.dumps({"pull_request": {"number": 42}}), encoding="utf-8")

            self.assertEqual(pull_request_number(str(path)), 42)


if __name__ == "__main__":
    unittest.main()
