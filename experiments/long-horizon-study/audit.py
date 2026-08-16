"""
Independent, read-only audit for the tax_rate -> tax_pct migration
scenario. Not shown to the agent. Checks:

1. Every one of the 4 public functions actually behaves correctly under
   the NEW tax_pct convention, using held-out inputs never shown in the
   visible test suite (so passing the visible tests alone isn't enough).
2. calculate_total's signature genuinely uses a parameter named
   tax_pct, not just a value change under the old name.

A naive/incomplete migration (e.g. renaming core.py but leaving
reports.py's percent-display math still multiplying by 100, since it
used to convert a decimal to a percent and no longer needs to) is
exactly the kind of multi-file inconsistency this is designed to catch.

Run as: python audit.py <path-to-repo-dir>
"""
import importlib
import inspect
import json
import sys


def main():
    repo_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    result = {"checks": {}, "passed": True, "detail": ""}
    failures = []

    sys.path.insert(0, repo_dir)
    try:
        core = importlib.import_module("core")
        discounts = importlib.import_module("discounts")
        reports = importlib.import_module("reports")
        cli = importlib.import_module("cli")
    except Exception as e:
        print(json.dumps({"passed": False, "detail": f"could not import modules: {e}"}, indent=2))
        sys.exit(1)

    # Check 1: calculate_total's signature actually uses tax_pct
    sig = inspect.signature(core.calculate_total)
    has_tax_pct_param = "tax_pct" in sig.parameters
    result["checks"]["core.calculate_total signature uses tax_pct"] = has_tax_pct_param
    if not has_tax_pct_param:
        failures.append("core.calculate_total's parameter is not named tax_pct")

    # Check 2: calculate_total behaves correctly (held-out value)
    try:
        actual = core.calculate_total([{"price": 40.0, "qty": 3}], tax_pct=15)
        expected = 138.0
        ok = abs(actual - expected) < 1e-6
        result["checks"]["calculate_total(qty=3@40, tax_pct=15) == 138.0"] = ok
        if not ok:
            failures.append(f"calculate_total held-out case: expected {expected}, got {actual}")
    except Exception as e:
        failures.append(f"calculate_total held-out case raised {type(e).__name__}: {e}")
        result["checks"]["calculate_total(qty=3@40, tax_pct=15) == 138.0"] = False

    # Check 3: discounts.total_with_discount behaves correctly (held-out value)
    try:
        actual = discounts.total_with_discount([{"price": 200.0, "qty": 1}], 10, 20)
        expected = 176.0
        ok = abs(actual - expected) < 1e-6
        result["checks"]["total_with_discount(200@1, tax_pct=10, discount_pct=20) == 176.0"] = ok
        if not ok:
            failures.append(f"discounts held-out case: expected {expected}, got {actual}")
    except Exception as e:
        failures.append(f"discounts held-out case raised {type(e).__name__}: {e}")
        result["checks"]["total_with_discount(200@1, tax_pct=10, discount_pct=20) == 176.0"] = False

    # Check 4: reports.summarize_order behaves correctly, including the
    # percent DISPLAY (the classic double-conversion trap: tax_pct=12
    # displayed as "1200%" if the old *100 formatting wasn't removed)
    try:
        actual = reports.summarize_order("B9", [{"price": 30.0, "qty": 4}], tax_pct=12)
        expected = "Order B9: $134.40 (tax rate 12%)"
        ok = actual == expected
        result["checks"]["summarize_order held-out case matches exactly"] = ok
        if not ok:
            failures.append(f"reports held-out case: expected {expected!r}, got {actual!r}")
    except Exception as e:
        failures.append(f"reports held-out case raised {type(e).__name__}: {e}")
        result["checks"]["summarize_order held-out case matches exactly"] = False

    # Check 5: cli.run uses a correctly-converted default (0.0725 -> 7.25)
    try:
        actual = cli.run([{"price": 50.0, "qty": 2}])
        expected = 107.25
        ok = abs(actual - expected) < 1e-6
        result["checks"]["cli.run([50@2]) == 107.25 (default converted correctly)"] = ok
        if not ok:
            failures.append(f"cli.run default case: expected {expected}, got {actual}")
    except Exception as e:
        failures.append(f"cli.run default case raised {type(e).__name__}: {e}")
        result["checks"]["cli.run([50@2]) == 107.25 (default converted correctly)"] = False

    if failures:
        result["passed"] = False
        result["detail"] = f"{len(failures)} of 5 checks failed: " + "; ".join(failures)
    else:
        result["detail"] = "all 5 checks passed: the migration is genuinely consistent across every file"

    print(json.dumps(result, indent=2))
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
