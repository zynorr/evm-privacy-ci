# Horizen Builder Fund — Category 3 project brief

**Project name:** EVM Privacy CI
**Category:** New Projects / public good
**Status:** Proposal-stage; validate pilots before representing demand as proven.

## One sentence

EVM Privacy CI is an open-source CI gate that checks whether Vela, zkVerify, and Solidity applications leak policy-protected data through public EVM and proof-verification boundaries.

## Ecosystem need

Horizen supports privacy as an application-layer feature through Vela confidential execution and zkVerify proof verification. Builders still need to decide and maintain what becomes public around those primitives: transaction data, logs, state roots, getters, public proof inputs, statements, and receipts.

Vela’s local walkthrough illustrates this boundary: the private account ledger runs in the TEE, while an app upload/deployment request, public identifiers, user key registration, and onchain deposits exist around it. [Vela walkthrough](https://docs.horizen.io/vela/getting-started/hello-world/) zkVerify’s proof flow also binds public-input bytes into a public statement digest and lets applications verify public aggregation receipts on EVM chains. [zkVerify proof flow](https://docs.zkverify.io/architecture/proof-submission-interface)

EVM Privacy CI creates a reusable engineering control so each builder does not need to manually rediscover the same boundary mistakes.

## Deliverable

1. Open-source policy specification and schema.
2. Solidity rules for protected data in calldata, logs, storage, getters, returns, external calls, and deployment state.
3. One zkVerify public-input adapter with schema-drift checks.
4. One Vela local-development boundary probe using test-only sentinels.
5. CLI, JSON/SARIF output, GitHub Action, fixture corpus, and documentation.
6. Three design-partner evaluations and two active CI pilots.

## What it is not

It is not a smart-contract audit, privacy certification, compliance product, generic AI scanner, proof-system verifier, or a claim that all privacy risks can be automated.

## Why Category 3

The Builder Fund names smaller public goods and focused security support as Category 3 candidates, while asking applicants to demonstrate genuine demand and early technical capability. EVM Privacy CI is designed as a small shared security capability with measurable pilots—not a broad research agenda. [Horizen Builder Fund](https://horizen.io/builder-fund/)

## Milestones

| Milestone | Evidence |
| --- | --- |
| M1: Prove the hard part | Six supported Solidity disclosure fixtures plus one zkVerify public-input fixture and one Vela local-boundary fixture |
| M2: Ship developer tooling | Versioned CLI, Docker safe mode, SARIF, GitHub Action, independent rule-quality review |
| M3: Show demand | Three design-partner evaluations and two live CI integrations, with anonymized triage outcomes |

## Demand honesty

The repository must not state that projects are users or partners until they have consented. The validation plan targets five interviews, three evaluations, and two active CI integrations; those are targets, not completed facts. See [validation plan](validation-plan.md).
