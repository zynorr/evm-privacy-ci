# Rule catalogue

**Status:** Designed. Rule IDs and expected behavior are stable design targets. They are not claims that each detector has shipped.

## Severity and confidence

| Value | Meaning |
| --- | --- |
| `error` | CI fails by default because a policy-prohibited disclosure is found |
| `warning` | Review required; CI behavior is repository-configurable |
| `high` confidence | Exact supported source-to-sink flow found |
| `medium` confidence | Conservative flow or transform inference; reviewer should confirm |
| `low` confidence | Heuristic candidate; never the sole basis for a compliance claim |
| `coverage-gap` | The analyzer cannot make a safe conclusion about a relevant path |

The tool must report a confidence level independently from severity. A high-impact result is not necessarily high-confidence.

## VC001 — Raw protected asset stored onchain

| Field | Value |
| --- | --- |
| Default severity | `error` for `secret` and `confidential`; `warning` for unapproved `linkable` persistence |
| Primary surfaces | Storage writes, constructor/initializer writes, mappings, arrays, structs |
| Primary sources | Policy-selected state fields, values flowing from policy-selected parameters/locals |

### Detects

Direct or supported interprocedural flow of a protected asset into an EVM storage write, including a `private` state field. Solidity `private` is not confidentiality on a public chain.

```solidity
uint256 private salary;
function setSalary(uint256 amount) external { salary = amount; }
```

### Does not establish

- Whether a ciphertext is correctly encrypted.
- Whether a storage representation is a safe commitment.
- Whether a storage layout is inaccessible to a specialized observer.

### Remediation

Keep the raw value offchain/in the TEE/private witness. Store a declared commitment or encrypted representation only after manual cryptographic review.

### Known gaps

Inline assembly storage writes, delegatecall-controlled storage layouts, dynamic library paths, and external data source mutation produce VC201 coverage findings until supported.

## VC002 — Public ABI disclosure

| Field | Value |
| --- | --- |
| Default severity | `error` |
| Primary surfaces | External/public function arguments, ABI-encoded payloads, top-level transaction input |

### Detects

Protected assets passed through a function callable from outside the contract, or through a supported ABI encoder that becomes external transaction input.

```solidity
function submitOrder(uint256 amount, bytes32 proof) external { ... }
```

### Important distinction

An `internal` function parameter is not itself public; its call path must be followed. An `external` or `public` function parameter becomes a public transaction argument when used in an EVM transaction. Any value included in an EVM transaction call needs explicit policy treatment.

### Remediation

Pass an approved commitment, ciphertext, proof, opaque ID, or nothing. Do not “fix” by changing a function to `private` if the underlying value still reaches a public transaction somewhere else.

## VC003 — Event disclosure

| Field | Value |
| --- | --- |
| Default severity | `error` |
| Primary surfaces | Event data and indexed topics |

### Detects

Protected asset flow into an emitted event, including a flow into a base-contract event emitted from an inherited method.

```solidity
event SalaryPaid(address indexed employee, uint256 amount);
emit SalaryPaid(employee, salary);
```

### Why it matters

Events are public EVM logs. `indexed` fields are additionally searchable through topics. An encrypted-state design can be undermined by an ordinary event emission. Oasis specifically cautions that standard logs can reveal confidential state. [Oasis contract logs](https://docs.oasis.io/build/sapphire/develop/concept/)

### Remediation

Emit an opaque identifier, a policy-approved commitment, or an encrypted event payload appropriate to the app's architecture. If public linkability is required, classify the asset as `linkable` and document the reason.

## VC004 — Read disclosure

| Field | Value |
| --- | --- |
| Default severity | `error` |
| Primary surfaces | Public state-variable getters, public/external view functions, external returns |

### Detects

- a policy-labelled field exposed through a compiler-generated getter;
- a protected value directly returned from a public/external function;
- a supported aggregate return that contains a protected field.

```solidity
mapping(address => uint256) public salaryOf;
function getSalary(address employee) external view returns (uint256) {
    return salaryOf[employee];
}
```

### Remediation

Do not expose raw values through public reads. A contract can return an approved commitment or require offchain/TEE/private proof flow, but authorization in a Solidity function does not by itself make a value unobservable to chain observers.

## VC005 — Recipient disclosure

| Field | Value |
| --- | --- |
| Default severity | `error` |
| Primary surfaces | External-contract calls, low-level calls, ABI encoders, custom errors/revert data |

### Detects

Protected assets passed directly to another contract or encoded into a supported external payload.

```solidity
analytics.record(employee, salary);
target.call(abi.encodeWithSelector(selector, salary));
revert SalaryTooLow(salary);
```

### Remediation

Pass only a deliberate, reviewed disclosure. If the recipient is an authorized private component, model it through a future adapter rather than an unconditional generic allowlist.

### Known gaps

Dynamic `delegatecall`, arbitrary assembly, and code generated outside the compiler path are coverage gaps until modeled.

## VC006 — Deployment disclosure

| Field | Value |
| --- | --- |
| Default severity | `error` |
| Primary surfaces | Constructor ABI, initialization call, immutable initialization, deployment scripts where supported |

### Detects

Protected values passed during contract creation or an initializer. Constructor input and immutable values can be recovered from deployment/bytecode context.

```solidity
uint256 immutable salary;
constructor(uint256 initialSalary) { salary = initialSalary; }
```

### Remediation

Deploy with public configuration only. Keep secrets offchain; use an approved commitment/ciphertext with careful review where necessary.

## VC101 — Unmapped public ZK signal

| Field | Value |
| --- | --- |
| Default severity | `warning`, upgraded to `error` with `require_clean_coverage` |
| Primary surfaces | Public input arrays, proof metadata, artifact schemas |

### Detects

A supported proof adapter finds a public-input position not mapped by `proofs[].public_inputs[]`.

### Why it matters

Public signals are not automatically innocuous. A proof may be valid while exposing an unnecessary value. The rule requires every public position to have a human purpose and class.

### Remediation

Name the signal, assign its class, link an asset if relevant, and state its purpose. If the input is intentionally public, say so in policy rather than leaving it implicit.

## VC102 — Prohibited public ZK signal

| Field | Value |
| --- | --- |
| Default severity | `error` |
| Primary surfaces | Public input array, supported Solidity proof builder, artifact signal map |

### Detects

A `secret` or policy-prohibited `confidential` asset reaches a declared public input.

```solidity
uint256[] memory publicInputs = new uint256[](2);
publicInputs[0] = root;
publicInputs[1] = privateAmount; // policy violation
```

### Remediation

Move the raw value to the private witness, use the correct approved derived value, or explicitly revise the product privacy promise and policy through review.

### Does not establish

- Whether a public value is constrained by the circuit.
- Whether the circuit leaked information through a different mechanism.
- Whether the proof system is actually zero knowledge.

Circuit-analysis tools remain complementary. zkHydra, for example, runs several analysis techniques on Circom circuits. [zkHydra](https://github.com/zksecurity/zkhydra)

## VC201 — Coverage gap or stale exception

| Field | Value |
| --- | --- |
| Default severity | `warning`; `error` for expired/invalid exceptions and clean-coverage configuration |
| Primary surfaces | Assembly, proxies, delegatecall, unresolved selectors, artifact mismatch, exception records |

### Detects

- a policy selector that does not resolve;
- an unsupported code construct on a potentially relevant path;
- a proxy/delegatecall target that cannot be resolved;
- source/artifact mismatch;
- an exception with no owner, reason, issue, approver, or expiry;
- an expired exception.

### Remediation

Model the code path, add a reviewed adapter, repair the artifact/build relation, or conduct documented manual review. Never suppress a coverage gap merely to preserve a green badge.

## Rule quality requirements

A rule cannot become stable without:

1. documented sources and sinks;
2. one intentionally leaky fixture;
3. one safe/allowed-disclosure fixture;
4. one unsupported/ambiguous fixture when relevant;
5. unit and integration tests;
6. expected SARIF result; and
7. manual-review notes explaining false-positive and false-negative boundaries.
