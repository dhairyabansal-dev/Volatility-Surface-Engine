"""Volatility smile construction."""

import pandas as pd


def build_smile(df, strike_col="strike", iv_col="implied_vol"):
    required = {strike_col, iv_col}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    return df[[strike_col, iv_col]].dropna().sort_values(strike_col).reset_index(drop=True)
