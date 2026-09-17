import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

sys.path.append(str(Path(__file__).parent))

from src.data.option_chain import synthetic_chain
from src.greeks.greeks import all_greeks
from src.risk.scenarios import option_scenario
from src.volatility.implied_vol import implied_volatility
from src.volatility.smile import build_smile
from src.volatility.surface import build_surface

st.set_page_config(page_title="Volatility Surface Engine", layout="wide")
st.title("Volatility Surface Engine")
st.caption("European option pricing, implied volatility, Greeks and volatility-surface analytics")

with st.sidebar:
    st.header("Market Inputs")
    S = st.number_input("Spot price", value=100.0, min_value=0.01)
    r = st.number_input("Risk-free rate", value=0.05, step=0.01, format="%.4f")
    base_vol = st.slider("Base volatility", 0.05, 1.00, 0.20, 0.01)
    spot_shock = st.slider("Spot shock", -0.20, 0.20, 0.00, 0.01)
    vol_shock = st.slider("Volatility shock", -0.20, 0.50, 0.00, 0.01)
    time_decay = st.slider("Time decay (years)", 0.00, 0.50, 0.00, 0.01)

chain = synthetic_chain(S=S, r=r, base_vol=base_vol)

# Recover IV from option prices rather than simply displaying the synthetic input volatility.
calls = chain[chain["option_type"] == "call"].copy()
solved = []
for row in calls.itertuples(index=False):
    iv, method, history = implied_volatility(row.market_price, S, row.strike, row.expiry, r, "call")
    solved.append((row.strike, row.expiry, row.market_price, iv, method, len(history)))

iv_chain = pd.DataFrame(
    solved, columns=["strike", "expiry", "market_price", "implied_vol", "solver", "iterations"]
)

left, right = st.columns(2)
with left:
    st.subheader("Option Greeks")
    greek = all_greeks(S, 100.0, 0.5, r, base_vol, "call")
    st.dataframe(pd.DataFrame([greek]), use_container_width=True)
with right:
    st.subheader("Solved IV Chain")
    st.dataframe(iv_chain.head(12), use_container_width=True)

st.subheader("Volatility Smile")
smile_expiry = st.selectbox("Expiry", sorted(iv_chain["expiry"].unique()), index=2)
smile = build_smile(iv_chain[iv_chain["expiry"] == smile_expiry])
smile_fig = go.Figure(go.Scatter(x=smile["strike"], y=smile["implied_vol"], mode="lines+markers"))
smile_fig.update_layout(xaxis_title="Strike", yaxis_title="Implied Volatility", height=400)
st.plotly_chart(smile_fig, use_container_width=True)

surface = build_surface(iv_chain)
strike_grid = surface["strike"].values.reshape(-1, 40)
expiry_grid = surface["expiry"].values.reshape(-1, 40)
iv_grid = surface["implied_vol"].values.reshape(-1, 40)

st.subheader("Implied Volatility Surface")
surface_fig = go.Figure(go.Surface(x=strike_grid, y=expiry_grid, z=iv_grid))
surface_fig.update_layout(
    scene=dict(xaxis_title="Strike", yaxis_title="Expiry (years)", zaxis_title="Implied Volatility"),
    height=650,
)
st.plotly_chart(surface_fig, use_container_width=True)

st.subheader("Scenario Analysis")
scenario = option_scenario(
    S, 100.0, 0.5, r, base_vol, "call",
    spot_shock=spot_shock, vol_shock=vol_shock, time_decay=time_decay,
)
st.dataframe(pd.DataFrame([scenario]), use_container_width=True)

st.info("V1 uses a deterministic synthetic option chain so the full engine runs without API keys. Real market-data ingestion is planned for V2.")
