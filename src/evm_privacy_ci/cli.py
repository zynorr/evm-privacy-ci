from __future__ import annotations

import argparse
from pathlib import Path

from evm_privacy_ci import __version__
from evm_privacy_ci.policy import load_policy, validate_policy
from evm_privacy_ci.rules import RULES


def _validate_policy(path: str) -> int:
    try:
        result = validate_policy(load_policy(path))
    except (OSError, ValueError) as error:
        print(f"Policy validation failed: {error}")
        return 2
    if result.valid:
        print(f"Policy is valid: {Path(path)}")
        return 0
    print(f"Policy is invalid: {Path(path)}")
    for error in result.errors:
        print(f"- {error}")
    return 1


def _explain_rule(identifier: str) -> int:
    rule = RULES.get(identifier.upper())
    if rule is None:
        print(f"Unknown rule: {identifier}")
        return 2
    print(f"{rule.identifier}: {rule.title}")
    print(f"Default severity: {rule.default_severity}")
    print(rule.summary)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="evm-privacy-ci", description="Proposal-stage privacy-boundary tooling.")
    parser.add_argument("--version", action="version", version=f"evm-privacy-ci {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate-policy", help="Validate a scaffold JSON policy.")
    validate.add_argument("path")

    explain = subparsers.add_parser("explain", help="Explain an EVM Privacy CI rule ID.")
    explain.add_argument("rule_id")

    subparsers.add_parser("scan", help="Reserved for the future analyzer; not implemented.")
    args = parser.parse_args(argv)

    if args.command == "validate-policy":
        return _validate_policy(args.path)
    if args.command == "explain":
        return _explain_rule(args.rule_id)
    print("scan is not implemented in this proposal-stage scaffold. See docs/roadmap.md.")
    return 3
