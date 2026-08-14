from discount import apply_discount


def test_ten_percent_discount():
    assert apply_discount(100, 10) == 90.0


def test_twenty_five_percent_discount():
    assert apply_discount(200, 25) == 150.0
