# Release checklist

No version may be presented as production-ready until every applicable item is complete.

## Identity and governance

- [ ] Product name and trademark/domain conflict reviewed.
- [ ] Copyright holder identified.
- [ ] Final SPDX license text added.
- [ ] Maintainer, security contact, CODEOWNERS, and governance model published.
- [ ] No draft placeholder URLs or contacts remain in public files.

## Technical quality

- [ ] Clean-environment CI executes unit, integration, schema, lint, and fixture tests.
- [ ] Supported compiler/framework versions are stated and tested.
- [ ] All rules have true-positive, safe, and coverage-gap fixtures.
- [ ] Rule IDs, severities, confidence, and remediation are documented.
- [ ] JSON and SARIF schemas are tested for compatibility.
- [ ] Unsupported paths produce coverage results, never silent passes.
- [ ] Release artifact is reproducible or provenance is documented.

## Security and privacy

- [ ] Dependency lockfiles and SBOM published.
- [ ] Container/image digest pinned and scanned.
- [ ] No network/telemetry behavior occurs without explicit opt-in.
- [ ] Safe-build mode runs without repository secrets.
- [ ] Reports redact dynamic sentinel literals.
- [ ] Security reporting channel tested.
- [ ] Independent review completed for core rule engine and CI action.

## Documentation and claims

- [ ] README distinguishes implemented, designed, and proposed capabilities.
- [ ] Threat model and limitations are linked from README and CLI output.
- [ ] Vela docs state local/emulated-environment limits.
- [ ] zkVerify docs state public-input checks do not prove circuit security.
- [ ] No “audit,” “certification,” “guarantee,” “compliance,” or “first” claims appear without support.

## Adoption evidence

- [ ] Pilot cohort and results documented truthfully.
- [ ] Partner naming approved in writing.
- [ ] Partner feedback incorporated or rejected with public rationale.
- [ ] Support and issue-triage policy published.
