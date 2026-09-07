# zkVerify adapter design

**Status:** Designed; not implemented.
**Scope:** Public-input intent, statement linkability, and EVM receipt-boundary policy.

## Why an adapter is needed

zkVerify is a public decentralized blockchain focused on zero-knowledge proof verification. Proof submission binds verifier context, verification key, verifier version, and hashed public-input bytes into a statement digest. [zkVerify overview](https://docs.zkverify.io/) [Proof submission flow](https://docs.zkverify.io/architecture/proof-submission-interface)

A proof can be valid while an application has disclosed more data than intended. VeilCheck therefore asks a separate question:

> Is each public input, derived statement, and EVM receipt surface explicitly classified by the application's privacy policy?

## Adapter objectives

- Require a name, purpose, and classification for every supported public-input position.
- Match policy-declared input order and count to available artifact/source metadata.
- Identify a policy-prohibited protected asset flowing to a public-input builder.
- Treat zkVerify statement digests as public and potentially linkable.
- Require policy treatment for EVM aggregation domain, ID, leaf, Merkle path, and receipt consumption.
- Report drift when context, verification-key identity, public-input schema, or proof-system configuration changes.

## Non-objectives

- Verify proof validity.
- Determine whether a circuit constrains each public input.
- Determine whether a proof system achieves zero knowledge.
- Verify a verification key cryptographically.
- Inspect every currently supported zkVerify proof family in v1.

The adapter starts with one well-documented artifact/source path, proposed as Groth16/Circom where usable partner projects exist. Other proof systems become adapters only after fixtures and design partners validate the demand. zkVerify supports Groth16, Noir variants, EZKL, Risc0, Plonky2, SP1, and TEE, among others; that diversity argues for a proof-neutral policy model and staged implementation. [zkVerify supported proofs](https://docs.zkverify.io/architecture/supported_proofs)

## Public data model

The zkVerify submission flow computes a leaf digest from verifier context, verification-key hash, verifier-version hash, and a hash of public-input bytes. The leaf/digest does not expose the raw inputs directly but can still be a durable correlator. [zkVerify statement digest](https://docs.zkverify.io/architecture/verification_pallets/abstract)

After verification/aggregation, the EVM-facing zkVerify contract stores public aggregation data and applications call `verifyProofAggregation` with domain ID, aggregation ID, leaf, Merkle path, leaf count, and index. [zkVerify EVM verification contract](https://docs.zkverify.io/architecture/proof-verification-smart-contract)

| Data | Policy treatment |
| --- | --- |
| Raw proof | Not classified as private by default; separate proof-system analysis required |
| Public input | Every position must be named, classified, and justified |
| Verifier context | Public configuration; detect drift |
| Verification-key identifier/hash | Public configuration; detect drift |
| Statement/leaf digest | `linkable` unless policy justifies public classification |
| Domain/aggregation ID | Public metadata; often linkable by timing/domain |
| Merkle path/index/leaf count | Public receipt metadata; policy-visible |

## Policy example

```yaml
proofs:
  - id: payroll-groth16
    adapter: zkverify
    system: groth16
    verifier_context: groth16
    verification_key:
      artifact: artifacts/payroll-vk.json
      expected_hash: "<expected hash>"
    public_inputs:
      - index: 0
        name: payroll_root
        class: public
        purpose: Current eligible-payroll tree root.
      - index: 1
        name: nullifier
        asset: payroll.nullifier
        class: linkable
        purpose: Prevent double claim.
      - index: 2
        name: net_amount
        asset: payroll.amount
        class: confidential
        allowed: false
```

## Checks

### VC101 — Unmapped public signal

If an adapter observes input index `n` but policy has no matching entry, report a coverage violation. This prevents silent policy drift.

### VC102 — Prohibited protected asset as public input

If a supported Solidity/circuit-builder flow assigns an asset whose policy forbids `zk_public_input` to a public input, report an error.

### VC-ZKV-003 — Schema and order drift

If public-signal count, names, order, types, verification-key identity, or context differs from the reviewed policy/artifact baseline, fail CI until the policy is reviewed.

### VC-ZKV-004 — Unclassified receipt surface

If application Solidity consumes a zkVerify aggregation receipt but policy does not declare intended linkability/public metadata, emit a review finding.

## Integration flow

```text
artifact + policy public-input map
        |
        v
verify index/count/order/name metadata
        |
        v
Slither-backed supported flow analysis of public-input construction
        |
        v
classify statement and receipt boundary
        |
        v
JSON/SARIF findings + policy-drift result
```

## Versioning policy

Proof artifacts and public-signal schemas are part of the privacy boundary. A pull request that changes either must modify the policy or carry a reviewed, time-bounded exception. Policy drift should be as visible as an ABI-breaking change.

## Open decisions

1. Which artifact formats are reliable enough to be the first adapter source of truth.
2. Whether a committed artifact lockfile or generated digest file is the best drift baseline.
3. How to represent proof-recursion and aggregate proofs without hiding nested public inputs.
4. Which zkVerify proof family has enough design-partner demand to implement after Groth16.
