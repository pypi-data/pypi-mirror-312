import re

class Preprocessor:
    @staticmethod
    def clean_text(text):
        text = re.sub(r"http\S+", "", text)  # Remove URLs
        text = re.sub(r"\s+", " ", text)  # Remove extra whitespaces
        return text.strip()

    @staticmethod
    def extract_features(data):
        # Implement feature extraction logic if needed
        pass
