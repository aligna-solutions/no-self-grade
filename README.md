<div align="center">

# no-self-grade

**Don't let a self-reported "done" count until an independent, read-only check confirms it.**

A minimal, framework-agnostic generalization of the Auditor pattern from [LongHorizon-Harness](https://arxiv.org/abs/2608.01964) (DreamX Team, Alibaba, arXiv:2608.01964): a fresh-context, independent check that runs after a worker claims completion, and whose verdict is authoritative. LongHorizon-Harness builds that check into one specific harness tied to particular coding-agent tooling and GUI+CLI computer-use tasks. This strips it down to a 15-line core function so it can wrap any task, any agent, any language runtime.

[![Tests](https://img.shields.io/badge/tests-passing-1f6e4a?style=flat-square)](tests/)
[![License: MIT](https://img.shields.io/badge/license-MIT-3d5a80?style=flat-square)](LICENSE)
[![Dependencies: none](https://img.shields.io/badge/dependencies-none-a3271f?style=flat-square)](pyproject.toml)
[![Aligna Builds](https://img.shields.io/badge/Aligna%20Builds-no--self--grade-1a1a17?style=flat-square)](https://aligna-solutions.github.io/)

[**Raw experiments →**](experiments/) · [**Comparative study →**](experiments/comparative-study/methods.md) · [**Pressure study →**](experiments/pressure-study/methods.md) · [**Long-horizon study →**](experiments/long-horizon-study/methods.md) · [**GUI study →**](experiments/gui-study/methods.md)

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

Five real studies, 43 trials total, 0 fake-completion shortcuts observed:

- **The original pilot** (4 trials, 3 scenarios): does the paper's fake-completion pattern show up on short, single-shot coding tasks with a strong model? It didn't, in any of the 4 trials. Raw scenarios and audit scripts: [`experiments/`](experiments/).
- **The comparative study** (18 trials, 5 scenarios, a weaker-backbone probe): does independent audit actually catch more than same-context self-critique or bare-signal reflection do? In this sample, no: all three methods caught the one real gap that came up, equally well. Full methodology: [`experiments/comparative-study/methods.md`](experiments/comparative-study/methods.md).
- **The pressure study** (9 trials, 3 scenarios): does a real deadline or self-interest framing (never an instruction to lie) push any method toward a shortcut? All 9 trials still passed independent audit. Full methodology: [`experiments/pressure-study/methods.md`](experiments/pressure-study/methods.md).
- **The long-horizon study** (4 trials, 1 scenario, 9 files, a weaker backbone): does the finding hold on a bigger, more error-prone task than any prior scenario, with Haiku instead of the default model? All 4 trials still passed independent audit; the GUI-heavy axis remained genuinely untested. Full methodology: [`experiments/long-horizon-study/methods.md`](experiments/long-horizon-study/methods.md).
- **The GUI study** (8 trials, 1 scenario, a real rendered page, 161+ real logged actions per trial): with no computer-use tool available in this environment, one was built (a Playwright-driven harness). All 4 unscripted trials passed independent audit, and a follow-up A vs B vs C comparison (independent audit, self-critique, bare-signal reflection) tied 6/6 on the same GUI task. Full methodology: [`experiments/gui-study/methods.md`](experiments/gui-study/methods.md).

The clearer result across all five: the specific failure mode the paper documents is harder to elicit outside its own long-horizon, GUI-heavy regime than a first read suggests, and that holds even now that the GUI axis has an actual first test rather than a stated gap.

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

Every claim in this README about LongHorizon-Harness's own results is checked directly against [arXiv:2608.01964](https://arxiv.org/abs/2608.01964). Every experimental result is backed by a real audit script and its actual output, included in [`experiments/`](experiments/) so anyone can rerun it.

## License

[MIT](LICENSE).
