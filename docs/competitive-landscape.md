# Competitive landscape and positioning

**Status:** Research snapshot, 2026-09-07. This is evidence for positioning, not a claim of exhaustive worldwide competitor absence.

## Conclusion

The underlying techniques are established. The opportunity is the composition:

> A policy-driven CI gate that connects declared privacy assets to public EVM surfaces, Vela boundaries, and zkVerify public-input/receipt metadata in existing Solidity/ZK applications.

Do not call VeilCheck “the first privacy linter” or “the only privacy scanner.” The defensible wording is:

> “In our public survey, we did not identify a maintained EVM tool that combines developer-declared privacy claims, Solidity public-surface data flow, and proof public-input policy in CI.”

## Adjacent solutions

| Tool or category | What it covers | VeilCheck relationship |
| --- | --- | --- |
| [Slither](https://github.com/crytic/slither) | Solidity/Vyper static analysis framework and custom detectors | Foundation/analysis dependency, not a competitor to rebuild |
| Solhint and generic EVM scanners | Style, known security patterns, generic vulnerabilities | Adjacent; VeilCheck must not become another generic scanner |
| [zkHydra](https://github.com/zksecurity/zkhydra) | Runs Circom circuit analyzers, SMT checks, symbolic execution, and fuzzing | Complementary circuit analysis; does not own Solidity-to-proof-boundary policy |
| [zkay](https://github.com/eth-sri/zkay) | Research language/compiler turning privacy annotations into private smart contracts | Important precedent; VeilCheck works with existing Solidity/ZK code and is not a privacy compiler |
| [Paralegal](https://github.com/brownsys/paralegal) | Policy/annotation-driven privacy and security analysis for Rust | Closest conceptual precedent; confirms policy-marked static analysis is viable, but it is not EVM tooling |
| [ERC-8086](https://eips.ethereum.org/EIPS/eip-8086) | Draft privacy token interface and privacy configuration file with public signal schema | Input/adaptation opportunity; VeilCheck should consume where relevant, not create competing metadata standards |
| Manual security/privacy audits | Contextual human review | VeilCheck prepares repeatable evidence and catches regressions; it does not replace audits |

## Differentiating decisions

### Existing repositories first

zkay demonstrates privacy specifications compiled into a special-purpose language, but its repository describes itself as a research project and warns against using it for production confidential data. VeilCheck targets existing Solidity repositories and their surrounding ZK/TEE integration points. [zkay](https://github.com/eth-sri/zkay)

### Boundary, not primitive

Circuit tools inspect circuit bugs. Generic Solidity tools inspect security patterns. VeilCheck asks whether a product's declared confidentiality claim survives contact with transaction encoding, logs, generated getters, storage, public signal metadata, and proof receipts.

### Policy as a maintainer artifact

Paralegal’s Rust model is a useful precedent: privacy engineers define high-level policy over code markers, then analysis enforces it. VeilCheck adopts that principle because EVM code alone cannot infer business confidentiality. [Paralegal](https://www.usenix.org/conference/osdi25/presentation/adam)

### Horizen-specific adapters, portable core

Vela and zkVerify give the first ecosystem focus. The policy language names generic public surfaces so the underlying project remains useful for EVM applications that choose different privacy implementations.

## Claim guardrails

| Avoid | Use instead |
| --- | --- |
| “First privacy linter” | “Policy-driven privacy-boundary CI for Solidity/ZK apps” |
| “Guarantees privacy” | “Finds configured disclosure-policy violations in supported scope” |
| “Audits Vela/zkVerify” | “Checks integration-boundary policy around Vela/zkVerify workflows” |
| “Replaces smart-contract audits” | “Provides repeatable pre-audit evidence and regression checks” |
| “ZK proof is private” | “Every public input must be classified and justified” |

## Watch list

Re-run this survey before public launch and each grant milestone. Monitor:

- Slither privacy-focused plugins and rule packs;
- new EVM privacy-policy analyzers;
- Vela native security/developer tools;
- zkVerify public-input metadata tooling;
- ERC-8086 maturity and competing standards;
- confidential-compute framework linting from Oasis, Zama, Fhenix, and related stacks.
