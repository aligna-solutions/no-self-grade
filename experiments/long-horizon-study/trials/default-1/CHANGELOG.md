# Changelog

## Unreleased
- `calculate_total` (and everything built on it — `discounts.py`, `reports.py`, `cli.py`) now takes `tax_pct` as a whole-number percentage (e.g. `8` for 8%) instead of `tax_rate` as a decimal fraction (e.g. `0.08`). Update any callers still passing decimal fractions.
