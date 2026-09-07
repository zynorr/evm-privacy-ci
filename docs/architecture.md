# Architecture

**Status:** Designed; only policy validation and rule metadata are implemented in the scaffold.

## Design principles

1. **Policy before inference.** The tool cannot reliably infer business sensitivity from names or types.
2. **Local before hosted.** A privacy tool should not require source upload to assess privacy boundaries.
3. **Determinism before prose.** Enforcement decisions must be reproducible without an LLM.
4. **Coverage before confidence.** Unsupported constructs are visible findings.
5. **Composition before reinvention.** Slither provides Solidity parsing and analysis primitives; zkHydra and similar circuit tools remain complementary.

## High-level data flow

```text
                 +---------------------------+
                 | evm-privacy-ci policy document |
                 +-------------+-------------+
                               |
                               v
                     +-------------------+
                     | policy normalizer |
                     +-------------------+
                               |
  source + build artifacts ----+---------------------+
                               |                     |
                               v                     v
                    +-------------------+  +--------------------+
                    | Solidity adapter  |  | proof/TEE adapters |
                    | AST, IR, ABI      |  | Vela, zkVerify      |
                    +---------+---------+  +---------+----------+
                              |                      |
                              +----------+-----------+
                                         v
                              +-------------------+
                              | finding engine    |
                              | flows + coverage  |
                              +---------+---------+
                                        |
                       +----------------+----------------+
                       v                v                v
                    terminal            JSON            SARIF
```

## Components

### 1. Policy parser and normalizer

**Implemented (partial):** JSON `evm-privacy-ci/v1` validation using the Python standard library.
**Designed:** YAML parsing, JSON Schema validation, source-location errors, schema migration, policy inheritance, and canonical JSON output.

The normalizer turns selectors, classifications, allowed disclosures, exceptions, and proof maps into a canonical internal model. The analyzer consumes only that model.

### 2. Solidity adapter

**Designed:** A Slither plugin package creates source, sink, and data-flow facts from Slither's AST and SlithIR. Slither supports custom detector plugins and is the preferred first implementation route. [Slither plugin documentation](https://github.com/crytic/slither/wiki/Adding-a-new-detector)

#### Inputs

- compiled Solidity project;
- source maps and AST emitted through the project’s compiler flow;
- ABI/artifacts;
- normalized policy;
- optional framework configuration for Foundry or Hardhat.

#### Fact model

```text
Asset selector -> source variable / parameter / field
Source -> definition/use graph
Sink -> public EVM surface
Path -> interprocedural chain of IR operations
Finding -> asset + source + sink + path + policy rule + confidence
```

#### Sink registry

The adapter owns a versioned sink registry. Sinks include event arguments, storage writes, external/public ABI values, generated getters, return values, external-call arguments, constructor inputs, custom error arguments, ABI encoders, and proof-input builders.

The registry is a security-sensitive API: adding or removing a sink requires fixtures, documentation, and review.

### 3. Vela boundary probe

**Designed:** A local integration runner starts only against Vela's documented Docker development workflow. It injects non-production sentinel values through test commands, then searches public transaction input, receipts, logs, permitted storage reads, and generated reports for exact sentinel or unsafe transformations.

The probe does not inspect TEE memory, prove encryption, or make a hardware-attestation claim. See [Vela adapter design](adapters/vela.md).

### 4. zkVerify adapter

**Designed:** Reads a public-input map and proof-system-specific metadata. It checks that every public input is named and classified, then connects supported Solidity builder paths to policy assets. It treats the proof statement and EVM aggregation receipt as public/linkable surfaces.

See [zkVerify adapter design](adapters/zkverify.md).

### 5. Dynamic trace adapter

**Proposed, post-v1:** Ingest local Anvil, Foundry, or Hardhat traces. It adds execution evidence to static findings and detects values introduced through a test builder that static analysis did not model. Dynamic traces are complementary: unexecuted paths remain untested.

Foundry can produce detailed call traces for all tests, providing a viable local integration point. [Foundry traces](https://getfoundry.sh/forge/traces)

### 6. Finding engine

The engine deduplicates equivalent paths, applies severity, validates exceptions, tracks baseline findings, and serializes output.

#### Finding identity

Each finding has:

- stable `ruleId`;
- canonical asset ID;
- source and sink location;
- path fingerprint;
- policy-file fingerprint;
- analyzer version;
- confidence (`high`, `medium`, `low`, `coverage-gap`);
- remediation and documentation URL.

The fingerprint must be stable across harmless line movement where source maps permit it, while a semantic path change must create a new reviewable finding.

### 7. Output adapters

| Output | Purpose |
| --- | --- |
| terminal | Local developer feedback |
| JSON | Machine integration, benchmarks, partner evidence |
| SARIF | GitHub code-scanning annotations |
| Markdown checklist | Human privacy-boundary review and audit handoff |

GitHub accepts third-party SARIF results in code scanning. [GitHub SARIF documentation](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/integrate-with-existing-tools/upload-sarif-file)

## Analysis algorithm: intended v1

1. Compile the repository using its trusted local build configuration.
2. Parse and normalize the policy.
3. Resolve every policy selector to zero, one, or several source entities.
4. Emit a coverage finding for any selector that cannot be resolved.
5. Build data-flow facts over supported SlithIR operations.
6. Propagate asset taint through assignments, calls, struct fields, arrays, mappings, and supported encoding operations.
7. Compare every reached sink to the asset’s forbidden and allowed disclosures.
8. Emit a finding on forbidden sinks; emit review findings on ambiguous transforms or unsupported paths.
9. Validate policy exceptions and public-input maps.
10. Produce results and fail CI only according to configured severity policy.

## Transform handling

EVM Privacy CI must not silently “declassify” an asset after `keccak256`, encryption, or an arbitrary library call. A transform is allowed only if the policy declares it and the rule implementation recognizes its supported form.

For example, an approved commitment must declare a transform such as `commitment_with_secret_blinder`. The analyzer then checks the supported construction has a designated secret blinder input. This is an implementation check—not a cryptographic proof that the commitment is hiding or binding.

## Trust boundaries

| Boundary | Risk | Control |
| --- | --- | --- |
| Repository -> compiler | Build scripts may execute arbitrary code | Containerized safe mode, locked toolchain, no secrets, documented trust requirement |
| Compiler -> analyzer | Artifact/source mismatch | Verify compiler configuration and artifact references; report mismatch |
| Policy -> analyzer | Wrong classifications create false assurance | Explicit policy review, unresolved selectors fail coverage |
| CI -> reports | Findings may reveal security/privacy design | Local artifacts, opt-in SARIF upload, no external telemetry |
| Suppression -> pass | Exceptions hide regressions | Owner, reason, expiry, and CI validation |

## Versioning

- Policy schemas use `evm-privacy-ci/vN` identifiers.
- Rule IDs never change meaning after first stable release.
- A changed detection semantic requires a new rule ID or an explicit major-version compatibility note.
- Adapter compatibility is separately versioned from the policy schema.
