# Project charter

**Status:** Designed
**Project name:** EVM Privacy CI
**Category:** Horizen Builder Fund, Category 3 — New Projects / public good

## Mission

Make privacy promises in EVM applications testable before deployment.

EVM Privacy CI converts a developer-authored privacy policy into local, deterministic checks over public application surfaces. Its initial focus is Solidity applications that use or integrate with Horizen's Vela and zkVerify primitives.

## Problem statement

Privacy primitives protect a particular layer. A TEE can protect a computation; a ZK proof can hide a witness. Neither primitive prevents an application developer from later disclosing the same protected data in Solidity calldata, an event, storage, a getter, a public input, an aggregation receipt, or a frontend transaction builder.

The EVM has no `private data` storage modifier. Solidity documentation states that `private` and `internal` only restrict other contracts; the data remains visible to blockchain observers. Public state variables also have generated getters. [Solidity contracts documentation](https://docs.soliditylang.org/en/v0.8.35/contracts.html)

## Target users

1. **Protocol engineers** building a private trading, payroll, settlement, identity, reputation, or gaming application.
2. **Security engineers and auditors** who need a maintained map of disclosure decisions and a repeatable pre-audit control.
3. **ZK engineers** who need every public signal to have a declared purpose and classification.
4. **Vela builders** who need to inspect the public transaction and event envelope around confidential execution.

## Product promise

> Given a complete policy and a supported code path, EVM Privacy CI reports when an asset classified as protected reaches a policy-forbidden public surface.

The promise is deliberately narrower than “verify privacy.” A clean result does not prove that a system has no privacy flaw.

## Goals

- Local-first developer tooling: no code upload, account, cloud scan, or telemetry in v1.
- Explainable, deterministic findings with a source, sink, and policy reference.
- A tiny manifest maintained alongside code.
- Horizen-first adapters for Vela and zkVerify, without vendor lock-in in the core policy format.
- An open fixture corpus that allows rule quality to be independently measured.
- CI output suitable for terminal use, JSON processing, and GitHub code scanning.

## Non-goals

- Replacing human security or privacy review.
- A privacy score, compliance seal, or privacy certification.
- Automatically inferring business semantics such as “this `uint256` is a salary.”
- Automated proof-system or circuit-soundness verification.
- Hardware TEE attestation verification or enclave side-channel analysis.
- Mempool, network, IP, browser, gas, timing, or anonymity-set analysis in v1.
- An LLM-based audit bot.

## Ecosystem value

Vela is a TEE-based confidential execution layer: data is encrypted in memory and computation is attested. zkVerify is a public chain dedicated to proof verification. EVM Privacy CI sits at the integration boundary: it checks what must still be public for applications using those tools, and whether that public data matches the project's own policy. [Vela introduction](https://docs.horizen.io/vela/introduction/) [zkVerify overview](https://docs.zkverify.io/)

That makes the project a network capability rather than another end-user finance application: each privacy-forward builder can use the same policy language, fixtures, CI gate, and reporting format.

## Success measures

### Product measures

- A policy author can define their first supported asset in under one hour.
- Every shipped rule has a positive, safe, and unsupported fixture.
- Findings include a source/sink path and a policy-correct remediation.
- A policy change is required when a previously unclassified ZK public input is introduced.

### Adoption measures

- Five discovery interviews before the grant application is treated as demand-validated.
- Three design-partner evaluations during the build.
- Two active CI integrations by the final grant milestone.
- At least one partner-contributed fixture, limitation, or rule request.

### Safety measures

- No unclassified unsupported construct produces a “pass.”
- No source, policy, trace, key, or telemetry leaves the runner by default.
- Exceptions have an owner, a reason, and an expiry date.

## Naming and communications

Use the following formulation in grant and technical communications:

> “EVM Privacy CI is an open-source privacy-boundary CI project.”

Do not claim it is “the first privacy linter,” “a privacy audit,” or “a privacy guarantee.”
