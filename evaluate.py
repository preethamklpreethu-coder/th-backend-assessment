"""
Accuracy calculator: compares output.json to ground_truth.json.
String: case-insensitive, trimmed. Float: match after round to 2 decimals. Null: only equals null.
"""

import json
from pathlib import Path

FIELDS = [
    "product_line",
    "origin_port_code",
    "origin_port_name",
    "destination_port_code",
    "destination_port_name",
    "incoterm",
    "cargo_weight_kg",
    "cargo_cbm",
    "is_dangerous",
]

OUTPUT_PATH = Path(__file__).parent / "output.json"
GROUND_TRUTH_PATH = Path(__file__).parent / "ground_truth.json"


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def values_equal(expected, actual) -> bool:
    if expected is None and actual is None:
        return True
    if expected is None or actual is None:
        return False
    if isinstance(expected, bool) and isinstance(actual, bool):
        return expected == actual
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        return round(float(expected), 2) == round(float(actual), 2)
    if isinstance(expected, str) and isinstance(actual, str):
        return expected.strip().lower() == actual.strip().lower()
    return expected == actual


def main() -> None:
    if not OUTPUT_PATH.exists():
        print("Run extract.py first to generate output.json")
        return
    output = load_json(OUTPUT_PATH)
    truth = load_json(GROUND_TRUTH_PATH)
    by_id = {r["id"]: r for r in truth}
    correct_total = 0
    field_total = 0
    field_correct = {f: 0 for f in FIELDS}
    field_count = {f: 0 for f in FIELDS}
    for rec in output:
        eid = rec.get("id")
        if eid not in by_id:
            continue
        gt = by_id[eid]
        for f in FIELDS:
            field_count[f] += 1
            if values_equal(gt.get(f), rec.get(f)):
                field_correct[f] += 1
                correct_total += 1
            field_total += 1
    print("Accuracy by field:")
    for f in FIELDS:
        n = field_count[f]
        c = field_correct[f]
        pct = (100.0 * c / n) if n else 0
        print(f"  {f}: {c}/{n} ({pct:.1f}%)")
    overall = (100.0 * correct_total / field_total) if field_total else 0
    print(f"\nOverall accuracy: {correct_total}/{field_total} ({overall:.1f}%)")


if __name__ == "__main__":
    main()
