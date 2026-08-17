"""
A self-reported "done" is a claim, not a fact. This module makes that
distinction load-bearing: `verify()` only reports success once something
that did not make the claim has independently, freshly checked the real
state and agrees.

The mechanism generalizes the Auditor role from LongHorizon-Harness
(DreamX Team, Alibaba; arXiv:2608.01964): a fresh-context, read-only check
that runs after a worker claims completion, before that claim is allowed
to count as done. That paper builds the check into one specific harness
tied to particular coding-agent tooling and GUI+CLI computer-use tasks.
This module strips the mechanism down to its minimum form so it can wrap
*any* task, any agent, any language runtime that can call a function or
run a command.
"""

from dataclasses import dataclass
from typing import Any, Callable, Optional


@dataclass
class Claim:
    """What the worker says happened. Not trusted on its own."""

    ok: bool
    detail: str = ""
    data: Any = None


@dataclass
class AuditResult:
    """What an independent, read-only check actually found."""

    passed: bool
    detail: str = ""
    data: Any = None


@dataclass
class Verdict:
    """The outcome of a verify() run."""

    status: str  # "verified" or "rejected"
    claim: Claim
    audit: AuditResult
    rounds: int

    @property
    def verified(self) -> bool:
        return self.status == "verified"


def verify(
    do_work: Callable[[Optional[str]], Claim],
    audit: Callable[[], AuditResult],
    max_rounds: int = 1,
) -> Verdict:
    """
    Run `do_work`, independently `audit` the resulting state, and only
    report "verified" if the audit agrees with the claim. If it doesn't,
    retry with the audit's finding passed back as feedback, up to
    `max_rounds` total attempts.

    Parameters
    ----------
    do_work : Callable[[Optional[str]], Claim]
        Performs the task and returns a Claim. Receives the previous
        round's audit feedback as its argument (None on the first round).
        Must not be the same function that performs the audit.
    audit : Callable[[], AuditResult]
        Independently, read-only, checks the real state after `do_work`
        runs. Must not consult `do_work`'s claim to decide whether it
        passed — it checks the actual environment (a file, a test suite,
        a parsed document, an API response) on its own.
    max_rounds : int
        Maximum number of do_work/audit cycles before giving up. Each
        round is a genuine retry with the previous audit's detail as
        feedback, not a re-check of the same unchanged claim.

    Returns
    -------
    Verdict
        `.verified` is True only if some round's audit passed. The claim
        and audit attached to a rejected Verdict are from the final round,
        so the caller can see exactly what was claimed and what the audit
        found instead.
    """
    if max_rounds < 1:
        raise ValueError("max_rounds must be at least 1")

    feedback: Optional[str] = None
    claim: Optional[Claim] = None
    result: Optional[AuditResult] = None

    for round_n in range(1, max_rounds + 1):
        claim = do_work(feedback)
        result = audit()
        if result.passed:
            return Verdict(status="verified", claim=claim, audit=result, rounds=round_n)
        feedback = result.detail

    return Verdict(status="rejected", claim=claim, audit=result, rounds=max_rounds)
