import unittest
from phishing_detection.preprocessor import Preprocessor

class TestPreprocessor(unittest.TestCase):
    def test_clean_text(self):
        text = "Visit http://example.com for details."
        cleaned_text = Preprocessor.clean_text(text)
        self.assertNotIn("http://example.com", cleaned_text)

if __name__ == "__main__":
    unittest.main()
