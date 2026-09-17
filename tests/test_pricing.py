from src.pricing.black_scholes import price
from src.pricing.binomial import price as binomial_price


def test_call_price_positive():
    assert price(100, 100, 1, 0.05, 0.20, "call") > 0


def test_put_call_values_are_close_to_binomial():
    bs = price(100, 100, 1, 0.05, 0.20, "call")
    tree = binomial_price(100, 100, 1, 0.05, 0.20, "call", steps=300)
    assert abs(bs - tree) < 0.05
