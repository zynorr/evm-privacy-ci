# ADR-0001: Neutral project naming and product scope

**Status:** Accepted
**Date:** 2026-09-07

## Context

The project needs a stable public identifier without implying trademark ownership, a privacy guarantee, or a distinct commercial product before there is evidence that such branding is needed.

The project also risked being described too broadly as a privacy scanner or audit platform.

## Decision

1. Use **EVM Privacy CI** as the repository and project name.
2. Describe the product as a **privacy-boundary CI gate**.
3. Position the product as policy-driven checks for existing Vela, zkVerify, and Solidity integrations.
4. Do not claim audit, certification, compliance, complete privacy verification, or product-name exclusivity.

## Consequences

- Repository documentation, the package, the CLI, and the policy namespace use the same neutral identifier.
- If a distinctive commercial brand, domain, or trademark becomes necessary, it requires a separate clearance decision.
- The product scope remains focused enough for a Category 3 public-good grant and can be evaluated by concrete fixtures and pilots.
