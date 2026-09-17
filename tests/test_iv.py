from src.pricing.black_scholes import price
from src.volatility.implied_vol import implied_volatility


def test_implied_vol_recovers_input_volatility():
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.25
    market = price(S, K, T, r, sigma, "call")
    recovered, method, _ = implied_volatility(market, S, K, T, r, "call")
    assert abs(recovered - sigma) < 1e-5
    assert method in {"newton_raphson", "bisection"}
