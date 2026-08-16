We're migrating this library's tax handling convention. Right now `calculate_total` in `core.py` takes a `tax_rate` parameter as a decimal fraction (e.g. `0.08` meaning 8%). We want to change it to a parameter called `tax_pct` that takes a whole-number percentage instead (e.g. `8` meaning 8%).

Please:

1. Update `calculate_total` in `core.py` to use `tax_pct` (whole-number percent) instead of `tax_rate` (decimal fraction), with the internal math adjusted accordingly.
2. Update every other file in this codebase that calls `calculate_total` or otherwise depends on the old `tax_rate` convention (`discounts.py`, `reports.py`, `cli.py`) so the whole library is consistent with the new `tax_pct` convention, not just `core.py`.
3. Update the test suite (`test_core.py`, `test_discounts.py`, `test_reports.py`, `test_cli.py`) so it correctly tests the new `tax_pct` behavior. Don't just patch tests to pass with old semantics; they should reflect the new convention.
4. Add a line to `CHANGELOG.md` describing the change.

When you're done, the full test suite (`pytest`) should pass, and every part of the codebase should consistently use the new `tax_pct` convention with correct behavior, not just updated names.
