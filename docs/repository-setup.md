# Repository setup and first push

**Status:** Local Git repository initialized on `main`; no remote is configured and nothing has been published.

## Before creating a public GitHub repository

Complete these items first:

1. Decide whether the working name **VeilCheck** has passed formal name/trademark review. Do not use it publicly until then.
2. Identify real maintainers and replace pre-release placeholders in `SECURITY.md`, `GOVERNANCE.md`, and `CODE_OF_CONDUCT.md`.
3. Select a final license after legal review; `LICENSE.md` is intentionally not a final license grant.
4. Review every example and fixture for keys, real addresses, production source, user data, and sensitive traces.
5. Run the local test suite using the commands in the README.
6. Create the GitHub repository as private until the release checklist is complete.

## Suggested repository settings

- Default branch: `main`.
- Require pull requests for `main` after there is more than one maintainer.
- Require the `CI` and `Documentation hygiene` checks.
- Require signed commits if the team already uses them.
- Enable private vulnerability reporting after a real contact is configured.
- Enable Dependabot version updates.
- Do not enable public issue intake until `SECURITY.md` has a functioning private reporting route.

## First push commands

Replace placeholders only after the repository exists and naming/licensing decisions are complete:

```bash
git add .
git commit -m "chore: initialize privacy-boundary CI project scaffold"
git remote add origin https://github.com/<organization>/<repository>.git
git push -u origin main
```

Do not include a remote access token in a command, README, workflow, or commit. Use GitHub CLI authentication, Git Credential Manager, SSH, or a securely stored fine-grained token instead.

## Git safety note

This project directory may be owned by the desktop user while automated tooling runs under a sandbox identity. If Git reports “dubious ownership” locally, use a command-scoped safe-directory setting rather than permanently trusting broad paths:

```bash
git -c safe.directory="$(pwd)" status
```
