from .detector import PhishingDetector

class BatchProcessor:
    def __init__(self, model_type="url"):
        self.detector = PhishingDetector(model_type)

    def process_batch(self, batch_data):
        results = []
        for item in batch_data:
            result = self.detector.predict_proba(item)
            results.append(result)
        return results
