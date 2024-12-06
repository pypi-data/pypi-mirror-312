import unittest
from phishing_detection_py.model_registry import ModelRegistry

class TestModelRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = ModelRegistry()

    def test_get_pipeline_url(self):
        pipeline = self.registry.get_pipeline("url")
        self.assertIsNotNone(pipeline)

    def test_get_pipeline_email(self):
        pipeline = self.registry.get_pipeline("email")
        self.assertIsNotNone(pipeline)

if __name__ == "__main__":
    unittest.main()
