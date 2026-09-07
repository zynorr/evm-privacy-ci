# Fixture and benchmark strategy

**Status:** Designed. The Solidity examples in `examples/solidity/` are documentation fixtures; no analyzer executes them yet.

## Purpose

Privacy tooling cannot be evaluated with a pass/fail unit suite alone. Every rule needs a corpus demonstrating:

1. a policy violation that must be detected;
2. a safe or explicitly allowed case that must not be reported as a violation;
3. a coverage gap or ambiguous case that must not become a false pass.

## Fixture layout

```text
fixtures/
  vc001-raw-storage/
    policy.json
    contracts/Leak.sol
    expected.json
  vc003-event-disclosure/
    policy.json
    contracts/Leak.sol
    expected.json
  vc102-zk-public-input/
    policy.json
    contracts/Builder.sol
    artifacts/...
    expected.json
```

Each `expected.json` must declare rule ID, severity, source, sink, path expectations, and whether the fixture is a true positive, allowed case, or coverage gap.

## Initial fixture matrix

| Rule | Violation fixture | Safe fixture | Gap fixture |
| --- | --- | --- | --- |
| VC001 | private state salary write | approved ciphertext/commitment storage | assembly `sstore` |
| VC002 | external `pay(amount)` | external `pay(commitment)` | dynamic ABI encoding helper |
| VC003 | `emit Salary(amount)` | `emit PaymentCommitment(commitment)` | inherited assembly log |
| VC004 | public mapping/getter | public commitment getter | proxy implementation getter |
| VC005 | `target.call(amount)` | approved private adapter call | delegatecall |
| VC006 | secret constructor arg | public config constructor arg | factory-generated init payload |
| VC101 | unmapped input index | full public-signal map | unknown proof format |
| VC102 | amount in public input | nullifier in public input with reason | offchain builder unavailable |
| VC201 | unresolved selector | reviewed explicit exception | dynamic implementation address |

## Partner fixtures

Partner source code may not be publishable. A partner can contribute a redacted/minimized fixture and expected behavior instead. Do not add production contracts, wallet configs, test keys, confidential amounts, customer IDs, or unredacted traces to the public corpus.

## Quality metrics

Track rule quality by corpus and partner triage:

- true positives;
- false positives;
- false negatives discovered by human review;
- undecided cases;
- coverage gaps;
- median policy-authoring time;
- median execution time on a representative repository.

Publish counts and reproducible fixtures, not an unqualified “accuracy percentage.”
