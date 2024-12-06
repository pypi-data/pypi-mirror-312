from transformers import pipeline
from .model_registry import ModelRegistry

class PhishingDetector:
    """
    A class for detecting phishing URLs or emails using pre-trained models from Hugging Face.
    """

    # Label mapping for clearer interpretation
    LABEL_MAPPING = {
        "LABEL_0": "benign",
        "LABEL_1": "phishing"
    }

    def __init__(self, model_type="url"):
        """
        Initialize the PhishingDetector with a specified model type.
        
        :param model_type: Type of input to analyze. Options are "url" or "email".
        """
        self.model_registry = ModelRegistry()
        self.model_type = model_type
        self.model_pipeline = self.model_registry.get_pipeline(model_type)

    def predict(self, input_data):
        """
        Perform a phishing prediction on a single input (URL or email content).
        
        :param input_data: A string containing the URL or email text to classify.
        :return: A structured dictionary with input and predictions mapped to human-readable labels.
        """
        raw_predictions = self.model_pipeline(input_data)
        formatted_predictions = self._format_predictions(raw_predictions)
        return {
            "input": input_data,
            "prediction": formatted_predictions
        }

    def predict_proba(self, input_data):
        """
        Retrieve phishing probabilities for the input, along with mapped predictions.
        
        :param input_data: A string containing the URL or email text to classify.
        :return: A structured dictionary with input, probabilities, and predictions.
        """
        raw_predictions = self.model_pipeline(input_data)
        formatted_predictions = self._format_predictions(raw_predictions)
        return {
            "input": input_data,
            "prediction": formatted_predictions
        }

    def _format_predictions(self, raw_predictions):
        """
        Helper method to format raw model predictions into human-readable labels and probabilities.
        
        :param raw_predictions: The raw output from the model pipeline.
        :return: A list of formatted prediction dictionaries.
        """
        return [
            {
                "label": self.LABEL_MAPPING.get(pred["label"], pred["label"]),
                "score": round(pred["score"], 6)  # Limiting float precision for readability
            }
            for pred in raw_predictions
        ]
