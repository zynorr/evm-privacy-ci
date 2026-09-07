# Governance

**Status:** Pre-release placeholder.

## Maintainer model

Before the first public release, the project must identify named maintainers and publish their GitHub handles. Until then, no contributor should assume approval authority from this document.

## Protected areas

Changes to the following require at least two maintainer approvals and an updated fixture/test set:

- policy schema;
- sink registry;
- rule semantics, severity, or confidence;
- exception behavior;
- Vela/zkVerify adapters;
- CI, Docker, release, dependency, or security workflow;
- licensing and governance files.

## Decision records

Material technical decisions belong in `docs/decisions/` using an ADR. An ADR records context, decision, alternatives when useful, and consequences.

## Releases

Releases require the [release checklist](docs/release-checklist.md), signed/provenanced artifacts, a changelog, and a security review appropriate to change risk.
