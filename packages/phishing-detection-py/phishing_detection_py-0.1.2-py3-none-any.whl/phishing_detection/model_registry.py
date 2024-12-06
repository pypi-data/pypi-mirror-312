from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

class ModelRegistry:
    MODELS = {
        "url": "ealvaradob/bert-finetuned-phishing",
        "email": "cybersectony/phishing-email-detection-distilbert_v2.4.1",
    }

    def __init__(self):
        self.cache = {}

    def get_pipeline(self, model_type):
        if model_type not in self.MODELS:
            raise ValueError(f"Model type {model_type} not supported.")
        if model_type not in self.cache:
            model_name = self.MODELS[model_type]
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.cache[model_type] = pipeline("text-classification", model=model, tokenizer=tokenizer)
        return self.cache[model_type]
