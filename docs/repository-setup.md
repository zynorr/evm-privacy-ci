# Repository setup and first push

**Status:** Public repository initialized on `main` at `zynorr/evm-privacy-ci`.

## Before a public release

Complete these items first:

1. Identify real maintainers and replace pre-release placeholders in `SECURITY.md`, `GOVERNANCE.md`, and `CODE_OF_CONDUCT.md`.
2. Select a final license after legal review; `LICENSE.md` is intentionally not a final license grant.
3. Review every example and fixture for keys, real addresses, production source, user data, and sensitive traces.
4. Run the local test suite using the commands in the README.
5. Review repository visibility and issue intake against the release checklist.

## Suggested repository settings

- Default branch: `main`.
- Require pull requests for `main` after there is more than one maintainer.
- Require the `CI` and `Documentation hygiene` checks.
- Require signed commits if the team already uses them.
- Enable private vulnerability reporting after a real contact is configured.
- Enable Dependabot version updates.
- Do not enable public issue intake until `SECURITY.md` has a functioning private reporting route.

## Publishing a clean clone

After cloning the repository and authenticating with GitHub:

```bash
git push -u origin main
```

Do not include a remote access token in a command, README, workflow, or commit. Use GitHub CLI authentication, Git Credential Manager, SSH, or a securely stored fine-grained token instead.

## Git safety note

This project directory may be owned by the desktop user while automated tooling runs under a sandbox identity. If Git reports “dubious ownership” locally, use a command-scoped safe-directory setting rather than permanently trusting broad paths:

```bash
git -c safe.directory="$(pwd)" status
```
