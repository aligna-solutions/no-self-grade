"""
Command-line wrapper: turn any two shell commands into a verified claim.

    no-self-grade run \\
      --claim-cmd "python agent_attempt.py" \\
      --audit-cmd "python check_real_state.py"

`--claim-cmd` is whatever your agent runs to do the work and report success
(its own exit code is recorded but never trusted on its own). `--audit-cmd`
is a separate, independent, read-only command that checks the real state
afterward — re-running the actual test suite, re-parsing an output file,
diffing against a known-good fixture. Exit code 0 means the audit passed.

On a retry round, the audit's stdout/stderr from the previous round is
exposed to `--claim-cmd` via the NSG_FEEDBACK environment variable, so a
claim command that wants to use it can.
"""

import argparse
import json
import os
import subprocess
import sys

from .core import AuditResult, Claim, verify


def _run(cmd: str, env: dict) -> tuple[int, str]:
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="no-self-grade",
        description="Don't let a self-reported 'done' count until an independent check confirms it.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run", help="wrap a claim command with an independent audit command")
    run_p.add_argument("--claim-cmd", required=True, help="shell command that does the work and reports success via exit code")
    run_p.add_argument("--audit-cmd", required=True, help="independent, read-only shell command; exit 0 means the claim is confirmed")
    run_p.add_argument("--max-rounds", type=int, default=1, help="retry the claim command this many times if the audit fails (default 1, no retry)")
    run_p.add_argument("--report", default=None, help="write a JSON report to this path in addition to stdout")

    args = parser.parse_args(argv)

    if args.command == "run":
        base_env = dict(os.environ)

        def do_work(feedback):
            env = dict(base_env)
            if feedback:
                env["NSG_FEEDBACK"] = feedback
            code, out = _run(args.claim_cmd, env)
            return Claim(ok=(code == 0), detail=out)

        def audit():
            code, out = _run(args.audit_cmd, base_env)
            return AuditResult(passed=(code == 0), detail=out)

        verdict = verify(do_work, audit, max_rounds=args.max_rounds)

        report = {
            "verdict": verdict.status,
            "rounds": verdict.rounds,
            "claim": {"ok": verdict.claim.ok, "detail": verdict.claim.detail},
            "audit": {"passed": verdict.audit.passed, "detail": verdict.audit.detail},
        }
        text = json.dumps(report, indent=2)
        print(text)
        if args.report:
            with open(args.report, "w", encoding="utf-8") as f:
                f.write(text)
        return 0 if verdict.verified else 1

    return 2


if __name__ == "__main__":
    sys.exit(main())
