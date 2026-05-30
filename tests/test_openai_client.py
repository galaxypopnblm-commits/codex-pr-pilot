import unittest

from codex_pilot.openai_client import extract_output_text


class OpenAIClientTests(unittest.TestCase):
    def test_extracts_output_text_shortcut(self):
        self.assertEqual(extract_output_text({"output_text": "hello"}), "hello")

    def test_extracts_nested_output_text(self):
        data = {
            "output": [
                {
                    "content": [
                        {"type": "output_text", "text": "hello"},
                        {"type": "output_text", "text": "world"},
                    ]
                }
            ]
        }

        self.assertEqual(extract_output_text(data), "hello\nworld")


if __name__ == "__main__":
    unittest.main()
