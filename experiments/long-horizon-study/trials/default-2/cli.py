from core import calculate_total

DEFAULT_TAX_PCT = 7.25


def run(items):
    """Entry point used by the command-line tool. Applies the store's default tax rate."""
    return calculate_total(items, DEFAULT_TAX_PCT)
