import unittest

from codex_pilot.review import render_dry_run_review, trim_diff


class ReviewTests(unittest.TestCase):
    def test_trim_diff_marks_truncated_content(self):
        diff, truncated = trim_diff("abcdef", 3)

        self.assertTrue(truncated)
        self.assertIn("abc", diff)
        self.assertIn("truncated", diff)

    def test_dry_run_lists_changed_files(self):
        review = render_dry_run_review("diff --git a/app.py b/app.py\n")

        self.assertIn("`app.py`", review)
        self.assertIn("Dry-run mode", review)


if __name__ == "__main__":
    unittest.main()
