import yaml
import os

def load_config(config_path="phishing_detection/config.yaml"):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
