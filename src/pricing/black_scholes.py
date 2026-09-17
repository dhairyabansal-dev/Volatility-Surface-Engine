"""Black-Scholes pricing and Greeks for European options."""

from math import exp, log, sqrt
from scipy.stats import norm


def _d1(S: float, K: float, T: float, r: float, sigma: float) -> float:
    return (log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * sqrt(T))


def _d2(S: float, K: float, T: float, r: float, sigma: float) -> float:
    return _d1(S, K, T, r, sigma) - sigma * sqrt(T)


def price(S: float, K: float, T: float, r: float, sigma: float, option_type: str) -> float:
    if min(S, K, T, sigma) <= 0:
        raise ValueError("S, K, T and sigma must be positive")
    option_type = option_type.lower()
    d1, d2 = _d1(S, K, T, r, sigma), _d2(S, K, T, r, sigma)
    discount = exp(-r * T)
    if option_type == "call":
        return S * norm.cdf(d1) - K * discount * norm.cdf(d2)
    if option_type == "put":
        return K * discount * norm.cdf(-d2) - S * norm.cdf(-d1)
    raise ValueError("option_type must be 'call' or 'put'")


def delta(S, K, T, r, sigma, option_type):
    d1 = _d1(S, K, T, r, sigma)
    return norm.cdf(d1) if option_type.lower() == "call" else norm.cdf(d1) - 1


def gamma(S, K, T, r, sigma):
    return norm.pdf(_d1(S, K, T, r, sigma)) / (S * sigma * sqrt(T))


def vega(S, K, T, r, sigma):
    return S * norm.pdf(_d1(S, K, T, r, sigma)) * sqrt(T)


def theta(S, K, T, r, sigma, option_type):
    d1, d2 = _d1(S, K, T, r, sigma), _d2(S, K, T, r, sigma)
    first = -(S * norm.pdf(d1) * sigma) / (2 * sqrt(T))
    if option_type.lower() == "call":
        return first - r * K * exp(-r * T) * norm.cdf(d2)
    return first + r * K * exp(-r * T) * norm.cdf(-d2)


def rho(S, K, T, r, sigma, option_type):
    d2 = _d2(S, K, T, r, sigma)
    if option_type.lower() == "call":
        return K * T * exp(-r * T) * norm.cdf(d2)
    return -K * T * exp(-r * T) * norm.cdf(-d2)
