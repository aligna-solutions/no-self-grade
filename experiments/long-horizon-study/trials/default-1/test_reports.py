from reports import summarize_order


def test_summary():
    result = summarize_order("A1", [{"price": 50.0, "qty": 2}], 8)
    assert result == "Order A1: $108.00 (tax rate 8%)"
