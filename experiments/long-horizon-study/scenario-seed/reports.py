from core import calculate_total


def summarize_order(order_id, items, tax_rate=0.08):
    """Return a one-line human-readable order summary."""
    total = calculate_total(items, tax_rate)
    return f"Order {order_id}: ${total:.2f} (tax rate {tax_rate * 100:.0f}%)"
