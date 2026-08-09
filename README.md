<div align="center">

# no-self-grade

**Don't let a self-reported "done" count until an independent, read-only check confirms it.**

A minimal, framework-agnostic generalization of the Auditor pattern from [LongHorizon-Harness](https://arxiv.org/abs/2608.01964) (DreamX Team, Alibaba, arXiv:2608.01964): a fresh-context, independent check that runs after a worker claims completion, and whose verdict is authoritative. LongHorizon-Harness builds that check into one specific harness tied to Claude Code/Codex and GUI+CLI computer-use tasks. This strips it down to about 30 lines so it can wrap any task, any agent, any language runtime.

[![Tests](https://img.shields.io/badge/tests-passing-1f6e4a?style=flat-square)](tests/)
[![License: MIT](https://img.shields.io/badge/license-MIT-3d5a80?style=flat-square)](LICENSE)
[![Dependencies: none](https://img.shields.io/badge/dependencies-none-a3271f?style=flat-square)](pyproject.toml)
[![Aligna Builds](https://img.shields.io/badge/Aligna%20Builds-no--self--grade-1a1a17?style=flat-square)](https://aligna-solutions.github.io/)

[**Read the research writeup →**](RESEARCH.md)

</div>

---

## Why this exists

A coding agent that reports "all tests pass" might be telling the truth, or it might have special-cased the one input the visible test checks. A validation script that now reports "PASS" might mean the underlying data got fixed, or it might mean someone weakened the validator. LongHorizon-Harness's actual finding, independent of its specific GUI/CLI tooling, is that **a claim of done is not itself evidence**. Evidence has to come from something that didn't make the claim.

`no-self-grade` is that one idea, with nothing else attached.

```python
from no_self_grade import verify, Claim, AuditResult

def do_work(feedback):
    # do the task; feedback is the previous round's audit finding, or None
    fix_the_bug()
    return Claim(ok=True, detail="fixed the parsing bug")

def audit():
    # independent, read-only check of the REAL state; never consults the claim
    result = run_the_actual_test_suite()
    return AuditResult(passed=result.all_passed, detail=result.summary)

verdict = verify(do_work, audit, max_rounds=2)
print(verdict.verified)  # True only if the audit actually agreed
```

Or wrap two existing shell commands with no code changes at all:

```bash
pip install no-self-grade

no-self-grade run \
  --claim-cmd "python agent_attempt.py" \
  --audit-cmd "python run_real_tests.py"
```

Exit code 0 only if the audit passed. On a retry round, the audit's output from the previous round is exposed to `--claim-cmd` via the `NSG_FEEDBACK` environment variable.

## Does it actually catch anything?

We built four real trials to find out, using three original scenarios (not copied from the paper) explicitly designed to make a shortcut available to a real, unscripted coding agent. Short version: **0 of 4 trials showed the agent taking the shortcut**, which is itself an interesting, honestly-reported result about where this failure mode does and doesn't show up. Full methodology, every raw artifact, and what we think it means: [**RESEARCH.md**](RESEARCH.md).

## Install

```bash
pip install no-self-grade
# or, for local development:
git clone https://github.com/aligna-solutions/no-self-grade.git
cd no-self-grade
pip install -e .
```

Requires Python 3.9+. Zero runtime dependencies.

## API

- `verify(do_work, audit, max_rounds=1) -> Verdict` — the core primitive. `do_work(feedback) -> Claim` performs the task; `audit() -> AuditResult` independently checks the real state. Retries with the audit's finding as feedback up to `max_rounds` times.
- `Claim(ok, detail="", data=None)` — what the worker says happened.
- `AuditResult(passed, detail="", data=None)` — what the independent check actually found.
- `Verdict(status, claim, audit, rounds)` — the outcome; `.verified` is `True` only if some round's audit passed.

See [`src/no_self_grade/core.py`](src/no_self_grade/core.py) for the full implementation (it's short) and [`tests/test_core.py`](tests/test_core.py) for a deterministic proof the retry-with-feedback loop and the reject-on-failed-audit behavior both work correctly.

## What this is not

It's not a replacement for LongHorizon-Harness. Their harness handles real GUI+CLI computer-use environments, multi-role model/backend assignment, and a full Manager/Executor/Auditor loop tuned against real benchmarks. This is the one structural idea underneath that (independent, authoritative verification) pulled out so it can be used on a task that has nothing to do with desktop automation: a CI pipeline, a data pipeline, a single function.

It's also not a guarantee. `verify()` is only as good as the `audit` function you give it. An audit that re-checks the wrong thing, or that isn't actually independent of `do_work`, provides no protection at all. The primitive enforces the *structure* of independent verification; it can't enforce that your specific audit function is a good one.

## Data & accuracy

Every claim in this README and in [`RESEARCH.md`](RESEARCH.md) about LongHorizon-Harness's own results is checked directly against [arXiv:2608.01964](https://arxiv.org/abs/2608.01964). Every experimental result is backed by a real audit script and its actual output, included in [`experiments/`](experiments/) so anyone can rerun it.

## License

[MIT](LICENSE).

---

<div align="center">

Built by [Aligna Solutions](https://aligna-solutions.github.io/) · one AI build shipped in public, every day

</div>
