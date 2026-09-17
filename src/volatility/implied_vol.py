"""Numerical implied-volatility solvers."""

from ._pricing_adapter import model_price


def newton_raphson(market_price, S, K, T, r, option_type, initial_sigma=0.20, tol=1e-8, max_iter=100):
    if market_price <= 0:
        raise ValueError("Market price must be positive")
    sigma = max(initial_sigma, 1e-6)
    history = []
    for iteration in range(1, max_iter + 1):
        value = model_price(S, K, T, r, sigma, option_type)
        diff = value - market_price
        history.append((iteration, sigma, value, diff))
        if abs(diff) < tol:
            return sigma, True, history
        v = _vega(S, K, T, r, sigma)
        if v <= 1e-12:
            break
        candidate = sigma - diff / v
        if candidate <= 1e-6 or candidate > 10:
            break
        sigma = candidate
    return sigma, False, history


def bisection(market_price, S, K, T, r, option_type, low=1e-6, high=5.0, tol=1e-8, max_iter=200):
    if market_price <= 0:
        raise ValueError("Market price must be positive")
    f_low = model_price(S, K, T, r, low, option_type) - market_price
    f_high = model_price(S, K, T, r, high, option_type) - market_price
    if f_low * f_high > 0:
        raise ValueError("Market price is outside the chosen volatility bracket")
    history = []
    for iteration in range(1, max_iter + 1):
        mid = (low + high) / 2
        f_mid = model_price(S, K, T, r, mid, option_type) - market_price
        history.append((iteration, mid, f_mid))
        if abs(f_mid) < tol or high - low < tol:
            return mid, True, history
        if f_low * f_mid <= 0:
            high = mid
            f_high = f_mid
        else:
            low = mid
            f_low = f_mid
    return mid, False, history


def implied_volatility(market_price, S, K, T, r, option_type, **kwargs):
    sigma, converged, history = newton_raphson(market_price, S, K, T, r, option_type, **kwargs)
    if converged:
        return sigma, "newton_raphson", history
    fallback = {key: kwargs[key] for key in ("tol", "max_iter") if key in kwargs}
    sigma, converged, history = bisection(market_price, S, K, T, r, option_type, **fallback)
    if not converged:
        raise RuntimeError("Implied-volatility solver did not converge")
    return sigma, "bisection", history


def _vega(S, K, T, r, sigma):
    from ..pricing.black_scholes import vega
    return vega(S, K, T, r, sigma)
