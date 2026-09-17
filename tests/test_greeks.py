from src.greeks.greeks import all_greeks


def test_greeks_return_expected_keys():
    result = all_greeks(100, 100, 1, 0.05, 0.20, "call")
    assert set(result) == {"delta", "gamma", "vega", "theta", "rho"}
    assert 0 < result["delta"] < 1
    assert result["gamma"] > 0
    assert result["vega"] > 0
