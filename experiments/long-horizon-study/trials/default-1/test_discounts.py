from discounts import total_with_discount


def test_discount():
    assert total_with_discount([{"price": 100.0, "qty": 1}], 8, 10) == 97.2
