"""
Script to fix the ground truth for EMAIL_006.
Client confirmed: incoterm should be FCA, not FOB.

This script:
1. Loads ground_truth.json
2. Updates EMAIL_006's incoterm from FOB to FCA
3. Saves the corrected data back to the file
"""

import json
from pathlib import Path

# Path to ground truth file (relative to script location)
GROUND_TRUTH_PATH = Path(__file__).parent / "ground_truth.json"


def fix_email_006_incoterm() -> bool:
    """
    Fix EMAIL_006 incoterm from FOB to FCA.
    Returns True if the fix was applied, False if EMAIL_006 was not found.
    """
    # Load ground truth
    with open(GROUND_TRUTH_PATH, encoding="utf-8") as f:
        data = json.load(f)

    # Find and update EMAIL_006
    updated = False
    for record in data:
        if record.get("id") == "EMAIL_006":
            old_incoterm = record.get("incoterm")
            record["incoterm"] = "FCA"
            updated = True
            print(f"✓ Fixed EMAIL_006: incoterm changed from '{old_incoterm}' to 'FCA'")
            break

    if not updated:
        print("✗ EMAIL_006 not found in ground truth")
        return False

    # Save updated ground truth
    with open(GROUND_TRUTH_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=None, ensure_ascii=False)

    print(f"✓ Ground truth saved to {GROUND_TRUTH_PATH}")
    return True


if __name__ == "__main__":
    fix_email_006_incoterm()
