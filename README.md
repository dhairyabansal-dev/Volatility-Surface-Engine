# Volatility Surface Engine

A modular quantitative-finance engine for European option pricing, implied volatility, Greeks, volatility smiles, volatility surfaces, and scenario analysis.

## What it does

The project turns option-chain prices into a research-ready volatility surface:

```text
Option Chain
     ↓
Validation
     ↓
Black-Scholes / Binomial Pricing
     ↓
Implied Volatility
     ↓
Greeks
     ↓
Volatility Smile
     ↓
Volatility Surface
     ↓
Scenario Analysis
     ↓
Interactive Dashboard
```

## V1 — Complete

### Pricing
- Black-Scholes European call and put pricing
- Cox-Ross-Rubinstein binomial pricing
- Black-Scholes vs. binomial consistency test

### Implied Volatility
- Newton-Raphson solver
- Bisection fallback
- Convergence history / diagnostics
- Input and bracket validation

The IV engine solves:

```text
Model Price(S, K, T, r, σ) = Market Price
```

### Greeks
- Delta
- Gamma
- Vega
- Theta
- Rho

### Volatility Analytics
- Synthetic option-chain generation
- Volatility smile construction
- Strike × expiry volatility-surface interpolation
- 3D Plotly surface visualization

### Risk
- Spot-price shocks
- Volatility shocks
- Time decay
- Interest-rate shocks
- Option-level stressed P&L

### Dashboard
The Streamlit application provides:
- Adjustable market inputs
- Recovered implied-volatility chain
- Solver and iteration diagnostics
- Volatility smile chart
- 3D implied-volatility surface
- Interactive scenario analysis

V1 deliberately uses deterministic synthetic option data so the entire engine can run without API keys or external market-data dependencies.

## Project Structure

```text
Volatility-Surface-Engine/
├── src/
│   ├── pricing/
│   │   ├── black_scholes.py
│   │   └── binomial.py
│   ├── volatility/
│   │   ├── _pricing_adapter.py
│   │   ├── implied_vol.py
│   │   ├── smile.py
│   │   └── surface.py
│   ├── greeks/
│   │   └── greeks.py
│   ├── data/
│   │   └── option_chain.py
│   ├── risk/
│   │   └── scenarios.py
│   └── utils/
│       └── validation.py
├── tests/
│   ├── test_pricing.py
│   ├── test_iv.py
│   ├── test_greeks.py
│   ├── test_surface.py
│   └── test_scenarios.py
├── app.py
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/dhairyabansal-dev/Volatility-Surface-Engine.git
cd Volatility-Surface-Engine
pip install -r requirements.txt
```

## Run the dashboard

```bash
streamlit run app.py
```

## Run tests

```bash
pytest
```

## Mathematical Foundation

V1 is built around the Black-Scholes model for European options. The numerical layer uses root-finding to invert the pricing function and recover implied volatility. The surface layer then organizes implied volatility across strike and maturity dimensions.

The project intentionally separates pricing, numerical solving, volatility analytics, Greeks, data generation, and risk scenarios so each component can be tested independently.

## V1 Status

**Complete:** pricing → IV solving → Greeks → smile → surface → scenarios → dashboard → tests.

## Roadmap

### V2 — Market Data
- Real option-chain ingestion
- Historical option-chain storage
- IV term structure
- Surface time series
- Portfolio-level P&L scenarios
- Persistent research results

### V3 — Advanced Volatility Research
- Advanced interpolation/extrapolation
- Calendar-spread consistency diagnostics
- Vertical-spread consistency diagnostics
- Surface discontinuity detection
- Abnormal IV detection
- Research-oriented surface arbitrage diagnostics

## Disclaimer

This repository is intended for quantitative-finance research and education. It is not investment advice and does not provide automated trading signals.
