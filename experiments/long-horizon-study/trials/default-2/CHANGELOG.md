# Changelog

## Unreleased
- `calculate_total` now takes `tax_pct` (whole-number percentage, e.g. `8` for 8%) instead of `tax_rate` (decimal fraction, e.g. `0.08`). `discounts.py`, `reports.py`, and `cli.py` have been updated to the new convention.
