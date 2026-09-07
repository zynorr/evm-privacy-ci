# Design-partner pilot guide

**Status:** Proposed pilot process. A team is not a partner until it has agreed in writing.

## Purpose

The pilot determines whether EVM Privacy CI solves a real engineering problem without requiring a team to expose production source, secrets, user data, or security-sensitive traces.

## Who is a good pilot partner

- Builds an EVM application with a meaningful privacy promise.
- Has a compilable Solidity repository and CI process.
- Can identify at least one confidential or linkable asset.
- Has an engineer and a security/product reviewer available for one-hour onboarding plus finding triage.
- Is willing to use a private/local tool run and share anonymized feedback.

## Pilot phases

### 1. Discovery — 30 minutes

Map the application's privacy promise and public surfaces. The partner answers the interview questions in [validation plan](validation-plan.md). No source sharing is required.

### 2. Policy workshop — up to 60 minutes

The partner authors one policy asset and its selectors. Start with a narrow high-value path: amount, recipient identity, nullifier, private strategy, or identity attribute.

Success is not a complete policy for the app. Success is a policy that accurately describes one supported flow and can be maintained by the partner.

### 3. Observe-only run

Run locally or in partner CI without failing merges. Triage each result:

- true privacy issue;
- intentional disclosed/linkable surface needing policy documentation;
- false positive;
- coverage gap;
- build/integration issue.

### 4. Enforcement decision

Only enable CI blocking for rule/scope combinations that the partner has reviewed. No partner is asked to make broad enforcement decisions on an unreleased analyzer.

### 5. Evidence and publication

Publish only aggregated counts and lessons by default. Names, logo, repository, screenshots, source locations, or detailed findings need written partner approval.

## Data handling

Never request or receive:

- private keys, wallet configuration, seed phrases, or P-521 private keys;
- production transaction payloads containing user data;
- unredacted confidential contracts without the partner’s security approval;
- private audit reports;
- API tokens or CI credentials.

Use sanitized fixtures whenever possible. For an on-repository local run, the partner runs the command themselves and shares only reviewed output.

## Pilot scorecard

| Measure | Record |
| --- | --- |
| Setup time | Minutes to first policy validation/run |
| Policy clarity | Partner score 1–5 and notes |
| Findings | True issue / intentional / false positive / gap counts |
| Runtime | Compile + analysis duration |
| Maintenance burden | Expected policy changes per typical feature |
| Adapter value | Solidity-only, zkVerify, Vela, or none |
| Retention | Observe-only, enforcement, or disabled; why |

## Exit criteria

The project can count a pilot as an evaluation only when the partner has completed discovery, authored/approved at least one policy asset, run the tool on a non-demo code path, and supplied feedback. A live integration additionally requires a maintained CI workflow.
