"""
Sanity check: Verify EMAIL_006 incoterm is FCA in ground_truth.json
"""
import json
from pathlib import Path

GROUND_TRUTH_PATH = Path(__file__).parent / "ground_truth.json"


def test_email_006_incoterm() -> bool:
    with open(GROUND_TRUTH_PATH, encoding="utf-8") as f:
        data = json.load(f)

    for record in data:
        if record.get("id") == "EMAIL_006":
            incoterm = record.get("incoterm")
            if incoterm == "FCA":
                print("PASS: EMAIL_006 incoterm is FCA (correct)")
                return True
            else:
                print(f"FAIL: EMAIL_006 incoterm is '{incoterm}', expected 'FCA'")
                return False

    print("FAIL: EMAIL_006 not found in ground truth")
    return False


if __name__ == "__main__":
    success = test_email_006_incoterm()
    exit(0 if success else 1)
