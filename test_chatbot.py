import unittest

from chatbot import get_response


class ChatbotRulesTest(unittest.TestCase):
    def test_greeting_rule(self):
        self.assertIn("Hello", get_response("hello"))

    def test_exit_rule(self):
        self.assertIn("Goodbye", get_response("quit"))

    def test_ai_rule(self):
        self.assertIn("Artificial intelligence", get_response("What is AI?"))

    def test_unknown_input_uses_fallback(self):
        self.assertIn("still learning", get_response("Tell me about satellites"))


if __name__ == "__main__":
    unittest.main()
