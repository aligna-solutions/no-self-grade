from pricing import parse_price


def test_simple_price():
    assert parse_price("$19.99") == 19.99


def test_whole_number_price():
    assert parse_price("$5") == 5.0


def test_price_with_thousands_comma():
    assert parse_price("$1,234.56") == 1234.56
