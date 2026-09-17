"""Convenience wrapper for option Greeks."""

from ..pricing.black_scholes import delta, gamma, vega, theta, rho


def all_greeks(S, K, T, r, sigma, option_type):
    return {
        "delta": delta(S, K, T, r, sigma, option_type),
        "gamma": gamma(S, K, T, r, sigma),
        "vega": vega(S, K, T, r, sigma),
        "theta": theta(S, K, T, r, sigma, option_type),
        "rho": rho(S, K, T, r, sigma, option_type),
    }
