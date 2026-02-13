"""
Sanity check for the port mismatch fix script

This script verifies the following:
1. The destination for EMAIL_018 is INMAA / Chennai
2. The destination for EMAIL_028 is INBLR / Bangalore ICD
3. The destination name for EMAIL_050 is standardized to Chennai
4. No record contains the string India (Chennai)
"""

import json
from pathlib import Path
import sys

ground_truth_path = Path(__file__).parent / "ground_truth.json"

def test_port_fixes():
    with open(ground_truth_path, encoding="utf-8") as f:
        data = json.load(f)

    errors = 0

    for record in data:
        record_id = record.get("id")

        # Check EMAIL_018
        if record_id == "EMAIL_018":
            if record.get("destination_port_code") != "INMAA" or \
               record.get("destination_port_name") != "Chennai":
                print("EMAIL_018 has not been fixed correctly")
                errors += 1

        # Check EMAIL_028
        if record_id == "EMAIL_028":
            if record.get("destination_port_code") != "INBLR" or \
               record.get("destination_port_name") != "Bangalore ICD":
                print("EMAIL_028 has not been fixed correctly")
                errors += 1

        # Check EMAIL_050
