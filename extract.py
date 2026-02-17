"""
Main extraction script. Processes emails_input.json with Groq LLM and writes output.json.
Uses temperature=0 and retry with exponential backoff.
"""

import json
import os
import time
import re
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from prompts import build_system_prompt, build_user_prompt
from schemas import ExtractedShipment

load_dotenv()

INPUT_PATH = Path(__file__).parent / "emails_input.json"
PORT_REF_PATH = Path(__file__).parent / "port_codes_reference.json"
OUTPUT_PATH = Path(__file__).parent / "output.json"

MODEL = "llama-3.3-70b-versatile"
MAX_RETRIES = 3
INITIAL_BACKOFF = 2.0


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_port_reference_json() -> str:
    """Build a compact code -> name map string for the prompt."""
    data = load_json(PORT_REF_PATH)
    seen = set()
    lines = []
    for item in data:
        code = item["code"]
        if code not in seen:
            seen.add(code)
            lines.append(f"  {code} -> {item['name']}")
    return "\n".join(lines)


def extract_one(client: Groq, email: dict, system_prompt: str) -> ExtractedShipment:
    """Call Groq for one email; retry with exponential backoff."""

    email_id = email["id"]
    user_content = build_user_prompt(
        email_id=email_id,
        subject=email.get("subject", ""),
        body=email.get("body", ""),
    )

    backoff = INITIAL_BACKOFF

    for attempt in range(MAX_RETRIES):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                temperature=0,
                response_format={"type": "json_object"},  # FORCE VALID JSON
            )

            text = response.choices[0].message.content.strip()

            # Extract JSON safely
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if not match:
                raise ValueError("No JSON object found in response")

            json_text = match.group(0)
            raw = json.loads(json_text)

            # Ensure correct ID
            raw["id"] = email_id

            # Normalize numeric fields
            if raw.get("cargo_weight_kg") is not None:
                raw["cargo_weight_kg"] = round(float(raw["cargo_weight_kg"]), 2)

            if raw.get("cargo_cbm") is not None:
                raw["cargo_cbm"] = round(float(raw["cargo_cbm"]), 2)

            return ExtractedShipment.model_validate(raw)

        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {email_id}: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(backoff)
                backoff *= 2

    # If all retries fail → return null structure
    return ExtractedShipment(
        id=email_id,
        product_line=None,
        origin_port_code=None,
        origin_port_name=None,
        destination_port_code=None,
        destination_port_name=None,
        incoterm=None,
        cargo_weight_kg=None,
        cargo_cbm=None,
        is_dangerous=False,
    )


def main() -> None:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise SystemExit("Set GROQ_API_KEY in .env (see .env.example)")

    client = Groq(api_key=api_key)

    emails = load_json(INPUT_PATH)
    port_ref_str = get_port_reference_json()
    system_prompt = build_system_prompt(port_ref_str)

    results = []

    for i, email in enumerate(emails):
        print(f"Processing {email['id']} ({i + 1}/{len(emails)})...")
        extracted = extract_one(client, email, system_prompt)
        results.append(extracted.model_dump(mode="json"))

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
