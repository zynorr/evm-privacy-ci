# Contributing to EVM Privacy CI

Thank you for helping build privacy-boundary tooling that is useful without overstating what automation can prove.

## Before opening a pull request

1. Read the [threat model](docs/threat-model.md) and [policy specification](docs/policy-spec.md).
2. Keep findings deterministic and explainable; do not add AI-generated enforcement decisions.
3. Add a positive and negative fixture for every rule change.
4. Document unsupported constructs rather than silently treating them as safe.
5. Never add real private keys, production traces, wallet configuration, or customer code.

## Rule contribution standard

Every new rule needs:

- a stable rule ID;
- a security/privacy rationale;
- source and sink definition;
- expected severity and confidence;
- at least one true-positive and one safe/intentional-disclosure fixture;
- remediation guidance;
- known false positives and unsupported cases; and
- a test that fails if the rule regresses.

## Local checks

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m evm_privacy_ci validate-policy examples/basic/evm-privacy-ci.json
```

## Commit and pull-request guidance

- Use small, reviewable commits.
- Explain policy-schema changes in the pull request body.
- Include updated documentation in the same pull request as behavioral changes.
- Do not merge an exception without an owner, reason, and expiry.

## Code of conduct

Be respectful, constructive, and mindful that contributors may work on sensitive privacy systems. Harassment, doxxing, and the public disclosure of private reports are not acceptable.
