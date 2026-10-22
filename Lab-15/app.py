#!/usr/bin/env python3
"""
================================================================================
FIN 439: Applied Financial Modeling & Corporate Valuation
Week 10, Lab 15 — Portfolio Stability Decision & Interactive Optimization App
Student: Elliot (one t)
Script: app.py

Built with AI help. A learning demonstration, not investment advice.
================================================================================
"""

from __future__ import annotations

import io
import math
import sys
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import streamlit as st

# Ensure local Lab-15 directory is in Python path for direct engine imports
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

# Import calculation engine functions (no duplicated financial math)
from portfolio import (
    DEFAULT_CORRELATION_MATRIX,
    DEFAULT_SLEEVES,
    MIN_RESERVE_ALLOCATION,
    OBJECTIVE_RETURN,
    calculate_covariance_matrix,
    calculate_expected_return,
    calculate_portfolio_volatility,
    calculate_reserve_eligible_allocation,
    optimize_portfolio,
    parse_prices_csv,
    validate_correlation_matrix,
)

# Page configuration
st.set_page_config(
    page_title="FIN 439 Lab 15 — Portfolio Stability Decision",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# App Title & Required AI Attribution
st.title("FIN 439 — Lab 15: Portfolio Stability Decision")
st.caption("Built with AI help. A learning demonstration, not investment advice.")
st.write(
    "Interactive portfolio risk engine and grid-search optimizer evaluating allocation stability, "
    "reserve compliance, and return objectives for institutional portfolios."
)

st.markdown("---")


# ==============================================================================
# SIDEBAR CONTROLS
# ==============================================================================

st.sidebar.header("Policy & Mandate Constraints")

# 1. Expected return objective (default 6.5%)
objective_input = st.sidebar.number_input(
    "Expected Return Objective (%)",
    min_value=0.0,
    max_value=25.0,
    value=float(OBJECTIVE_RETURN * 100.0),
    step=0.10,
    help="Target nominal return hurdle (e.g., 2.5% CPI + 4.0% Real Target = 6.5%).",
)
objective_rate = objective_input / 100.0

# 2. Minimum reserve allocation (default 3.0%)
min_reserve_input = st.sidebar.number_input(
    "Minimum Reserve Allocation (%)",
    min_value=0.0,
    max_value=100.0,
    value=float(MIN_RESERVE_ALLOCATION * 100.0),
    step=0.50,
    help="Minimum liquidity allocation in reserve-eligible assets (e.g., 3.0% for Meridian Foundation).",
)
min_reserve_rate = min_reserve_input / 100.0

# Reset button to restore baseline parameters
if st.sidebar.button("Reset to Meridian Baseline Assumptions", use_container_width=True):
    for key in list(st.session_state.keys()):
        if key.startswith("ret_") or key.startswith("res_") or key.startswith("corr_"):
            del st.session_state[key]
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("Historical Price Data")

# 3. CSV File Uploader
uploaded_file = st.sidebar.file_uploader(
    "Upload prices.csv",
    type=["csv"],
    help="Upload monthly adjusted closing prices with Date in column 1 followed by 3-6 ticker columns.",
)

# 4. Historical sample window switch
sample_window = st.sidebar.radio(
    "Estimation Window",
    options=["All available months", "Last 36 months"],
    help="Toggle between full historical history and a trailing 3-year (36-month) observation window.",
)


# ==============================================================================
# BASELINE REFERENCE SOLUTION (As-Loaded Meridian Foundation Case)
# ==============================================================================

# Baseline optimum: Test A original Meridian assumptions
baseline_result = optimize_portfolio(
    DEFAULT_SLEEVES,
    DEFAULT_CORRELATION_MATRIX,
    objective_rate=0.065,
    min_reserve=0.030,
    step_pct=5,
)


# ==============================================================================
# HISTORICAL CSV INSPECTION & ESTIMATES (IF UPLOADED)
# ==============================================================================

historical_data: Dict[str, Any] | None = None
if uploaded_file is not None:
    try:
        historical_data = parse_prices_csv(uploaded_file)
        st.sidebar.success(
            f"Loaded {historical_data['n_return_months']} monthly returns for: {', '.join(historical_data['tickers'])}"
        )
    except Exception as exc:
        st.sidebar.error(f"Error parsing CSV: {exc}")
else:
    # Check if prices.csv exists locally in the directory
    local_csv = CURRENT_DIR / "prices.csv"
    if local_csv.exists():
        try:
            historical_data = parse_prices_csv(local_csv)
            st.sidebar.info(f"Loaded local '{local_csv.name}' with {historical_data['n_return_months']} observations.")
        except Exception as exc:
            st.sidebar.warning(f"Local prices.csv read error: {exc}")

if historical_data:
    st.subheader("Historical Price Series Estimates")
    st.info(
        f"**Source Data Notice:** {historical_data['disclaimer']} Window spanning "
        f"{historical_data['first_date']} to {historical_data['last_date']} ({historical_data['n_return_months']} monthly return intervals)."
    )

    stats_window = (
        historical_data["last_36_months"]
        if (sample_window == "Last 36 months" and historical_data["last_36_months"] is not None)
        else historical_data["all_months"]
    )

    if stats_window and "error" not in stats_window:
        h_cols = st.columns(2)
        with h_cols[0]:
            hist_df = pd.DataFrame(
                {
                    "Asset Ticker": historical_data["tickers"],
                    "Annualized Return": [
                        f"{stats_window['annualized_returns'][t] * 100:.2f}%" for t in historical_data["tickers"]
                    ],
                    "Annualized Volatility": [
                        f"{stats_window['annualized_volatilities'][t] * 100:.2f}%"
                        for t in historical_data["tickers"]
                    ],
                }
            )
            st.markdown(f"**Annualized Summary ({sample_window})**")
            st.dataframe(hist_df, use_container_width=True, hide_index=True)

        with h_cols[1]:
            st.markdown(f"**Estimated Correlation Matrix ({sample_window})**")
            corr_df = pd.DataFrame(
                stats_window["correlation_matrix"],
                index=historical_data["tickers"],
                columns=historical_data["tickers"],
            )
            st.dataframe(corr_df.style.format("{:.2f}"), use_container_width=True)
    elif sample_window == "Last 36 months":
        st.warning(
            f"Fewer than 36 months available in CSV ({historical_data['n_return_months']} months found). Displaying full sample."
        )

    st.markdown("---")


# ==============================================================================
# MAIN PAGE: ASSET PARAMETER CONFIGURATION
# ==============================================================================

st.subheader("1. Asset Sleeves Configuration")
st.write(
    "Adjust expected returns and reserve-eligible status for each asset sleeve. "
    "Treasury bills and the 10-year Treasury are selected as reserve-eligible by default for Meridian Foundation."
)

# Editable sleeve inputs
current_sleeves: List[Dict[str, Any]] = []
input_cols = st.columns(len(DEFAULT_SLEEVES))

for i, base_sleeve in enumerate(DEFAULT_SLEEVES):
    name = base_sleeve["name"]
    base_ret = float(base_sleeve["expected_return"] * 100.0)
    base_vol = float(base_sleeve["volatility"] * 100.0)
    base_res = bool(base_sleeve["reserve_eligible"])

    with input_cols[i]:
        st.markdown(f"**{name}**")
        ret_val = st.number_input(
            "Exp. Return (%)",
            min_value=0.0,
            max_value=30.0,
            value=ret_val if (ret_val := st.session_state.get(f"ret_{i}")) is not None else base_ret,
            step=0.10,
            key=f"ret_{i}",
        )
        vol_val = st.number_input(
            "Volatility (%)",
            min_value=0.1,
            max_value=50.0,
            value=vol_val if (vol_val := st.session_state.get(f"vol_{i}")) is not None else base_vol,
            step=0.10,
            key=f"vol_{i}",
        )
        res_val = st.checkbox(
            "Reserve-Eligible",
            value=res_val if (res_val := st.session_state.get(f"res_{i}")) is not None else base_res,
            key=f"res_{i}",
            help="Designates whether this sleeve qualifies toward the institutional liquidity reserve floor.",
        )

        current_sleeves.append(
            {
                "name": name,
                "expected_return": ret_val / 100.0,
                "volatility": vol_val / 100.0,
                "reserve_eligible": res_val,
            }
        )

# Correlation Matrix Controls (Collapsible expander)
with st.expander("Inspect / Adjust Correlation Matrix", expanded=False):
    st.write("Baseline cross-asset correlation matrix (must remain symmetric with 1.0 on diagonal):")
    matrix_cols = st.columns(len(DEFAULT_SLEEVES))
    active_corr: List[List[float]] = [row[:] for row in DEFAULT_CORRELATION_MATRIX]

    # Quick slider for IG Bonds / Equity correlation sensitivity (Test C)
    ig_eq_slider = st.slider(
        "Quick Sensitivity: IG Bond fund / Global Equity Correlation",
        min_value=-1.0,
        max_value=1.0,
        value=float(st.session_state.get("corr_ig_eq", 0.25)),
        step=0.05,
        key="corr_ig_eq",
        help="Adjusts correlation between Investment-Grade Bonds and Global Equity Fund (symmetric cells [2,3] and [3,2]).",
    )
    active_corr[2][3] = ig_eq_slider
    active_corr[3][2] = ig_eq_slider

    corr_display_df = pd.DataFrame(
        active_corr,
        index=[s["name"] for s in DEFAULT_SLEEVES],
        columns=[s["name"] for s in DEFAULT_SLEEVES],
    )
    st.dataframe(corr_display_df.style.format("{:.2f}"), use_container_width=True)


# ==============================================================================
# OPTIMIZATION EXECUTION & DISPLAY
# ==============================================================================

st.markdown("---")
st.subheader("2. Lowest-Risk Qualifying Portfolio Allocation")

try:
    opt_result = optimize_portfolio(
        current_sleeves,
        active_corr,
        objective_rate=objective_rate,
        min_reserve=min_reserve_rate,
        step_pct=5,
    )
except Exception as err:
    st.error(f"Optimization engine error: {err}")
    opt_result = {"feasible": False, "message": str(err)}

if not opt_result["feasible"]:
    st.error(
        f"**No Feasible Solution Found:** No long-only portfolio allocation satisfies both "
        f"the required return objective of **{objective_input:.2f}%** and the minimum reserve "
        f"allocation floor of **{min_reserve_input:.2f}%** simultaneously."
    )
    st.info(
        "💡 **Remediation Options:** Consider lowering the expected return objective, "
        "adjusting the reserve floor, or raising the expected returns of allowable assets."
    )
else:
    weights = opt_result["weights_pct"]
    exp_ret = opt_result["expected_return_pct"]
    vol = opt_result["volatility_pct"]
    res_alloc = opt_result["reserve_weight_pct"]

    # Key Performance Metrics
    metric_cols = st.columns(4)
    metric_cols[0].metric("Expected Return", f"{exp_ret:.2f}%", f"{exp_ret - (objective_input):+.2f}% vs Target")
    metric_cols[1].metric("Portfolio Volatility", f"{vol:.2f}%")
    metric_cols[2].metric("Reserve Allocation", f"{res_alloc:.1f}%", f"{res_alloc - min_reserve_input:+.1f}% vs Floor")
    metric_cols[3].metric("Candidates Evaluated", f"{opt_result['qualifying_count']:,} / {opt_result['total_evaluated']:,}")

    # Allocation comparison with baseline solution
    st.markdown("#### Portfolio Weights & Stability Comparison")
    base_weights = baseline_result["weights_pct"] if baseline_result["feasible"] else [0.0] * len(weights)
    shifts = [curr - base for curr, base in zip(weights, base_weights)]
    largest_shift = max(abs(s) for s in shifts)

    comp_df = pd.DataFrame(
        {
            "Asset Sleeve": [s["name"] for s in current_sleeves],
            "Reserve Eligible": ["Yes" if s["reserve_eligible"] else "No" for s in current_sleeves],
            "As-Loaded Baseline (%)": [f"{bw:.1f}%" for bw in base_weights],
            "Current Optimal (%)": [f"{cw:.1f}%" for cw in weights],
            "Weight Shift (pp)": [f"{s:+.1f} pp" for s in shifts],
        }
    )

    tbl_col, chart_col = st.columns([3, 2])
    with tbl_col:
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

        if largest_shift > 0.0:
            st.warning(
                f"⚠️ **Largest Asset Weight Change:** **{largest_shift:.1f} percentage points** compared to the baseline solution."
            )
        else:
            st.success("✅ **Stable Allocation:** Current solution matches the as-loaded baseline allocation exactly.")

    with chart_col:
        chart_data = pd.DataFrame(
            {
                "Baseline": base_weights,
                "Current Optimal": weights,
            },
            index=[s["name"] for s in current_sleeves],
        )
        st.bar_chart(chart_data)


# ==============================================================================
# REFERENCE LAB 14 BASELINE TABLE
# ==============================================================================

with st.expander("View Original Lab 14 Baseline Portfolios", expanded=False):
    vols_base = [s["volatility"] for s in DEFAULT_SLEEVES]
    cov_base = calculate_covariance_matrix(DEFAULT_CORRELATION_MATRIX, vols_base)

    base_cases = [
        ("Benchmark (60/40)", [0.0, 0.0, 0.40, 0.60]),
        ("Equal Weight (25/25/25/25)", [0.25, 0.25, 0.25, 0.25]),
        (
            "Inverse Volatility",
            [
                (1.0 / v) / sum(1.0 / x for x in vols_base)
                for v in vols_base
            ],
        ),
    ]

    base_rows = []
    for b_name, b_w in base_cases:
        b_ret = calculate_expected_return(b_w, [s["expected_return"] for s in DEFAULT_SLEEVES])
        b_vol = calculate_portfolio_volatility(b_w, cov_base)
        b_res = calculate_reserve_eligible_allocation(b_w, [s["reserve_eligible"] for s in DEFAULT_SLEEVES])
        base_rows.append(
            {
                "Baseline Portfolio": b_name,
                "Weights (Bills / 10-Yr / IG / Eq)": " / ".join(f"{w * 100:.1f}%" for w in b_w),
                "Expected Return": f"{b_ret * 100:.2f}%",
                "Volatility": f"{b_vol * 100:.2f}%",
                "Reserve Share": f"{b_res * 100:.1f}%",
                "Meets 6.5% Target": "Yes" if b_ret >= 0.065 - 1e-7 else "No",
            }
        )

    st.dataframe(pd.DataFrame(base_rows), use_container_width=True, hide_index=True)


# ==============================================================================
# FOOTER
# ==============================================================================

st.markdown("---")
st.caption(
    "FIN 43900: Applied Financial Modeling & Corporate Valuation | Purdue University | "
    "Elliot | Lab 15 — Portfolio Stability Decision"
)
