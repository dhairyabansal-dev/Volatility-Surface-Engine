import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.append(str(Path(__file__).parent))

from src.data.option_chain import synthetic_chain
from src.greeks.greeks import all_greeks
from src.volatility.surface import build_surface

st.set_page_config(page_title="Volatility Surface Engine", layout="wide")
st.title("Volatility Surface Engine")
st.caption("Option pricing, implied volatility, Greeks and surface analytics")

with st.sidebar:
    S = st.number_input("Spot price", value=100.0, min_value=0.01)
    r = st.number_input("Risk-free rate", value=0.05, step=0.01, format="%.4f")
    base_vol = st.slider("Base volatility", 0.05, 1.00, 0.20, 0.01)

chain = synthetic_chain(S=S, r=r, base_vol=base_vol)

left, right = st.columns(2)
with left:
    st.subheader("Option Greeks")
    greek = all_greeks(S, 100.0, 0.5, r, base_vol, "call")
    st.dataframe(greek, use_container_width=True)
with right:
    st.subheader("Synthetic Chain")
    st.dataframe(chain.head(12), use_container_width=True)

surface_input = chain[chain["option_type"] == "call"]
surface = build_surface(surface_input)

st.subheader("Implied Volatility Surface")
fig = go.Figure(data=[go.Surface(x=surface["strike"].values.reshape(-1, 40), y=surface["expiry"].values.reshape(-1, 40), z=surface["implied_vol"].values.reshape(-1, 40))])
fig.update_layout(scene=dict(xaxis_title="Strike", yaxis_title="Expiry (years)", zaxis_title="Implied Volatility"), height=650)
st.plotly_chart(fig, use_container_width=True)

st.info("V1 uses a synthetic option chain. Market-data ingestion and historical surface analysis are planned for V2.")
