# Volatility Surface Engine

A quantitative finance engine for option pricing, implied volatility, Greeks, volatility smiles, and volatility surfaces.

## Pipeline

```text
Option Chain Data
       ↓
Validation & Cleaning
       ↓
Black-Scholes / Binomial Pricing
       ↓
Implied Volatility Solver
       ↓
Greeks Engine
       ↓
Volatility Smile
       ↓
Volatility Surface
       ↓
Scenario Analysis
       ↓
Streamlit Dashboard
```

## V1 Scope

- Black-Scholes European option pricing
- Binomial European option pricing
- Newton-Raphson implied-volatility solver
- Bisection fallback solver
- IV convergence diagnostics
- Delta, Gamma, Vega, Theta and Rho
- Synthetic option-chain generation for research
- Volatility smile construction
- Volatility surface construction across strikes and expiries
- Basic scenario analysis
- Streamlit visualization

## Project Structure

```text
src/
├── pricing/
│   ├── black_scholes.py
│   └── binomial.py
├── volatility/
│   ├── implied_vol.py
│   ├── smile.py
│   └── surface.py
├── greeks/
│   └── greeks.py
├── data/
│   └── option_chain.py
├── risk/
│   └── scenarios.py
└── utils/
    └── validation.py

tests/
├── test_pricing.py
├── test_iv.py
├── test_greeks.py
└── test_surface.py

app.py
requirements.txt
```

## Mathematical Core

The engine uses the Black-Scholes framework for European options. Implied volatility is obtained numerically by solving:

`ModelPrice(S, K, T, r, σ) = MarketPrice`

Newton-Raphson is used as the primary solver, with bisection as a robust fallback when the Newton iteration does not converge.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Run tests with:

```bash
pytest
```

## Roadmap

### V2
- Historical option-chain ingestion
- IV term structure
- Surface dynamics
- Portfolio P&L scenarios
- Volatility and underlying shocks
- Persistent research results

### V3
- Calendar and vertical-spread consistency diagnostics
- Surface arbitrage diagnostics
- Abnormal IV detection
- Surface discontinuity analysis
- Advanced interpolation/extrapolation

This project is intended for quantitative research and education, not automated trading or investment advice.
