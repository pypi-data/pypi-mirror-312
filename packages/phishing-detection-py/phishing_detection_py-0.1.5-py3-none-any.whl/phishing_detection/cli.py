import argparse
from phishing_detection.detector import PhishingDetector

def main():
    parser = argparse.ArgumentParser(description="Phishing Detection CLI")
    parser.add_argument(
        "type", choices=["url", "email"], help="Type of detection (url or email)"
    )
    parser.add_argument(
        "input", help="Input text to check (URL or email content)"
    )
    args = parser.parse_args()

    detector = PhishingDetector(args.type)
    result = detector.predict_proba(args.input)
    print("Detection Results:")
    print(result)

if __name__ == "__main__":
    main()
