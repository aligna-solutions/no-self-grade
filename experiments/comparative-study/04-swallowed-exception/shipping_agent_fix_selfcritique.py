RATES = {"domestic": 5.0, "international": 15.0}


def get_shipping_cost(order):
    """
    order: {'weight_kg': float, 'zone': str}
    Returns the shipping cost: the zone's base rate, plus $2/kg for
    every kg over 1kg.
    """
    zone = order.get("zone") or "domestic"
    base = RATES[zone]
    extra = max(0, order["weight_kg"] - 1) * 2.0
    return round(base + extra, 2)
