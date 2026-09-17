"""Cox-Ross-Rubinstein binomial option pricer."""

from math import exp, sqrt


def price(S, K, T, r, sigma, option_type, steps=100):
    if min(S, K, T, sigma) <= 0 or steps < 1:
        raise ValueError("Invalid pricing inputs")
    option_type = option_type.lower()
    dt = T / steps
    u = exp(sigma * sqrt(dt))
    d = 1 / u
    p = (exp(r * dt) - d) / (u - d)
    if not 0 <= p <= 1:
        raise ValueError("Risk-neutral probability outside [0, 1]")

    values = []
    for j in range(steps + 1):
        spot = S * u**j * d**(steps - j)
        payoff = max(spot - K, 0) if option_type == "call" else max(K - spot, 0)
        values.append(payoff)

    discount = exp(-r * dt)
    for i in range(steps - 1, -1, -1):
        values = [discount * (p * values[j + 1] + (1 - p) * values[j]) for j in range(i + 1)]
    return values[0]
