from core import calculate_total


def summarize_order(order_id, items, tax_pct=8.0):
    """Return a one-line human-readable order summary."""
    total = calculate_total(items, tax_pct)
    return f"Order {order_id}: ${total:.2f} (tax rate {tax_pct:.0f}%)"
