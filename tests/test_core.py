import pytest

from no_self_grade import Claim, AuditResult, verify


def test_verified_on_first_round_when_audit_passes():
    def do_work(feedback):
        assert feedback is None
        return Claim(ok=True, detail="done")

    def audit():
        return AuditResult(passed=True, detail="confirmed")

    v = verify(do_work, audit, max_rounds=3)
    assert v.verified
    assert v.status == "verified"
    assert v.rounds == 1
    assert v.claim.detail == "done"
    assert v.audit.detail == "confirmed"


def test_rejected_when_audit_never_passes():
    def do_work(feedback):
        return Claim(ok=True, detail="I say it's done")

    def audit():
        return AuditResult(passed=False, detail="the file was never actually written")

    v = verify(do_work, audit, max_rounds=2)
    assert not v.verified
    assert v.status == "rejected"
    assert v.rounds == 2
    assert v.audit.detail == "the file was never actually written"


def test_claim_success_does_not_override_a_failing_audit():
    """The core scenario this whole library exists for: the worker says
    'done', but the independent check disagrees. The audit wins."""

    def do_work(feedback):
        return Claim(ok=True, detail="all tests pass")

    def audit():
        return AuditResult(passed=False, detail="3 of 12 tests still fail")

    v = verify(do_work, audit, max_rounds=1)
    assert v.claim.ok is True
    assert not v.verified


def test_feedback_is_passed_to_the_next_round():
    seen_feedback = []

    def do_work(feedback):
        seen_feedback.append(feedback)
        return Claim(ok=True, detail=f"attempt {len(seen_feedback)}")

    calls = {"n": 0}

    def audit():
        calls["n"] += 1
        if calls["n"] < 3:
            return AuditResult(passed=False, detail=f"missing case {calls['n']}")
        return AuditResult(passed=True, detail="all cases covered")

    v = verify(do_work, audit, max_rounds=5)
    assert v.verified
    assert v.rounds == 3
    assert seen_feedback == [None, "missing case 1", "missing case 2"]


def test_gives_up_after_max_rounds_and_reports_the_final_attempt():
    attempts = []

    def do_work(feedback):
        attempts.append(feedback)
        return Claim(ok=True, detail=f"attempt {len(attempts)} of 2")

    def audit():
        return AuditResult(passed=False, detail="still broken")

    v = verify(do_work, audit, max_rounds=2)
    assert len(attempts) == 2
    assert v.rounds == 2
    assert not v.verified
    assert v.claim.detail == "attempt 2 of 2"


def test_max_rounds_must_be_at_least_one():
    with pytest.raises(ValueError):
        verify(lambda fb: Claim(ok=True), lambda: AuditResult(passed=True), max_rounds=0)
