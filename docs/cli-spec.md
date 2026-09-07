# CLI and output specification

**Status:** `validate-policy` and `explain` are implemented in the scaffold. All analysis commands below are designed behavior until a release identifies them as implemented.

## Command design

```text
veilcheck validate-policy <policy.json>
veilcheck explain <RULE_ID>
veilcheck scan <target> --policy veilcheck.yaml --format terminal|json|sarif
veilcheck baseline create --policy veilcheck.yaml --output .veilcheck/baseline.json
veilcheck adapter vela run --policy veilcheck.yaml
veilcheck adapter zkverify validate --policy veilcheck.yaml --proof <proof-id>
```

## Current behavior

| Command | Behavior |
| --- | --- |
| `validate-policy <json>` | Validates the dependency-free JSON subset of `veilcheck/v1` |
| `explain <rule>` | Prints stable rule metadata |
| `scan` | Exits with status `3` and says that analysis is not implemented |

The current CLI should never be used as evidence of a Solidity scan.

## Intended scan options

| Option | Meaning |
| --- | --- |
| `--policy <path>` | Policy document; default `veilcheck.yaml` |
| `--format terminal,json,sarif,markdown` | One or more output serializers |
| `--output <path>` | Report path for non-terminal formats |
| `--fail-on error,warning` | Finding severities that produce a non-zero result |
| `--baseline <path>` | Reviewed baseline file |
| `--changed-since <git-ref>` | Restrict PR annotation/display, never rule coverage silently |
| `--safe-build` | Require containerized/network-isolated build mode |
| `--no-network` | Refuse adapters requiring an RPC/network call |
| `--adapter solidity,vela,zkverify` | Select adapters; unsupported adapter is an explicit error |
| `--debug` | Emit diagnostic details without sensitive literal values |

## Exit codes

| Code | Meaning |
| ---: | --- |
| 0 | No configured failing findings; not a privacy certification |
| 1 | Policy violation/finding met configured failure threshold |
| 2 | Invalid command, policy, or configuration |
| 3 | Requested capability is not implemented or unavailable |
| 4 | Analysis could not complete due to compilation/artifact/environment failure |
| 5 | Clean-coverage requirement failed due to unsupported or unresolved path |

## Terminal result contract

```text
ERROR VC003 event-disclosure [high]
Asset: payroll.amount (confidential)
Policy: veilcheck.yaml:12
Source: contracts/Payroll.sol:42 `pay(amount)`
Sink: contracts/Payroll.sol:47 `emit SalaryPaid(employee, amount)`
Path: pay.amount -> SalaryPaid.amount
Why: event payload is publicly readable from EVM logs.
Fix: emit an approved commitment or revise the privacy policy through review.
Docs: https://<future-repository>/blob/<version>/docs/rule-catalog.md#vc003--event-disclosure
```

Requirements:

- Never print raw dynamic sentinel values or a full secret literal.
- Always print rule ID, asset, classification, source, sink, confidence, and policy location.
- A `coverage-gap` result must visibly say that no safety conclusion was reached.

## JSON result contract

```json
{
  "tool": {"name": "veilcheck", "version": "0.1.0"},
  "policy": {"schema": "veilcheck/v1", "path": "veilcheck.yaml", "digest": "sha256:..."},
  "summary": {"errors": 1, "warnings": 0, "coverage_gaps": 0},
  "findings": [
    {
      "rule_id": "VC003",
      "severity": "error",
      "confidence": "high",
      "asset": {"id": "payroll.amount", "class": "confidential"},
      "source": {"uri": "contracts/Payroll.sol", "line": 42, "symbol": "Payroll.pay.amount"},
      "sink": {"uri": "contracts/Payroll.sol", "line": 47, "symbol": "SalaryPaid.amount", "surface": "event"},
      "path": ["Payroll.pay.amount", "SalaryPaid.amount"],
      "policy_location": {"uri": "veilcheck.yaml", "line": 12},
      "status": "new",
      "remediation": "Emit an approved commitment rather than raw amount."
    }
  ]
}
```

The exact JSON schema must be versioned before the first non-preview release. Clients must not parse terminal text.

## SARIF mapping

| VeilCheck field | SARIF field |
| --- | --- |
| Rule ID | `ruleId` |
| Rule documentation | `tool.driver.rules[].helpUri` |
| Severity | `level` |
| Source location | `locations[0].physicalLocation` |
| Taint path | `codeFlows` where supported |
| Asset and classification | `properties.veilcheck.asset` |
| Policy location | `relatedLocations` |
| Coverage gap | `level: warning` plus `properties.veilcheck.coverageGap: true` |

SARIF output must follow GitHub limits and avoid over-large reports; the tool should summarize repetitive paths rather than emitting a finding per equivalent callsite.

## Baseline policy

A baseline is a migration aid, not an approval ledger. It stores a finding fingerprint, review issue, owner, approver, rationale, and expiry. New findings never inherit an old baseline entry merely because they share a rule ID.
