"""Volatility surface utilities."""

import numpy as np
import pandas as pd
from scipy.interpolate import griddata


def build_surface(df, strike_col="strike", expiry_col="expiry", iv_col="implied_vol", strikes=40, expiries=30):
    required = {strike_col, expiry_col, iv_col}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    clean = df[[strike_col, expiry_col, iv_col]].dropna()
    x = np.linspace(clean[strike_col].min(), clean[strike_col].max(), strikes)
    y = np.linspace(clean[expiry_col].min(), clean[expiry_col].max(), expiries)
    xx, yy = np.meshgrid(x, y)
    zz = griddata((clean[strike_col], clean[expiry_col]), clean[iv_col], (xx, yy), method="linear")
    return pd.DataFrame({"strike": xx.ravel(), "expiry": yy.ravel(), "implied_vol": zz.ravel()})
