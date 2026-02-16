"""Extraction prompts. Evolution: v1 (basic) → v2 (UN/LOCODE + rules) → v3 (full business rules)."""


def build_system_prompt(port_codes_json: str) -> str:
    """
    v3: Full business rules, port reference, conflict resolution, DG, units.
    v2: Added UN/LOCODE list and India/product_line rule.
    v1: Basic extraction only.
    """
    return f"""You extract structured shipment details from freight forwarding enquiry emails.

Output valid JSON only, with these exact keys: id, product_line, origin_port_code, origin_port_name, destination_port_code, destination_port_name, incoterm, cargo_weight_kg, cargo_cbm, is_dangerous.

RULES:
- Product line: If destination is India (port code starts with IN) → pl_sea_import_lcl. If origin is India → pl_sea_export_lcl.
- Port codes: Use ONLY 5-letter UN/LOCODE from this reference. Output the code and the matching canonical name from the reference. If no match, use null for both code and name.
- Valid incoterms (uppercase): FOB, CIF, CFR, EXW, DDP, DAP, FCA, CPT, CIP, DPU. If missing or ambiguous → FOB.
- Body overrides subject when they conflict. Extract only the FIRST shipment if multiple are mentioned.
- is_dangerous: true if email mentions DG, dangerous, hazardous, Class + number, IMO, IMDG. false if "non-DG", "non-hazardous", "not dangerous", or no mention.
- Weight: convert lbs to kg (×0.453592), tonnes to kg (×1000). Round to 2 decimals. TBD/N/A → null. Do not compute CBM from dimensions.
- Missing values → null (not 0 or "").

PORT CODES REFERENCE (code -> name):
{port_codes_json}
"""


def build_user_prompt(email_id: str, subject: str, body: str) -> str:
    """Build user message for one email."""
    return f"""Extract shipment details from this email. Reply with a single JSON object only, no markdown or explanation.

id: {email_id}
Subject: {subject}
Body: {body}"""
