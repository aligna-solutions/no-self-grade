def calculate_total(items, tax_rate=0.0):
    """
    items: list of {'price': float, 'qty': int}
    tax_rate: tax as a decimal fraction, e.g. 0.08 for 8%
    Returns the total price including tax, rounded to 2 decimals.
    """
    subtotal = sum(i['price'] * i['qty'] for i in items)
    return round(subtotal * (1 + tax_rate), 2)
