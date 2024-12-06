import unittest
from phishing_detection.detector import PhishingDetector

class TestPhishingDetector(unittest.TestCase):
    def setUp(self):
        self.url_detector = PhishingDetector(model_type="url")
        self.email_detector = PhishingDetector(model_type="email")

    def test_url_detection(self):
        sample_url = "http://phishing-site.com"
        result = self.url_detector.predict(sample_url)

        # Adjust for dictionary-based output
        self.assertIn("input", result)
        self.assertIn("prediction", result)
        self.assertIn("label", result["prediction"][0])
        self.assertIn("score", result["prediction"][0])

    def test_email_detection(self):
        sample_email = "Your account is locked. Click here to unlock it."
        result = self.email_detector.predict(sample_email)

        # Adjust for dictionary-based output
        self.assertIn("input", result)
        self.assertIn("prediction", result)
        self.assertIn("label", result["prediction"][0])
        self.assertIn("score", result["prediction"][0])
