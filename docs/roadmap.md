# Roadmap

**Status:** Proposed. Dates are intentionally relative until grant terms and team availability are confirmed.

## Phase 0 — Repository and demand foundation

**Duration:** 1–2 weeks
**Exit criteria:**

- Complete project documentation, policy schema, rule catalogue, fixtures, and public contribution model.
- Formal name/brand clearance decision.
- Five discovery interviews scheduled or completed.
- Confirmed choice of initial supported Solidity framework and compiler matrix.
- Slither licensing/distribution decision reviewed by counsel or qualified maintainer.

## Phase 1 — Policy and static MVP

**Duration:** 3 weeks
**Scope:** VC001–VC004 for direct Solidity flows in a fixed compiler/framework matrix.

**Acceptance criteria:**

- YAML/JSON schema validation with source-located errors.
- Slither plugin resolves policy selectors and emits deterministic findings.
- VC001–VC004 have violation, safe, and gap fixtures.
- Terminal JSON output includes source, sink, rule, asset, confidence, and remediation.
- Unsupported code paths emit VC201 rather than a pass.

## Phase 2 — CI and disclosure controls

**Duration:** 2 weeks
**Scope:** VC005, VC006, exceptions, SARIF, GitHub Action.

**Acceptance criteria:**

- CI action runs locally and in a clean runner.
- SARIF results have stable rule IDs and source locations.
- Baseline/suppression behavior requires reason, owner, approver, issue, and expiry.
- Docker safe mode is documented and tested.

## Phase 3 — zkVerify public-input adapter

**Duration:** 2 weeks
**Scope:** one proof family validated by partners, proposed Groth16/Circom.

**Acceptance criteria:**

- VC101 and VC102 work against a pinned fixture artifact.
- Public-input count/order/name map drift fails as designed.
- Statement and receipt public/linkable surfaces appear in policy/report documentation.
- No claim is made that the adapter proves circuit soundness.

## Phase 4 — Vela local boundary probe

**Duration:** 2 weeks
**Scope:** local Docker sample and one partner-approved minimal integration.

**Acceptance criteria:**

- Test-only high-entropy sentinels do not appear raw in configured public traces when the safe fixture runs.
- A deliberately leaky public-envelope fixture is detected.
- WASM artifact hash policy drift is reported.
- Results clearly state use of the emulated local environment and lack of enclave assurance.

## Phase 5 — Pilot hardening and release candidate

**Duration:** 2–3 weeks
**Acceptance criteria:**

- Three design-partner evaluations; two active CI integrations.
- Published anonymized triage statistics and limitations.
- Independent rule-quality/security review complete.
- Release checklist passes.

## Explicitly deferred

- Universal proof-system support.
- Production Vela attestation validation.
- Full frontend/RPC/network privacy analysis.
- Autonomous remediation or AI enforcement.
- Hosted SaaS and telemetry.
- A commercial tier.
