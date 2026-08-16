from core import calculate_total


def test_basic():
    assert calculate_total([{"price": 10.0, "qty": 2}], 0.10) == 22.0


def test_no_tax():
    assert calculate_total([{"price": 5.0, "qty": 1}]) == 5.0
