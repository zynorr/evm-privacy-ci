"""Stable metadata for the first EVM Privacy CI rule catalogue.

These entries describe the intended rules. They are not evidence that a
corresponding analyzer has shipped.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    identifier: str
    title: str
    default_severity: str
    summary: str


RULES = {
    "VC001": Rule("VC001", "Raw protected asset stored onchain", "error", "Flags a secret or confidential asset written raw to EVM storage."),
    "VC002": Rule("VC002", "Public ABI disclosure", "error", "Flags a protected asset that reaches externally observable calldata."),
    "VC003": Rule("VC003", "Event disclosure", "error", "Flags a protected asset that reaches an EVM event or log."),
    "VC004": Rule("VC004", "Read disclosure", "error", "Flags a protected asset exposed by a getter, view function, or return value."),
    "VC005": Rule("VC005", "Recipient disclosure", "error", "Flags a protected asset passed to an external recipient or error payload."),
    "VC006": Rule("VC006", "Deployment disclosure", "error", "Flags a protected asset in constructor or immutable deployment data."),
    "VC101": Rule("VC101", "Unmapped public ZK signal", "warning", "Flags a ZK public input without a policy mapping."),
    "VC102": Rule("VC102", "Prohibited public ZK signal", "error", "Flags a policy-prohibited protected asset used as a ZK public input."),
    "VC201": Rule("VC201", "Coverage gap or stale exception", "warning", "Reports unsupported execution or an invalid policy exception."),
}
