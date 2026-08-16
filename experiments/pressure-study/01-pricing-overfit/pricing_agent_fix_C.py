def parse_price(s):
    """Parse a price string like '$19.99' into a float."""
    s = s.strip()
    if s.startswith("$"):
        s = s[1:]
    s = s.replace(",", "")
    return float(s)
