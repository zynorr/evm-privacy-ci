# Risk register

**Status:** Living document. Update at every milestone and before a public claim, grant report, or release.

| ID | Risk | Likelihood | Impact | Mitigation | Trigger / owner |
| --- | --- | --- | --- | --- | --- |
| R1 | A future distinctive brand creates name or trademark conflict | Low | Medium | Keep the current descriptive project name; complete clearance before adopting a distinct brand, domain, or trademark | Founder/legal; before branding change |
| R2 | No builder demand for a maintained policy manifest | Medium | High | Five interviews, three pilots, measure authoring time; stop/pivot if adoption is weak | Product owner; Phase 0/5 |
| R3 | Static analysis produces unacceptable noise | Medium | High | Narrow v1 rules, fixtures, observe-only pilots, explicit coverage gaps, no broad heuristics | Rule owner; every release |
| R4 | Static analysis creates false assurance | Medium | Critical | Strong threat model, clean-coverage behavior, no privacy score/certification language, independent review | Maintainers; docs/release |
| R5 | Slither license affects intended distribution/business model | High | Medium | Treat direct integration as AGPL-compatible; obtain legal review before final license/release | Founder/legal; Phase 0 |
| R6 | Vela interfaces are unstable or local-only | High | Medium | Keep Vela adapter optional/local, pin tested configuration, do not make MVP depend on production Vela | Adapter owner; Phase 4 |
| R7 | zkVerify proof-family diversity expands scope | High | Medium | Implement exactly one partner-validated proof family first; proof-neutral policy schema | ZK owner; Phase 3 |
| R8 | CI compilation runs untrusted repository code | Medium | Critical | Local-first safe-build container, no network/secrets, least privilege, documentation | Security owner; Phase 2 |
| R9 | Reports leak privacy-design data | Medium | High | No telemetry, local reports, SARIF opt-in, redact sentinels, partner consent | Security owner; all phases |
| R10 | A direct competitor emerges | Medium | Medium | Maintain survey; differentiate only where capabilities remain distinct; integrate or pivot when appropriate | Product owner; quarterly |
| R11 | Partner code/identities disclosed without permission | Low | High | Anonymized reporting default; written consent for names, repos, or findings | Partner lead; all pilots |
| R12 | Grant reviewers reject unproven demand | Medium | High | Apply only with current evidence ladder level stated and pilot plan/milestones concrete | Founder; application |

## Escalation rules

- Any `Critical` risk blocks a public release until mitigated or explicitly accepted in a maintainer ADR.
- A new risk affecting user funds, confidential data, licensing, or name rights requires an issue plus ADR or security advisory.
- Grant materials must reflect unresolved risks rather than presenting them as solved.
