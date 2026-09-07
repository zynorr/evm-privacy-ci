# Implementation plan

**Status:** Proposed engineering plan. It assumes one experienced security/tooling engineer with access to Solidity/ZK reviewers; schedule changes with team composition.

## Repository evolution

```text
src/veilcheck/
  cli.py                 command parsing and exit behavior
  policy.py              parser, normalizer, schema migration
  rules.py               rule metadata only
  analysis/
    facts.py             source/sink/finding data model
    taint.py             supported flow propagation
    sinks.py             versioned EVM sink registry
    solidity.py          Slither adapter boundary
  adapters/
    vela.py              local public-envelope probe
    zkverify.py          signal/statement/receipt adapter
  reporting/
    terminal.py
    json.py
    sarif.py
  exceptions.py          baseline, expiry, approval validation
tests/
fixtures/
schemas/
```

## Work package 1 — Policy engine

### Tasks

- Add pinned YAML parsing and JSON Schema validation.
- Implement canonical normalized model and source-located diagnostic errors.
- Support documented classes, surfaces, disclosures, proof maps, defaults, and exceptions.
- Define migration behavior from `veilcheck/v1` to later schema versions.
- Add policy linter rules: duplicate IDs, missing selectors, unsafe raw-hash assumption, expired exception, unknown surface.

### Done when

- Valid YAML and JSON normalize to byte-stable canonical JSON.
- Invalid policy errors name path/line/field and remediation.
- Schema fixtures cover every required and rejected field.

## Work package 2 — Solidity facts and first rules

### Tasks

- Pin a supported Slither release and declare compiler/framework compatibility.
- Implement selector resolution to Slither entities.
- Build a minimal data-flow/fact layer over supported SlithIR operations.
- Implement VC001–VC004 with direct and supported interprocedural flows.
- Add generated-getter and inherited-event coverage.
- Emit VC201 for unsupported assembly, unresolved proxy, dynamic dispatch, missing artifact, and ambiguous selector.

### Done when

- Each rule passes positive/safe/gap fixtures in CI.
- Finding output contains meaningful source/sink symbols and source maps.
- No unmodelled construct yields a clean pass under clean-coverage policy.

## Work package 3 — Calls, deployment, and exceptions

### Tasks

- Implement VC005 over high-level and selected low-level calls/ABI encoding.
- Implement VC006 for constructor arguments, initializers, and immutables.
- Implement exception/baseline storage and expiry validator.
- Add SARIF and JSON report serializers.
- Make GitHub Action wrapper only after standalone CLI behavior is stable.

### Done when

- New error findings fail CI; expired exception fails CI.
- SARIF ingestion works in a sample public repository.
- Reports redact dynamic protected test values.

## Work package 4 — zkVerify adapter

### Tasks

- Pick one proof family based on partner evidence.
- Define metadata/artifact reader and artifact-lock baseline.
- Implement VC101/VC102 plus schema/context/VK drift checks.
- Model statement digest and receipt surfaces in reports.
- Add public-input fixture corpus and a manual-review checklist for circuit soundness.

### Done when

- An intentionally public amount fails policy while a declared root/nullifier fixture behaves as intended.
- Changed signal order/count fails without a matching policy update.
- Documentation plainly distinguishes application-boundary checks from circuit review.

## Work package 5 — Vela adapter

### Tasks

- Pin a documented Vela local Docker configuration and record its version.
- Build disposable test harness and test-only high-entropy sentinel generation.
- Capture and sanitize public transaction/receipt/log/storage evidence.
- Implement artifact identity and public-envelope checks.
- Add `deanonymize` policy-review control.

### Done when

- Safe fixture shows no raw sentinel in configured public surfaces.
- Intentionally leaky fixture generates a reproducible finding.
- Adapter reports the Vela local/emulated scope on every run.

## Work package 6 — hardening and adoption

### Tasks

- Conduct design-partner evaluations and triage findings.
- Tune only with corpus-backed changes; do not hide findings ad hoc.
- Obtain independent rule-quality and tool security review.
- Publish limitations, SBOM, signed release, and pilot report.

### Done when

- Two active CI pilots remain enabled.
- Release checklist passes.
- Project claims reflect recorded evidence.

## Technical decisions requiring review before coding

| Decision | Why it matters | Owner to identify |
| --- | --- | --- |
| Direct Slither plugin vs separate-process adapter | License and integration boundary | Maintainer + legal reviewer |
| YAML library | Parser security, supply chain, error quality | Tooling maintainer |
| First supported compiler/framework matrix | Determines reliable source maps | Solidity lead |
| First proof family | Determines artifact adapter scope | ZK lead + partner evidence |
| Vela harness API/version | Current product is in active development | Vela contact + maintainer |
| Final license | Required before public release | Copyright holder + counsel |
| Public name | Brand/trademark risk | Founder + counsel |
