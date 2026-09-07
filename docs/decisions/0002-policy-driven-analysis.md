# ADR-0002: Require an explicit privacy policy

**Status:** Accepted
**Date:** 2026-09-07

## Context

Solidity types and variable names do not establish business privacy semantics. A `uint256` can be a public fee, a confidential amount, or a secret opening. Fully automatic classification would cause unsound passes and noisy heuristics.

## Decision

EVM Privacy CI requires a versioned policy document with:

- classified assets;
- selectors resolving to source entities;
- forbidden and allowed surfaces;
- proof public-input maps where applicable; and
- time-bounded exceptions.

## Consequences

- The onboarding cost is intentional and must be measured with design partners.
- Findings can cite an explicit policy decision instead of making opaque semantic guesses.
- Missing policy coverage becomes an actionable finding, not a pass.
