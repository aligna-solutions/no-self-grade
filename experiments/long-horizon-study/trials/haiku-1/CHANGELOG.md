# Changelog

## Unreleased
- Migrate tax handling from decimal fraction (`tax_rate`) to whole-number percentage (`tax_pct`): `calculate_total()` now takes `tax_pct` as a whole number (e.g. 8 for 8%) instead of decimal fraction (e.g. 0.08). All dependent code and tests updated accordingly.
