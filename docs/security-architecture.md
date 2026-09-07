# Security architecture

**Status:** Designed. This document is a release requirement, not aspirational security language.

## Principle

EVM Privacy CI processes source code, build artifacts, privacy policies, and potentially traces. Those inputs can reveal an application's attack surface or privacy design. The tool must never create a larger privacy exposure than the one it detects.

## Data handling commitments for v1

- No account, authentication, cloud dashboard, or remote scan.
- No source-code upload.
- No default telemetry, analytics, crash reporting, RPC call, or dependency auto-download during scan.
- No collection of policy contents, findings, trace values, or repository identifiers.
- Reports stay in the local working directory unless a user explicitly uploads SARIF through their own CI configuration.

## Safe execution modes

### Default local mode

Runs analysis against an already compiled repository. It may read declared source/artifact paths but must not mutate source files.

### Containerized build mode

Compiling a repository can execute untrusted build scripts. The release-quality container mode must:

- run without network access by default;
- mount the repository read-only where possible;
- write artifacts only to an explicit output directory;
- have no wallet, SSH, cloud, package-manager, or deployment credentials;
- pin tool versions and image digest;
- disclose that compilation remains trusted-code execution inside the selected sandbox.

### CI mode

- Use least-privilege GitHub token permissions.
- Do not expose secrets to pull-request builds from untrusted forks.
- Treat SARIF as potentially sensitive repository metadata.
- Upload reports only when project policy allows it.

## Supply-chain controls

Before public release:

1. Pin all direct dependencies and record checksums where ecosystem tooling permits.
2. Publish an SBOM for releases.
3. Sign release artifacts and publish provenance.
4. Scan dependencies and containers in CI.
5. Require code review for sink-registry, policy-schema, adapter, and release-workflow changes.
6. Publish a responsible disclosure address and security advisory workflow.

## Secret handling

EVM Privacy CI must reject or warn about known secret-bearing input paths such as `wallet.conf`, `.env`, PEM/key files, and raw Vela wallet state when they are passed as analysis targets. It must not log their contents.

The Vela adapter must generate or use non-production test sentinels; it must not operate on real P-521 private keys, deployment keys, or user data.

## Report hygiene

Findings should include source/sink locations and policy asset IDs, but avoid copying full sensitive literal values. Dynamic probes may report a hashed/redacted sentinel correlation instead of emitting the raw sentinel.

## Security boundaries EVM Privacy CI cannot enforce

- Developer workstation compromise.
- Compromised compiler, dependency, or Docker daemon.
- Private keys supplied by a user to unrelated build scripts.
- Security of an application’s cryptographic primitives.
- Trustworthiness of a remote RPC endpoint.

Those limitations must remain visible in docs and release notes.
