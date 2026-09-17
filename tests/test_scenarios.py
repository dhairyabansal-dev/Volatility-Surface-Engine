from src.pricing.black_scholes import price
from src.risk.scenarios import option_scenario


def test_neutral_scenario_has_zero_pnl():
    result = option_scenario(100, 100, 1, 0.05, 0.20, "call")
    assert abs(result["pnl"]) < 1e-12


def test_spot_shock_changes_option_value():
    result = option_scenario(100, 100, 1, 0.05, 0.20, "call", spot_shock=0.10)
    assert result["stressed_price"] > result["base_price"]
    assert result["pnl"] > 0


def test_base_price_matches_pricer():
    result = option_scenario(100, 100, 1, 0.05, 0.20, "put")
    expected = price(100, 100, 1, 0.05, 0.20, "put")
    assert abs(result["base_price"] - expected) < 1e-12
