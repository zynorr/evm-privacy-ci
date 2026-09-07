# EVM Privacy CI

> A local-first CI gate for privacy boundaries in Vela, zkVerify, and Solidity applications.

**Project status:** proposal-stage scaffold. The policy validator and rule catalogue are usable; static Solidity analysis, Vela probing, and zkVerify adapters are deliberately not represented as shipped features.

EVM Privacy CI turns a privacy promise into a testable engineering policy. A builder labels an asset as `secret`, `confidential`, `linkable`, or `public`; EVM Privacy CI then checks whether supported code paths expose that asset through observable EVM or proof-verification surfaces.

## The problem

Encryption, trusted execution, and zero-knowledge proofs do not automatically protect an application's public boundary. A supposedly private value can still escape in transaction calldata, events, raw on-chain storage, getters, return values, external calls, or ZK public inputs.

EVM Privacy CI does **not** certify privacy, replace a security audit, prove circuit soundness, or validate a TEE. It catches policy violations in a deliberately limited, explainable analysis scope. Read [the threat model](docs/threat-model.md) before relying on a finding or a pass.

## Scope

| Surface | v0 scaffold | v1 target |
| --- | --- | --- |
| Policy validation | Available | Stable JSON/YAML schema and migration tooling |
| Solidity/EVM rule engine | Catalogue and fixtures | Slither-backed source-to-sink analysis |
| Vela adapter | Design and fixture contract | Local boundary probe against Docker development flows |
| zkVerify adapter | Design and policy fields | Public-input, statement, and receipt policy checks |
| GitHub Actions/SARIF | Workflow scaffold | Release-quality action and code-scanning upload |

## Why Vela and zkVerify

Vela provides confidential TEE execution, but deployment, key registration, transaction envelopes, public state roots, and authorized disclosure controls are privacy boundaries. zkVerify validates proofs, but a valid proof may still contain a policy-prohibited public input. EVM Privacy CI is the engineering gate around those primitives, not a replacement for either one.

See [Vela adapter design](docs/adapters/vela.md) and [zkVerify adapter design](docs/adapters/zkverify.md).

## Quick start

The current scaffold uses only the Python standard library.

```bash
python -m pip install -e .
evm-privacy-ci validate-policy examples/basic/evm-privacy-ci.json
evm-privacy-ci explain VC003
```

Expected result:

```text
Policy is valid: examples/basic/evm-privacy-ci.json
```

The `scan` command intentionally exits with a clear not-yet-implemented message. This avoids a false impression that the repository already detects Solidity leaks.

## Example policy

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
      - zk_public_input
    allowed_disclosures:
      - surface: commitment
        transform: commitment_with_secret_blinder
```

Read the complete [policy specification](docs/policy-spec.md) before authoring a policy. A hash is not automatically considered a safe privacy transform.

## Architecture

```text
evm-privacy-ci.yaml
      |
      +-- Solidity analyzer ---- AST / IR / ABI / source maps
      |
      +-- Vela boundary probe - local transactions / logs / storage / artifact hash
      |
      +-- zkVerify adapter ---- public-input / statement / receipt policy
      |
      v
findings -> terminal + JSON + SARIF + CI annotations
```

The detailed architecture, interfaces, supported constructs, and non-goals are in [docs/architecture.md](docs/architecture.md).

## Rule catalogue

The initial rule IDs are stable design commitments, not claims of implementation:

| Rule | Summary |
| --- | --- |
| VC001 | Raw secret or confidential asset stored onchain |
| VC002 | Confidential asset reaches public or external ABI calldata |
| VC003 | Confidential asset reaches an event or log |
| VC004 | Confidential asset reaches a getter, view, or return value |
| VC005 | Confidential asset reaches an external call or error payload |
| VC006 | Confidential asset reaches deployment/immutable data |
| VC101 | Public ZK signal is missing a policy mapping |
| VC102 | Policy-prohibited asset is a ZK public input |
| VC201 | Unsupported execution path or stale suppression |

Every rule has a rationale, confidence model, examples, and required fixtures in [docs/rule-catalog.md](docs/rule-catalog.md).

## Repository map

```text
src/evm_privacy_ci/       Policy validator, CLI, rule metadata
tests/               Unit tests for shipped scaffold behavior
examples/            Valid policy and intentionally leaky Solidity examples
docs/                Product, security, architecture, and adapter documentation
.github/             CI, issue forms, pull request template
```

## Development

```bash
python -m unittest discover -s tests -v
python -m evm_privacy_ci validate-policy examples/basic/evm-privacy-ci.json
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules and [SECURITY.md](SECURITY.md) for vulnerability reporting.

## License status

The planned core license is **AGPL-3.0-or-later** because direct Slither integration is the cleanest technical route and Slither is AGPLv3. This repository intentionally carries a license-status notice rather than a final legal grant until a copyright holder and legal review are in place. See [LICENSE.md](LICENSE.md).

## References

- [Horizen Vela introduction](https://docs.horizen.io/vela/introduction/)
- [Vela local confidential-app walkthrough](https://docs.horizen.io/vela/getting-started/hello-world/)
- [zkVerify documentation](https://docs.zkverify.io/)
- [zkVerify proof-submission flow](https://docs.zkverify.io/architecture/proof-submission-interface)
- [Solidity visibility and getters](https://docs.soliditylang.org/en/v0.8.35/contracts.html)
- [Slither](https://github.com/crytic/slither)
