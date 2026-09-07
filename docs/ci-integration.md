# CI integration

**Status:** Workflow scaffold available; privacy scanning is not implemented yet.

## Current repository CI

The repository's own CI validates the implemented policy-validator scaffold and runs unit tests in a clean Python environment. It does not claim to scan Solidity contracts.

## Intended consumer workflow

When the analyzer ships, a consumer repository will use a pinned EVM Privacy CI release:

```yaml
name: Privacy boundary

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read
  security-events: write

jobs:
  evm-privacy-ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<PINNED_SHA>

      - name: Run EVM Privacy CI
        uses: <future-org>/<future-action>@<PINNED_SHA>
        with:
          policy: evm-privacy-ci.yaml
          format: sarif
          output: reports/evm-privacy-ci.sarif
          safe-build: true

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@<PINNED_SHA>
        with:
          sarif_file: reports/evm-privacy-ci.sarif
          category: evm-privacy-ci
```

The placeholder action reference is deliberate. Do not copy it into a production workflow until a released action, immutable SHA, and signed provenance are published.

## Pull-request safety

- Do not pass deployment keys, wallet secrets, private RPC URLs, or production environment variables to the scan job.
- Do not run builds with write tokens on code from untrusted forks.
- Prefer a read-only checkout and containerized safe-build mode.
- Review SARIF visibility policy for private repositories; findings may identify privacy-sensitive source locations.
- Pin all third-party actions by commit SHA before production use.

## Baseline and exceptions

EVM Privacy CI will support a reviewed baseline only for gradual rollout. New `error` findings must fail pull requests. An exception requires a reason, owner, approver, linked issue, and expiry; expiry is enforced by VC201.

## SARIF rationale

SARIF allows third-party findings to appear in GitHub code scanning. [GitHub SARIF documentation](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/integrate-with-existing-tools/upload-sarif-file)

SARIF is an output convenience, not a privacy guarantee; users may choose terminal/JSON-only mode where uploading source-location metadata is undesirable.
