# Validation plan

**Status:** Proposed. This plan produces evidence; it does not assume demand exists.

## Questions to validate

1. Do privacy-forward EVM builders experience accidental public-boundary disclosures as a material risk?
2. Will they maintain a compact policy manifest in exchange for CI enforcement?
3. Are the proposed rules precise enough to stay enabled in normal development?
4. Is Vela/zkVerify-specific support valuable enough to justify maintenance?
5. Does the project provide a distinct capability beyond generic Solidity static analysis and circuit tools?

## Discovery cohort

Interview five teams building privacy-sensitive EVM apps. Prioritize active or prospective Horizen builders across private trading, payroll, settlement, identity/reputation, and games. Do not name a project as a partner unless it has expressly agreed.

### Interview script

1. Which user data, asset data, or strategy data must remain private?
2. What exactly is intentionally public, linkable, or selectively disclosed?
3. Where is that decision currently documented and reviewed?
4. Has a log, ABI, getter, public input, test helper, or inherited contract ever created a privacy concern?
5. Which supported surface would make a CI tool immediately useful?
6. What policy format would be maintainable by your team?
7. Would you run a local/open-source tool? Would you allow SARIF uploads to your repository?
8. What error rate, runtime, or onboarding burden would cause you to disable it?
9. Would you contribute a redacted/minimal fixture or a policy-design review?
10. Would you participate in a pilot? What would success look like?

## Evidence ladder

| Level | Evidence | Interpretation |
| --- | --- | --- |
| 0 | Internal thesis only | Not demand validation |
| 1 | Five completed interviews, notes anonymized | Problem evidence |
| 2 | Three explicit pilot commitments | Intent evidence |
| 3 | Two live CI integrations on non-demo repositories | Behavior evidence |
| 4 | A real issue/regression prevented or partner-contributed rule | Value evidence |
| 5 | Repeat adoption outside initial cohort | Early product-market evidence |

Grant application language must state the current level honestly.

## Product validation experiments

### Experiment A — Policy authoring

Give a builder the template and ask them to classify one privacy-critical flow. Measure time to first valid policy, number of clarification questions, selectors that fail to resolve, and whether the resulting policy reflects the team’s intended boundary.

**Pass condition:** first supported asset authored in under one hour with no tool-maintainer code change.

### Experiment B — Fixture review

Present VC001–VC006 examples without the expected finding. Ask the builder/auditor whether the issue is a real privacy risk for their threat model.

**Pass condition:** at least three of five teams classify at least one rule as relevant to their codebase.

### Experiment C — Pilot CI

Install the tool in observe-only mode. Triage every finding with the partner as true issue, intentional disclosure, false positive, or coverage gap.

**Pass condition:** the partner keeps the tool enabled, and actionable findings exceed false positives/coverage noise for the agreed supported scope.

### Experiment D — Vela/zkVerify value

Ask specific builders whether they need: Vela envelope checks, public-input maps, statement/receipt linkability review, or none. Implement adapters only where pilots validate demand.

## Quality evaluation

Do not claim an unqualified “accuracy” rate. Report by rule and corpus:

- known true positives detected;
- known safe cases not reported as violations;
- known false negatives;
- false positives from partner triage;
- unresolved/unsupported cases;
- runtime and peak memory;
- policy authoring time.

Each benchmark result must include tool version, compiler version, adapter version, policy version, fixture revision, and command line.

## Stop / pivot conditions

- Fewer than two pilot attempts after five qualified interviews.
- No team will maintain a policy manifest.
- The core value collapses to generic Slither wrapping.
- A maintained direct competitor already performs the same policy-to-EVM-boundary check.
- Supported rules are too noisy to stay enabled after two tuning cycles.
- Vela/zkVerify integration cannot be maintained against stable documented development interfaces.
