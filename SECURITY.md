# Security policy

## Scope

EVM Privacy CI is security-sensitive developer tooling. Findings, policies, local trace data, fixtures, and build integrations may reveal information about an application's threat model. Treat reports as potentially sensitive.

## Reporting a vulnerability

Until a dedicated security contact is published, do **not** open a public issue for a suspected vulnerability that could expose user funds, private data, build secrets, or a bypass of an enforcement rule.

Send a private report to the maintainer contact listed in the future GitHub repository security advisory configuration. Include:

- affected EVM Privacy CI version or commit;
- minimal reproduction steps;
- impact and likely affected users;
- a safe proof of concept; and
- any suggested mitigation.

The project will publish a responsible-disclosure contact before the first public release. This file must be updated with the real channel before a repository is made public.

## Operational guarantees

EVM Privacy CI must not upload source code, policies, traces, private keys, or telemetry by default. Any future networked feature must be opt-in, documented, and independently reviewed.
