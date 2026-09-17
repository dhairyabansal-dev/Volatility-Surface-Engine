"""Input validation helpers."""


def validate_option_inputs(S, K, T, r, sigma=None):
    if S <= 0 or K <= 0 or T <= 0:
        raise ValueError("Spot, strike and time-to-expiry must be positive")
    if sigma is not None and sigma <= 0:
        raise ValueError("Volatility must be positive")
    if not isinstance(r, (int, float)):
        raise TypeError("Risk-free rate must be numeric")
    return True
