# ADR-0003: Local-first deterministic enforcement

**Status:** Accepted
**Date:** 2026-09-07

## Context

The project analyzes sensitive source code and privacy design. Hosted scanning and generative AI recommendations could expand the exposure surface and make enforcement non-reproducible.

## Decision

The v1 enforcement path is deterministic, local-first, and has no telemetry or source upload. AI may eventually help generate non-authoritative explanations in an opt-in developer workflow, but it cannot decide whether CI passes or fails.

## Consequences

- The project needs strong local report formats and documentation.
- Cloud analytics, remote model calls, and automated patches are deferred.
- Every enforcement result is reproducible from repository state, policy, tool version, and compiler configuration.
