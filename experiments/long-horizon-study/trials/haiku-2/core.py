def calculate_total(items, tax_pct=0.0):
    """
    items: list of {'price': float, 'qty': int}
    tax_pct: tax as a whole-number percent, e.g. 8 for 8%
    Returns the total price including tax, rounded to 2 decimals.
    """
    subtotal = sum(i['price'] * i['qty'] for i in items)
    return round(subtotal * (1 + tax_pct / 100), 2)
