"""Minimal, dependency-free validation for veilcheck/v1 policy documents.

The parser deliberately accepts JSON only in the scaffold. YAML support belongs
behind a pinned dependency and a full schema test suite; docs use YAML because
it is the intended user-facing format.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


VALID_CLASSES = {"secret", "confidential", "linkable", "public"}
VALID_SURFACES = {
    "transaction_calldata",
    "event",
    "storage",
    "public_getter",
    "return_value",
    "external_call",
    "deployment_data",
    "zk_public_input",
    "commitment",
    "vela_encrypted_event",
    "zkverify_statement",
    "zkverify_receipt",
}


@dataclass(frozen=True)
class ValidationResult:
    errors: tuple[str, ...]

    @property
    def valid(self) -> bool:
        return not self.errors


def load_policy(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    if source.suffix.lower() not in {".json"}:
        raise ValueError(
            "The scaffold accepts JSON policy files only. YAML support is documented but not implemented yet; convert the example to JSON for CLI validation."
        )
    with source.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("A VeilCheck policy must be a JSON object.")
    return payload


def validate_policy(policy: dict[str, Any]) -> ValidationResult:
    errors: list[str] = []
    if policy.get("schema") != "veilcheck/v1":
        errors.append("schema must equal 'veilcheck/v1'.")

    assets = policy.get("assets")
    if not isinstance(assets, list) or not assets:
        errors.append("assets must be a non-empty list.")
        return ValidationResult(tuple(errors))

    seen_ids: set[str] = set()
    for index, asset in enumerate(assets):
        location = f"assets[{index}]"
        if not isinstance(asset, dict):
            errors.append(f"{location} must be an object.")
            continue
        asset_id = asset.get("id")
        if not isinstance(asset_id, str) or not asset_id:
            errors.append(f"{location}.id must be a non-empty string.")
        elif asset_id in seen_ids:
            errors.append(f"{location}.id duplicates '{asset_id}'.")
        else:
            seen_ids.add(asset_id)

        classification = asset.get("class")
        if classification not in VALID_CLASSES:
            errors.append(f"{location}.class must be one of {sorted(VALID_CLASSES)}.")

        selectors = asset.get("selectors")
        if not isinstance(selectors, list) or not selectors or not all(isinstance(item, str) and item for item in selectors):
            errors.append(f"{location}.selectors must be a non-empty list of strings.")

        for field in ("forbidden_surfaces",):
            surfaces = asset.get(field, [])
            if not isinstance(surfaces, list) or not all(surface in VALID_SURFACES for surface in surfaces):
                errors.append(f"{location}.{field} contains an unknown surface.")

        disclosures = asset.get("allowed_disclosures", [])
        if not isinstance(disclosures, list):
            errors.append(f"{location}.allowed_disclosures must be a list.")
        else:
            for disclosure_index, disclosure in enumerate(disclosures):
                if not isinstance(disclosure, dict) or disclosure.get("surface") not in VALID_SURFACES:
                    errors.append(f"{location}.allowed_disclosures[{disclosure_index}] must name a known surface.")

    return ValidationResult(tuple(errors))
