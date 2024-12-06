import os

CONFIG = {
    "log_level": "INFO",
    "model_types": ["url", "email"],
    "huggingface_cache": os.getenv("HF_HOME", "~/.cache/huggingface"),
}
