# EVM Privacy CI documentation

EVM Privacy CI is a proposal-stage open-source project. This documentation is intentionally specific about current behavior, planned behavior, and unresolved decisions.

| Read this | When you need to know |
| --- | --- |
| [Project charter](project-charter.md) | Why EVM Privacy CI exists, who it serves, and what success looks like |
| [Threat model](threat-model.md) | What a finding or pass does and does not mean |
| [Architecture](architecture.md) | Component design, data flow, interfaces, and trust boundaries |
| [CLI and output specification](cli-spec.md) | Command, exit-code, JSON, and SARIF contracts |
| [Policy specification](policy-spec.md) | How to write `evm-privacy-ci/v1` policy documents |
| [Rule catalogue](rule-catalog.md) | What every rule detects, misses, and requires |
| [Vela adapter](adapters/vela.md) | Boundary checks for Vela local development |
| [zkVerify adapter](adapters/zkverify.md) | Public-input, statement, and receipt checks |
| [Fixture strategy](fixtures.md) | How rules are tested against intentional leaks and safe cases |
| [Validation plan](validation-plan.md) | Design-partner, precision, and demand evidence plan |
| [Pilot guide](pilot-guide.md) | How a design partner evaluates EVM Privacy CI without exposing sensitive code/data |
| [Competitive landscape](competitive-landscape.md) | What exists, what EVM Privacy CI adds, and claims to avoid |
| [Risk register](risk-register.md) | Product, technical, legal, and ecosystem risks with mitigations |
| [Security architecture](security-architecture.md) | How EVM Privacy CI protects repositories, reports, and CI |
| [Roadmap](roadmap.md) | Release phases, milestones, and acceptance gates |
| [Implementation plan](implementation-plan.md) | Work packages, package layout, and pre-coding decisions |
| [Release checklist](release-checklist.md) | What must be true before public release |
| [Repository setup](repository-setup.md) | How to prepare the local repository and first GitHub push |
| [Architecture decisions](decisions/) | Decisions that have been made and those still open |

## Reading convention

- **Implemented** means code and tests exist in this repository.
- **Designed** means the behavior is specified but is not a shipped feature.
- **Proposed** means it needs validation, a design partner, or a decision before implementation.

Any issue, README statement, or release note that blurs those terms is a documentation defect.
