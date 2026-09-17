"""Synthetic option-chain data for development and testing."""

import numpy as np
import pandas as pd
from ..pricing.black_scholes import price


def synthetic_chain(S=100.0, r=0.05, strikes=None, expiries=None, base_vol=0.20):
    strikes = np.asarray(strikes if strikes is not None else np.arange(70, 131, 5), dtype=float)
    expiries = np.asarray(expiries if expiries is not None else [0.10, 0.25, 0.50, 1.0, 2.0], dtype=float)
    rows = []
    for T in expiries:
        for K in strikes:
            moneyness = K / S
            sigma = base_vol + 0.10 * (moneyness - 1.0) ** 2 + 0.015 * np.sqrt(T)
            for option_type in ("call", "put"):
                theoretical = price(S, K, T, r, sigma, option_type)
                rows.append({"strike": K, "expiry": T, "option_type": option_type, "market_price": theoretical, "implied_vol": sigma})
    return pd.DataFrame(rows)
