"""
Script to fix known port mismatches and naming inconsistencies
in ground_truth.json.

Fixes applied:
1. EMAIL_018 → Correct destination_port_code (KRPUS → INMAA)
2. EMAIL_028 → Correct destination_port_code (INMAA → INBLR)
3. EMAIL_050 → Standardize destination_port_name to "Chennai"
4. Standardize "India (Chennai)" → "Chennai" globally
"""

import json
from pathlib import Path

# Path to ground truth file (relative to script location)
GROUND_TRUTH_PATH = Path(__file__).parent / "ground_truth.json"


def fix_port_mismatches() -> bool:
    """
    Apply known fixes to port mismatches and naming issues.
    Returns True if any updates were made.
    """
    with open(GROUND_TRUTH_PATH, encoding="utf-8") as f:
        data = json.load(f)

    updated = False

    for record in data:

        # --- Fix EMAIL_018 ---
        if record.get("id") == "EMAIL_018":
            if record.get("destination_port_code") == "KRPUS":
                record["destination_port_code"] = "INMAA"
                record["destination_port_name"] = "Chennai"
                print("✓ Fixed EMAIL_018: destination corrected to INMAA / Chennai")
                updated = True

        # --- Fix EMAIL_028 ---
        if record.get("id") == "EMAIL_028":
            if record.get("destination_port_code") == "INMAA":
                record["destination_port_code"] = "INBLR"
                record["destination_port_name"] = "Bangalore ICD"
                print("✓ Fixed EMAIL_028: destination corrected to INBLR / Bangalore ICD")
                updated = True

        # --- Fix EMAIL_050 ---
        if record.get("id") == "EMAIL_050":
            if record.get("destination_port_name") == "India (Chennai)":
                record["destination_port_name"] = "Chennai"
                print("✓ Fixed EMAIL_050: standardized name to 'Chennai'")
                updated = True

        # --- Global Standardization ---
        if record.get("destination_port_name") == "India (Chennai)":
            record["destination_port_name"] = "Chennai"
            updated = True

    if not updated:
        print("No fixes were required.")
        return False

    with open(GROUND_TRUTH_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=None, ensure_ascii=False)

    print(f"✓ Ground truth saved to {GROUND_TRUTH_PATH}")
    return True


if __name__ == "__main__":
    fix_port_mismatches()
