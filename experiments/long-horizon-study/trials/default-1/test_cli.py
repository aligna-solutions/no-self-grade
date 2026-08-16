from cli import run


def test_cli_run():
    assert run([{"price": 20.0, "qty": 1}]) == 21.45
