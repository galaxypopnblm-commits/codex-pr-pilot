import json
import unittest
from unittest import mock

from codex_pilot.github_client import create_issue_comment


class FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps({"html_url": "https://github.com/o/r/issues/1#comment"}).encode()


class GitHubClientTests(unittest.TestCase):
    @mock.patch("urllib.request.urlopen", return_value=FakeResponse())
    def test_create_issue_comment_returns_html_url(self, urlopen):
        url = create_issue_comment(
            repo="o/r",
            issue_number=1,
            body="hello",
            token="token",
        )

        self.assertEqual(url, "https://github.com/o/r/issues/1#comment")
        request = urlopen.call_args.args[0]
        self.assertEqual(request.get_method(), "POST")
        self.assertIn("/repos/o/r/issues/1/comments", request.full_url)


if __name__ == "__main__":
    unittest.main()
