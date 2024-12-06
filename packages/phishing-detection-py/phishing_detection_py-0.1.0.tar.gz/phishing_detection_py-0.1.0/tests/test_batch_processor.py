import unittest
from phishing_detection.batch_processor import BatchProcessor

class TestBatchProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = BatchProcessor("url")

    def test_process_batch(self):
        sample_data = ["http://phishing-site.com", "http://safe-site.com"]
        results = self.processor.process_batch(sample_data)
        self.assertEqual(len(results), len(sample_data))

if __name__ == "__main__":
    unittest.main()
