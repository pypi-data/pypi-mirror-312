import unittest
from phishing_detection_py.utils import load_config
from unittest.mock import mock_open, patch

class TestUtils(unittest.TestCase):
    def test_load_config(self):
        mock_yaml = """
        models:
          url: "ealvaradob/bert-finetuned-phishing"
          email: "cybersectony/phishing-email-detection-distilbert_v2.4.1"
        """
        with patch("builtins.open", mock_open(read_data=mock_yaml)):
            config = load_config("phishing_detection_py/config.yaml")
            self.assertIn("models", config)
            self.assertIn("url", config["models"])
            self.assertIn("email", config["models"])
