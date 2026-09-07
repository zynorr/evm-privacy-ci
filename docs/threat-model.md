# Threat model

**Status:** Designed
**Applies to:** `evm-privacy-ci/v1`, v1 rule pack, Vela and zkVerify adapters

## Security statement

EVM Privacy CI detects specified, supported paths from a **policy-labelled asset** to a **policy-forbidden observable surface**. It does not establish a global confidentiality proof.

A passing result means only:

> The configured rule set found no policy violation in the compiled, supported scope, and all known coverage gaps were reported.

## Assets

| Class | Meaning | Typical examples |
| --- | --- | --- |
| `secret` | Must never be published or included in an onchain transaction | private key, note preimage, encryption secret, unblinded witness |
| `confidential` | May appear only in a policy-approved cryptographic form or authorized private environment | amount, salary, bid, identity attribute, private strategy |
| `linkable` | Is public by design but can correlate actions or identities; every disclosure needs an explicit reason | nullifier, commitment, view tag, account identifier, statement digest |
| `public` | Intentionally public | Merkle root, protocol version, public fee |

The classes express an application claim, not an intrinsic property of a Solidity type. `bytes32`, `uint256`, and `address` may belong to any class depending on context.

## Public surfaces

| Surface | What an observer can see | v1 treatment |
| --- | --- | --- |
| `transaction_calldata` | Top-level external transaction input and publicly reachable ABI data | Detect for supported Solidity flow paths |
| `event` | Event topics and data | Detect; all event payload is public and indexed values are easily queryable |
| `storage` | Raw EVM storage slots and construction state | Detect direct supported writes; `private` is not encryption |
| `public_getter` | Compiler-generated getter or external/public view API | Detect where ABI/source map is available |
| `return_value` | Result returned by public/external call or `eth_call` | Detect direct supported returns |
| `external_call` | Calldata, value, and error behavior sent to another contract | Detect direct supported call paths |
| `deployment_data` | Constructor arguments, immutable initialization, creation transaction data | Detect supported deployment paths |
| `zk_public_input` | Public values associated with a proof statement | Require mapping; block prohibited use |
| `zkverify_statement` | Public digest that commits to verifier context, VK, version, and public-input bytes | Treat as linkability surface |
| `zkverify_receipt` | Public EVM aggregation domain/id/leaf/path/receipt data | Require explicit classification where relevant |
| `vela_encrypted_event` | Ciphertext returned from Vela | Require declaration; do not treat as proof of safe encryption |

## Adversaries

### Passive public observer

Reads blocks, mempool data where available, receipts, logs, ABI metadata, verified source, storage, and proof receipts. This is the primary v1 adversary.

### Indexer or chain-analytics service

Builds searchable profiles from logs, addresses, proof statements, commitments, nullifiers, deposits, withdrawals, and timing. v1 identifies explicit declared linkability surfaces but does not model graph analysis quality.

### External-contract recipient

Receives data through an EVM call. v1 detects direct prohibited data flow into supported call sites, but cannot decide whether the recipient is trusted without policy information.

### Malicious or mistaken developer

Adds a seemingly harmless event, public getter, debug return, circuit signal, or inherited function that reveals protected data. CI is designed to make this change reviewable.

## Threats addressed

| Threat | Example | Control |
| --- | --- | --- |
| Raw onchain persistence | `uint256 private salary;` | VC001 |
| ABI disclosure | `function pay(uint256 salary) external` | VC002 |
| Log disclosure | `emit Payment(employee, salary)` | VC003 |
| Read API disclosure | `getSalary()` or a public mapping | VC004 |
| Cross-contract disclosure | `oracle.submit(amount)` | VC005 |
| Deployment disclosure | constructor receives a secret commitment opening | VC006 |
| Unreviewed ZK disclosure | `publicInputs[3] = amount` | VC101/VC102 |
| False assurance | inline assembly, proxy implementation, unsupported compiler path | VC201 coverage gap |

## Threats explicitly not addressed

- Whether a ZK circuit constrains an input correctly, is zero knowledge, or is sound.
- Whether a hash, encryption function, commitment, or key-management design is cryptographically secure.
- Private-read leakage to RPC providers, IP addresses, device fingerprints, analytics, frontend telemetry, or network routing.
- Timing, gas, volume, access-pattern, side-channel, or anonymity-set correlation.
- TEE implementation, hardware root of trust, remote-attestation validation, or side channels.
- Unverified bytecode, arbitrary inline assembly, dynamic delegatecall, and code generated after the supported build unless explicitly covered by a later adapter.

Ethereum’s privacy roadmap describes private reads, private writes, and private proving as distinct problem areas. EVM Privacy CI covers only a bounded application-level subset of public execution and proof metadata; it does not claim to solve the full roadmap. [Ethereum privacy roadmap](https://ethereum.org/roadmap/privacy/)

## Policy assumptions

EVM Privacy CI assumes that users:

1. classify assets honestly and completely;
2. build their contracts successfully with the same configuration inspected in CI;
3. commit relevant generated artifacts and policy files or generate them reproducibly;
4. review any exception rather than using it to suppress a difficult finding;
5. run human review and appropriate security audits for high-value applications.

## Safe failure behavior

When the analyzer cannot model a path, it must emit a coverage finding—not a clean pass. Unsupported execution is a review task, not a safety conclusion.
