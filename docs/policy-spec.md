# EVM Privacy CI policy specification

**Schema:** `evm-privacy-ci/v1`
**Status:** Designed. The repository scaffold validates the required JSON subset; YAML parsing, JSON Schema enforcement, source-map selectors, exceptions, and adapters are not implemented yet.

## 1. Purpose

A policy tells EVM Privacy CI which application assets need protection, where those assets occur in the code, and which public disclosures are either prohibited or deliberately allowed.

The policy is not a privacy policy for end users and is not a legal compliance document. It is an engineering control checked against a limited analysis scope.

## 2. File location and format

The canonical path is:

```text
evm-privacy-ci.yaml
```

The preferred authoring format is YAML. The canonical generated form is JSON. The proposal-stage CLI currently accepts `.json` only so that the scaffold has no undeclared parser dependency; use [examples/basic/evm-privacy-ci.json](../examples/basic/evm-privacy-ci.json) to exercise it.

Before the first release, YAML support must use a pinned, reviewed parser and validate against [`schemas/evm-privacy-ci-v1.schema.json`](../schemas/evm-privacy-ci-v1.schema.json).

## 3. Minimal document

```yaml
schema: evm-privacy-ci/v1
assets:
  - id: payroll.amount
    class: confidential
    selectors:
      - contracts/Payroll.sol::Payee.amount
    forbidden_surfaces:
      - transaction_calldata
      - event
      - storage
      - public_getter
```

## 4. Top-level fields

| Field | Required | Meaning |
| --- | --- | --- |
| `schema` | yes | Must be `evm-privacy-ci/v1` |
| `assets` | yes | Non-empty list of classified assets |
| `proofs` | no | Proof-system/public-input policy maps |
| `vela` | no | Vela deployment and boundary assertions |
| `exceptions` | no | Time-bounded, auditable finding exceptions |
| `defaults` | no | Repository-wide default severities and CI behavior |
| `metadata` | no | Owner, repository, review date, and evidence links; never secrets |

Unknown top-level fields must be rejected in the stable schema. Unknown values are a policy-maintenance problem, not a forward-compatibility feature.

## 5. Assets

### Required fields

| Field | Meaning |
| --- | --- |
| `id` | Stable lowercase dotted identifier, unique within the document: `trade.amount` |
| `class` | `secret`, `confidential`, `linkable`, or `public` |
| `selectors` | One or more code/artifact locations that identify the asset |

### Optional fields

| Field | Meaning |
| --- | --- |
| `description` | Human explanation of the asset and sensitivity |
| `owners` | Named maintainers responsible for policy changes |
| `forbidden_surfaces` | Public surfaces that cannot receive the asset |
| `allowed_disclosures` | Specific deliberate disclosures and required transform metadata |
| `review_required_surfaces` | Surfaces permitted only with manual review finding |
| `retention` | Intended future control for persistence analysis; informational in v1 |

### Classification semantics

#### `secret`

The raw value must never be sent onchain, written to a report, or configured in policy. Examples include a private key, note secret, encryption key, and unblinded witness. The default `secret` policy forbids every known public surface.

#### `confidential`

The raw value has restricted disclosure. It may be carried inside an approved ciphertext, commitment, TEE environment, or ZK private witness only when the policy names that use. A salary, order amount, recipient identity, or private strategy is normally `confidential`.

#### `linkable`

The value may be public but creates correlation risk. A nullifier, commitment, statement digest, deposit ID, registered public key, or account identifier should be declared `linkable`, with an explicit reason for its public surfaces. Do not label it `public` merely because a protocol requires it to be visible.

#### `public`

The value is intentionally public. Use sparingly; a public classification is a deliberate policy decision and should have a description.

## 6. Selectors

The stable selector grammar is:

```text
<path>::<contract-or-module>.<member>[.<nested-member>]
<path>::<contract-or-module>::<function>.<parameter-or-return>
artifact:<path>#<json-pointer>
```

Examples:

```yaml
selectors:
  - contracts/Payroll.sol::Payroll.pay.amount
  - contracts/OrderBook.sol::Order.amount
  - contracts/PrivateToken.sol::balances.value
  - artifact:artifacts/circuit.json#/publicSignals/3
```

### Resolution requirements

- A selector resolving to zero sources yields a coverage finding.
- A selector resolving to more sources than expected yields a review finding unless the policy declares `allow_multiple: true`.
- A source moved or renamed must require a policy update; fuzzy name matching must never silently keep a policy green.
- Selectors cannot contain wildcards in v1. Explicitness is more valuable than convenience for a privacy policy.

## 7. Public surfaces

| Surface | Meaning |
| --- | --- |
| `transaction_calldata` | Data passed through an external EVM call/transaction ABI |
| `event` | Event topics or event data |
| `storage` | EVM storage or raw persisted state |
| `public_getter` | Generated getter or public/external view read |
| `return_value` | Externally observable return data |
| `external_call` | Arguments or payload sent to a non-local EVM target |
| `deployment_data` | Constructor/creation/immutable initialization data |
| `zk_public_input` | Public input to a proof system |
| `commitment` | Explicitly declared cryptographic commitment |
| `vela_encrypted_event` | Event/data returned to Vela client after declared encryption |
| `zkverify_statement` | Public zkVerify statement/leaf digest |
| `zkverify_receipt` | Public zkVerify aggregation-receipt information consumed on EVM |

## 8. Allowed disclosures

An allowed disclosure is a narrow exception to a classification. It must name a surface and, for any transform, the intended transform.

```yaml
allowed_disclosures:
  - surface: commitment
    transform: commitment_with_secret_blinder
    blinder_selector: circuits/order.circom::order_blinder
    purpose: Membership proof without exposing amount or owner
    reviewer: privacy-engineering
```

### Transform rules

- `keccak256`, `sha256`, encryption, encoding, and custom library calls are **not** automatically safe transforms.
- `commitment_with_secret_blinder` is a supported future pattern only if the analysis sees a specified secret blinder on the recognized construction path.
- Any unrecognized transform is a review finding, not an implicit allow.
- An allowed disclosure changes a policy result; it does not provide a cryptographic assurance.

## 9. zkVerify proof maps

Every supported public input needs a semantic mapping.

```yaml
proofs:
  - id: order-validity-groth16
    system: groth16
    adapter: zkverify
    verifier_context: groth16
    verification_key:
      source: artifact:artifacts/order-vk.json#/hash
    public_inputs:
      - index: 0
        name: merkle_root
        class: public
        purpose: Current membership-tree root
      - index: 1
        name: nullifier
        asset: order.nullifier
        class: linkable
        purpose: Prevent double spend
      - index: 2
        name: amount
        asset: order.amount
        class: confidential
        allowed: false
```

Rules:

1. Every input position has a unique `index` and `name`.
2. `asset` is required if the input derives from a classified application asset.
3. A `secret` asset can never be `allowed: true` as a public input.
4. A `confidential` asset requires an explicit review/transform policy; raw disclosure is blocked.
5. `linkable` inputs require a stated `purpose`.
6. Input count/order drift between metadata and source/artifacts fails CI once the adapter supports that proof family.

## 10. Vela boundary assertions

```yaml
vela:
  applications:
    - id: private-payroll
      wasm_artifact: artifacts/payment_app.wasm
      approved_sha256: "REPLACE_WITH_RELEASE_HASH"
      protected_test_sentinels:
        - asset: payroll.amount
          value_source: test-fixture-only
      permitted_public_surfaces:
        - application_id
        - state_root
        - user_p521_public_key
      authorized_disclosures:
        - operation: deanonymize
          role: AUDITOR_ROLE
          purpose: Authorized audit flow
```

The file must never contain a production key, real employee amount, raw witness, P-521 private key, or copied wallet configuration.

## 11. Exceptions

Exceptions are a documented review decision, not a way to make CI quiet.

```yaml
exceptions:
  - id: VEX-2026-001
    rule: VC003
    asset: proof.nullifier
    location: contracts/Verifier.sol:84
    reason: Nullifier emission is required to prevent replay and is policy-declared linkability.
    owner: protocol-security@example.invalid
    approved_by: reviewer@example.invalid
    expires: 2026-12-31
    issue: https://example.invalid/issues/123
```

The stable validator must reject exceptions without `reason`, `owner`, `approved_by`, `expires`, and `issue`. An expired exception produces `VC201` at error severity.

## 12. CI defaults

```yaml
defaults:
  fail_on:
    - error
  require_clean_coverage: true
  baseline: .evm-privacy-ci/baseline.json
```

`require_clean_coverage: true` means an unsupported code path cannot produce a passing privacy gate. Teams may set it to false only with an explicit, reviewed exception in v1.

## 13. Complete example

```yaml
schema: evm-privacy-ci/v1
metadata:
  owner: protocol-security
  review_date: 2026-09-07

assets:
  - id: payroll.amount
    class: confidential
    description: Net salary amount processed inside confidential execution.
    selectors:
      - contracts/PayrollGateway.sol::PayrollGateway.deposit.amount
    forbidden_surfaces:
      - transaction_calldata
      - event
      - storage
      - public_getter
      - zk_public_input
    allowed_disclosures:
      - surface: commitment
        transform: commitment_with_secret_blinder
        purpose: Commitment used for private payment proof.

  - id: payroll.nullifier
    class: linkable
    selectors:
      - contracts/PayrollVerifier.sol::nullifier
    allowed_disclosures:
      - surface: event
        purpose: Double-spend prevention.
      - surface: zk_public_input
        purpose: Proof statement binding.

proofs:
  - id: payroll-proof
    system: groth16
    adapter: zkverify
    public_inputs:
      - index: 0
        name: payroll_root
        class: public
        purpose: Membership root.
      - index: 1
        name: nullifier
        asset: payroll.nullifier
        class: linkable
        purpose: One-time payment marker.
```
