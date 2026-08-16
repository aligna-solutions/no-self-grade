from core import calculate_total


def total_with_discount(items, tax_rate, discount_pct):
    """Apply tax, then a percentage discount off the taxed total."""
    total = calculate_total(items, tax_rate)
    return round(total * (1 - discount_pct / 100), 2)
