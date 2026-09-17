from ..pricing.black_scholes import price


def model_price(S, K, T, r, sigma, option_type):
    return price(S, K, T, r, sigma, option_type)
