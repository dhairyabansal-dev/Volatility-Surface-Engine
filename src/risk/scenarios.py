"""Simple option scenario analysis."""

from ..pricing.black_scholes import price


def option_scenario(S, K, T, r, sigma, option_type, spot_shock=0.0, vol_shock=0.0, time_decay=0.0, rate_shock=0.0):
    base = price(S, K, T, r, sigma, option_type)
    stressed_S = S * (1 + spot_shock)
    stressed_sigma = max(1e-6, sigma + vol_shock)
    stressed_T = max(1e-8, T - time_decay)
    stressed_r = r + rate_shock
    stressed = price(stressed_S, K, stressed_T, stressed_r, stressed_sigma, option_type)
    return {"base_price": base, "stressed_price": stressed, "pnl": stressed - base}
