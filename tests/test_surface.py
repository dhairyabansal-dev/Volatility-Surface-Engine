from src.data.option_chain import synthetic_chain
from src.volatility.surface import build_surface


def test_surface_has_expected_columns_and_rows():
    df = synthetic_chain()
    calls = df[df["option_type"] == "call"]
    surface = build_surface(calls, strikes=10, expiries=8)
    assert list(surface.columns) == ["strike", "expiry", "implied_vol"]
    assert len(surface) == 80
