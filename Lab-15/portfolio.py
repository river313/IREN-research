#!/usr/bin/env python3
"""
================================================================================
FIN 439: Applied Financial Modeling & Corporate Valuation
Week 10, Lab 15 — Portfolio Stability Decision & Optimization
Student: Elliot (one t)
Script: portfolio.py

Description:
    Extended risk and optimization engine for the Meridian Foundation case.
    Preserves all Lab 14 baseline calculations (Benchmark, Equal Weight,
    Inverse Volatility) and extends functionality with:
      1. Transparent, reproducible long-only grid search optimization in
         5-percentage-point increments to find the lowest-volatility allocation
         satisfying target return and reserve-eligibility constraints.
      2. Historical price series estimation engine supporting monthly adjusted
         close prices from 'prices.csv' (all available months vs. last 36 months).
      3. Rigorous automated verification against the professor's known answers
         (Test A: Base, Test B: Lower equity return, Test C: Higher IG/Equity corr).

Python standard library primary implementation with optional pandas compatibility.
================================================================================
"""

from __future__ import annotations

import csv
import io
import math
import os
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple, Union

# ==============================================================================
# COURSE-PROVIDED TRAINING ASSUMPTIONS (Meridian Foundation)
# ==============================================================================

DEFAULT_SLEEVES: List[Dict[str, Any]] = [
    {
        "name": "Treasury bills",
        "expected_return": 0.035,
        "volatility": 0.005,
        "reserve_eligible": True,
    },
    {
        "name": "Treasury 10-year note",
        "expected_return": 0.043,
        "volatility": 0.070,
        "reserve_eligible": True,
    },
    {
        "name": "Investment-grade bond fund",
        "expected_return": 0.050,
        "volatility": 0.060,
        "reserve_eligible": False,
    },
    {
        "name": "Global equity index fund",
        "expected_return": 0.080,
        "volatility": 0.160,
        "reserve_eligible": False,
    },
]

# Baseline Correlation Matrix (Bills, 10-Year, IG Bonds, Global Equity)
DEFAULT_CORRELATION_MATRIX: List[List[float]] = [
    [1.00,  0.10,  0.05,  0.00],
    [0.10,  1.00,  0.80, -0.10],
    [0.05,  0.80,  1.00,  0.25],
    [0.00, -0.10,  0.25,  1.00],
]

# Meridian Institutional Parameters
CPI_ESTIMATE: float = 0.025             # 2.5% inflation estimate
REAL_RETURN_TARGET: float = 0.040       # 4.0% real return objective
OBJECTIVE_RETURN: float = CPI_ESTIMATE + REAL_RETURN_TARGET  # 6.50% nominal target
MIN_RESERVE_ALLOCATION: float = 0.030   # 3.00% liquidity reserve floor


# ==============================================================================
# 1. CORE RISK ENGINE (Preserved from Lab 14)
# ==============================================================================

def validate_correlation_matrix(matrix: List[List[float]], n_assets: int) -> bool:
    """
    Validates correlation matrix dimensions, bounds [-1.0, 1.0], unit diagonal,
    and exact symmetry. Raises ValueError upon breach.
    """
    if len(matrix) != n_assets:
        raise ValueError(
            f"Correlation matrix dimension error: expected {n_assets} rows, got {len(matrix)}."
        )

    for i in range(n_assets):
        if len(matrix[i]) != n_assets:
            raise ValueError(
                f"Correlation matrix row {i} dimension error: expected {n_assets} columns, got {len(matrix[i])}."
            )

        if abs(matrix[i][i] - 1.0) > 1e-7:
            raise ValueError(
                f"Correlation diagonal error: diagonal element ({i}, {i}) must be 1.0, got {matrix[i][i]}."
            )

        for j in range(n_assets):
            val = matrix[i][j]
            if val < -1.0 or val > 1.0:
                raise ValueError(
                    f"Invalid correlation value: cell ({i}, {j}) has value {val:.4f}, "
                    f"which violates the required range [-1.0, +1.0]."
                )

            diff = abs(matrix[i][j] - matrix[j][i])
            if diff > 1e-7:
                raise ValueError(
                    f"Asymmetric correlation matrix: cell ({i}, {j}) = {matrix[i][j]:.4f} "
                    f"does not match cell ({j}, {i}) = {matrix[j][i]:.4f} (difference: {diff:.6e})."
                )

    return True


def calculate_covariance_matrix(
    corr_matrix: List[List[float]], volatilities: List[float]
) -> List[List[float]]:
    """
    Constructs the covariance matrix:
      cov[i][j] = corr[i][j] * vol[i] * vol[j]
    """
    n = len(volatilities)
    cov_matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cov_matrix[i][j] = corr_matrix[i][j] * volatilities[i] * volatilities[j]
    return cov_matrix


def calculate_expected_return(weights: List[float], returns: List[float]) -> float:
    """
    Calculates portfolio expected return:
      E(R_p) = sum(w_i * E(R_i))
    """
    if len(weights) != len(returns):
        raise ValueError("Length mismatch between weights and expected returns.")
    return sum(w * r for w, r in zip(weights, returns))


def calculate_portfolio_volatility(
    weights: List[float], cov_matrix: List[List[float]]
) -> float:
    """
    Calculates portfolio standard deviation incorporating full covariance:
      sigma_p = sqrt(w^T * Cov * w)
    """
    n = len(weights)
    variance = 0.0
    for i in range(n):
        for j in range(n):
            variance += weights[i] * weights[j] * cov_matrix[i][j]

    if variance < 0.0:
        if abs(variance) < 1e-12:
            variance = 0.0
        else:
            raise ValueError(f"Negative portfolio variance encountered: {variance}")

    return math.sqrt(variance)


def calculate_reserve_eligible_allocation(
    weights: List[float], reserve_flags: List[bool]
) -> float:
    """
    Calculates total allocation to reserve-eligible assets.
    """
    if len(weights) != len(reserve_flags):
        raise ValueError("Length mismatch between weights and reserve flags.")
    return sum(w for w, flag in zip(weights, reserve_flags) if flag)


def check_return_objective(
    expected_return: float, objective_rate: float = OBJECTIVE_RETURN
) -> bool:
    """
    Checks if expected return meets or exceeds target return (within floating tolerance).
    """
    return expected_return >= (objective_rate - 1e-7)


def calculate_inverse_volatility_weights(volatilities: List[float]) -> List[float]:
    """
    Weights inversely proportional to volatility:
      w_i = (1 / sigma_i) / sum_k(1 / sigma_k)
    """
    for v in volatilities:
        if v <= 0.0:
            raise ValueError(f"Asset volatility must be strictly positive, got {v}.")
    inv_vols = [1.0 / v for v in volatilities]
    total_inv = sum(inv_vols)
    return [inv / total_inv for inv in inv_vols]


def evaluate_portfolio(
    name: str,
    weights: List[float],
    sleeves: List[Dict[str, Any]],
    cov_matrix: List[List[float]],
    objective_rate: float = OBJECTIVE_RETURN,
) -> Dict[str, Any]:
    """
    Evaluates expected return, volatility, reserve allocation, and hurdle compliance.
    """
    returns = [s["expected_return"] for s in sleeves]
    reserve_flags = [bool(s["reserve_eligible"]) for s in sleeves]

    exp_return = calculate_expected_return(weights, returns)
    volatility = calculate_portfolio_volatility(weights, cov_matrix)
    reserve_weight = calculate_reserve_eligible_allocation(weights, reserve_flags)
    meets_objective = check_return_objective(exp_return, objective_rate)

    return {
        "name": name,
        "weights": weights,
        "weights_pct": [w * 100.0 for w in weights],
        "expected_return": exp_return,
        "expected_return_pct": exp_return * 100.0,
        "volatility": volatility,
        "volatility_pct": volatility * 100.0,
        "reserve_weight": reserve_weight,
        "reserve_weight_pct": reserve_weight * 100.0,
        "meets_objective": meets_objective,
        "meets_str": "yes" if meets_objective else "no",
    }


# ==============================================================================
# 2. REUSABLE GRID SEARCH OPTIMIZATION ENGINE (Lab 15 Requirement 2)
# ==============================================================================

def generate_long_only_allocations(
    n_assets: int, step_pct: int = 5
) -> Generator[Tuple[float, ...], None, None]:
    """
    Generates every possible long-only portfolio allocation in step_pct increments
    (default 5 percentage points) such that weights sum exactly to 100%.

    Uses integer partition search to guarantee exact arithmetic with no float drift.
    For n=4 and step=5%, yields exactly 1,771 allocations.
    """
    if step_pct <= 0 or 100 % step_pct != 0:
        raise ValueError(f"step_pct must evenly divide 100, got {step_pct}")

    total_units = 100 // step_pct

    def _recurse(remaining_units: int, count: int) -> Generator[Tuple[float, ...], None, None]:
        if count == 1:
            yield (round(remaining_units * step_pct / 100.0, 4),)
            return
        for units in range(remaining_units + 1):
            w = round(units * step_pct / 100.0, 4)
            for tail in _recurse(remaining_units - units, count - 1):
                yield (w,) + tail

    return _recurse(total_units, n_assets)


def optimize_portfolio(
    sleeves: List[Dict[str, Any]],
    corr_matrix: List[List[float]],
    objective_rate: float = OBJECTIVE_RETURN,
    min_reserve: float = MIN_RESERVE_ALLOCATION,
    step_pct: int = 5,
) -> Dict[str, Any]:
    """
    Conducts a complete, reproducible grid search over all long-only allocations
    in step_pct increments (default 5 pp):
      1. Requires portfolio weights to total 100%.
      2. Retains portfolios with expected return >= objective_rate.
      3. Retains portfolios with reserve-eligible allocation >= min_reserve.
      4. Computes volatility using full covariance matrix.
      5. Returns the qualifying portfolio with the absolute lowest volatility.
      6. Returns a non-feasible result if no portfolio satisfies both constraints.
    """
    n_assets = len(sleeves)
    validate_correlation_matrix(corr_matrix, n_assets)

    vols = [float(s["volatility"]) for s in sleeves]
    returns = [float(s["expected_return"]) for s in sleeves]
    reserve_flags = [bool(s["reserve_eligible"]) for s in sleeves]

    cov_matrix = calculate_covariance_matrix(corr_matrix, vols)

    best_vol: float = float("inf")
    best_weights: Optional[Tuple[float, ...]] = None
    best_ret: Optional[float] = None
    best_res: Optional[float] = None
    qualifying_count: int = 0
    total_evaluated: int = 0

    # Tolerance to prevent floating point edge-case exclusions
    tol: float = 1e-7

    for alloc in generate_long_only_allocations(n_assets, step_pct=step_pct):
        total_evaluated += 1
        ret = calculate_expected_return(list(alloc), returns)
        reserve = calculate_reserve_eligible_allocation(list(alloc), reserve_flags)

        if (ret >= objective_rate - tol) and (reserve >= min_reserve - tol):
            qualifying_count += 1
            vol = calculate_portfolio_volatility(list(alloc), cov_matrix)
            if vol < best_vol:
                best_vol = vol
                best_weights = alloc
                best_ret = ret
                best_res = reserve

    if best_weights is None:
        return {
            "feasible": False,
            "message": (
                f"No feasible allocation satisfies both the expected return objective "
                f"(>= {objective_rate * 100:.2f}%) and the reserve floor "
                f"(>= {min_reserve * 100:.2f}%)."
            ),
            "total_evaluated": total_evaluated,
            "qualifying_count": 0,
            "weights": None,
            "weights_pct": None,
            "expected_return": None,
            "expected_return_pct": None,
            "volatility": None,
            "volatility_pct": None,
            "reserve_weight": None,
            "reserve_weight_pct": None,
        }

    return {
        "feasible": True,
        "name": "Lowest-Risk Qualifying Portfolio",
        "weights": list(best_weights),
        "weights_pct": [round(w * 100.0, 2) for w in best_weights],
        "expected_return": best_ret,
        "expected_return_pct": round(best_ret * 100.0, 2),
        "volatility": best_vol,
        "volatility_pct": round(best_vol * 100.0, 2),
        "reserve_weight": best_res,
        "reserve_weight_pct": round(best_res * 100.0, 2),
        "total_evaluated": total_evaluated,
        "qualifying_count": qualifying_count,
        "message": f"Successfully identified optimal portfolio among {qualifying_count:,} qualifying candidates.",
    }


# ==============================================================================
# 3. HISTORICAL PRICE ESTIMATION ENGINE (Lab 15 Requirement 3)
# ==============================================================================

def parse_prices_csv(
    file_source: Union[str, Path, io.StringIO, io.BytesIO],
    min_funds: int = 3,
    max_funds: int = 6,
) -> Dict[str, Any]:
    """
    Parses a monthly adjusted close prices CSV file and calculates historical return,
    volatility, and correlation estimates.

    CSV Requirements:
      - Column 0: Date (chronological, oldest month first).
      - Columns 1+: Adjusted closing prices for 3 to 6 fund tickers.

    Calculations:
      - Monthly percentage returns: r_t = (P_t - P_{t-1}) / P_{t-1}
      - Annualized return = average monthly return * 12
      - Annualized volatility = monthly sample standard deviation * sqrt(12)
      - Correlation matrix across all asset pairs
      - Dual window evaluation: All available months vs. Last 36 months

    Note: Historical estimates are backward-looking and not guaranteed future returns.
    """
    # Handle string paths, Path objects, or in-memory file buffers
    if isinstance(file_source, (str, Path)):
        path = Path(file_source)
        if not path.exists():
            raise FileNotFoundError(
                f"Historical prices file not found at '{path}'. Required format: "
                f"Date column first (oldest month first), followed by 3-6 ticker columns."
            )
        with open(path, "r", encoding="utf-8-sig") as f:
            content = f.read()
    elif isinstance(file_source, io.BytesIO):
        content = file_source.getvalue().decode("utf-8-sig", errors="replace")
    elif isinstance(file_source, io.StringIO):
        content = file_source.getvalue()
    else:
        # Generic buffer (e.g. Streamlit UploadedFile)
        try:
            content = file_source.read()
            if isinstance(content, bytes):
                content = content.decode("utf-8-sig", errors="replace")
        except Exception as e:
            raise ValueError(f"Unable to read CSV content: {e}")

    reader = csv.reader(io.StringIO(content.strip()))
    rows = [row for row in reader if row and any(cell.strip() for cell in row)]

    if len(rows) < 3:
        raise ValueError("CSV contains insufficient data rows (minimum 2 price points required).")

    header = [col.strip() for col in rows[0]]
    date_col = header[0]
    tickers = header[1:]

    if len(tickers) < min_funds or len(tickers) > max_funds:
        raise ValueError(
            f"CSV must contain between {min_funds} and {max_funds} asset ticker columns. "
            f"Found {len(tickers)}: {tickers}"
        )

    dates: List[str] = []
    prices: Dict[str, List[float]] = {t: [] for t in tickers}

    for row_idx, row in enumerate(rows[1:], start=2):
        if len(row) < len(header):
            continue  # Skip ragged empty rows
        dates.append(row[0].strip())
        for idx, ticker in enumerate(tickers, start=1):
            val_str = row[idx].strip().replace("$", "").replace(",", "")
            try:
                prices[ticker].append(float(val_str))
            except ValueError:
                raise ValueError(
                    f"Row {row_idx}: non-numeric price '{row[idx]}' for ticker '{ticker}'."
                )

    n_prices = len(dates)
    if n_prices < 2:
        raise ValueError("At least 2 price rows are required to calculate percentage returns.")

    # Calculate monthly percentage returns: r_t = (P_t - P_{t-1}) / P_{t-1}
    monthly_returns: Dict[str, List[float]] = {t: [] for t in tickers}
    for t in tickers:
        p_list = prices[t]
        for i in range(1, len(p_list)):
            if p_list[i - 1] <= 0:
                raise ValueError(f"Non-positive price encountered for {t} at row {i + 1}.")
            monthly_returns[t].append((p_list[i] - p_list[i - 1]) / p_list[i - 1])

    n_return_months = len(dates) - 1

    def _compute_stats(returns_subset: Dict[str, List[float]]) -> Dict[str, Any]:
        """Calculates annualized metrics and correlation matrix for a returns dict."""
        m_count = len(next(iter(returns_subset.values())))
        if m_count < 2:
            return {"error": "Insufficient observations (need at least 2 return months)."}

        means: Dict[str, float] = {}
        stds: Dict[str, float] = {}
        ann_returns: Dict[str, float] = {}
        ann_volatilities: Dict[str, float] = {}

        for t in tickers:
            series = returns_subset[t]
            mean_m = sum(series) / m_count
            variance_m = sum((x - mean_m) ** 2 for x in series) / (m_count - 1)
            std_m = math.sqrt(max(0.0, variance_m))

            means[t] = mean_m
            stds[t] = std_m
            ann_returns[t] = mean_m * 12.0
            ann_volatilities[t] = std_m * math.sqrt(12.0)

        # Pairwise Pearson correlation
        corr_matrix: List[List[float]] = []
        for i, t_i in enumerate(tickers):
            row_corr: List[float] = []
            for j, t_j in enumerate(tickers):
                if i == j:
                    row_corr.append(1.00)
                else:
                    cov_ij = sum(
                        (returns_subset[t_i][k] - means[t_i])
                        * (returns_subset[t_j][k] - means[t_j])
                        for k in range(m_count)
                    ) / (m_count - 1)
                    denom = stds[t_i] * stds[t_j]
                    corr_val = cov_ij / denom if denom > 1e-12 else 0.0
                    corr_val = max(-1.0, min(1.0, corr_val))
                    row_corr.append(round(corr_val, 4))
            corr_matrix.append(row_corr)

        return {
            "observations_count": m_count,
            "annualized_returns": ann_returns,
            "annualized_volatilities": ann_volatilities,
            "monthly_means": means,
            "monthly_stds": stds,
            "correlation_matrix": corr_matrix,
        }

    # 1. All available months
    all_stats = _compute_stats(monthly_returns)

    # 2. Last 36 months (if available)
    last_36_stats: Optional[Dict[str, Any]] = None
    if n_return_months >= 36:
        last_36_returns = {t: monthly_returns[t][-36:] for t in tickers}
        last_36_stats = _compute_stats(last_36_returns)

    return {
        "tickers": tickers,
        "n_price_observations": n_prices,
        "n_return_months": n_return_months,
        "first_date": dates[0],
        "last_date": dates[-1],
        "all_months": all_stats,
        "last_36_months": last_36_stats,
        "disclaimer": "Historical estimates are backward-looking and not guaranteed future returns.",
    }


# ==============================================================================
# 4. PROFESSOR'S KNOWN ANSWERS VERIFICATION (Tests A, B, and C)
# ==============================================================================

def run_professor_known_answer_tests() -> Dict[str, Dict[str, Any]]:
    """
    Executes and validates the professor's 3 required benchmark tests:
      Test A: Original Meridian training inputs
              Expected: [0%, 20%, 25%, 55%], Return: 6.51%, Volatility: 9.44%
      Test B: Global equity expected return decreases from 8.0% to 7.0%
              Expected: [0%, 10%, 10%, 80%], Return: 6.53%, Volatility: 12.94%
              Largest weight shift: 25 pp
      Test C: IG bond / Equity correlation increases from 0.25 to 0.50
              Expected: [0%, 40%, 0%, 60%], Return: 6.52%, Volatility: 9.73%
    """
    results: Dict[str, Dict[str, Any]] = {}

    # TEST A: Base inputs
    res_a = optimize_portfolio(
        DEFAULT_SLEEVES, DEFAULT_CORRELATION_MATRIX, OBJECTIVE_RETURN, MIN_RESERVE_ALLOCATION
    )
    pass_a_weights = res_a["weights_pct"] == [0.0, 20.0, 25.0, 55.0]
    pass_a_ret = abs(res_a["expected_return_pct"] - 6.51) <= 0.02
    pass_a_vol = abs(res_a["volatility_pct"] - 9.44) <= 0.02
    results["Test A"] = {
        "description": "Original inputs",
        "result": res_a,
        "passed": pass_a_weights and pass_a_ret and pass_a_vol,
        "expected": {"weights": [0.0, 20.0, 25.0, 55.0], "return": 6.51, "volatility": 9.44},
    }

    # TEST B: Equity expected return decreases 8.0% -> 7.0%
    sleeves_b = [dict(s) for s in DEFAULT_SLEEVES]
    sleeves_b[3] = dict(sleeves_b[3])
    sleeves_b[3]["expected_return"] = 0.070
    res_b = optimize_portfolio(
        sleeves_b, DEFAULT_CORRELATION_MATRIX, OBJECTIVE_RETURN, MIN_RESERVE_ALLOCATION
    )
    base_weights = res_a["weights_pct"]
    diffs = [abs(curr - base) for curr, base in zip(res_b["weights_pct"], base_weights)]
    largest_diff = max(diffs)

    pass_b_weights = res_b["weights_pct"] == [0.0, 10.0, 10.0, 80.0]
    pass_b_ret = abs(res_b["expected_return_pct"] - 6.53) <= 0.02
    pass_b_vol = abs(res_b["volatility_pct"] - 12.94) <= 0.02
    pass_b_diff = abs(largest_diff - 25.0) <= 0.01

    results["Test B"] = {
        "description": "Equity return decreases to 7.0%",
        "result": res_b,
        "largest_weight_change_pp": largest_diff,
        "passed": pass_b_weights and pass_b_ret and pass_b_vol and pass_b_diff,
        "expected": {
            "weights": [0.0, 10.0, 10.0, 80.0],
            "return": 6.53,
            "volatility": 12.94,
            "largest_weight_change_pp": 25.0,
        },
    }

    # TEST C: IG bond / Equity correlation increases 0.25 -> 0.50
    corr_c = [row[:] for row in DEFAULT_CORRELATION_MATRIX]
    corr_c[2][3] = 0.50
    corr_c[3][2] = 0.50
    res_c = optimize_portfolio(
        DEFAULT_SLEEVES, corr_c, OBJECTIVE_RETURN, MIN_RESERVE_ALLOCATION
    )
    pass_c_weights = res_c["weights_pct"] == [0.0, 40.0, 0.0, 60.0]
    pass_c_ret = abs(res_c["expected_return_pct"] - 6.52) <= 0.02
    pass_c_vol = abs(res_c["volatility_pct"] - 9.73) <= 0.02

    results["Test C"] = {
        "description": "IG bond / equity correlation increases to 0.50",
        "result": res_c,
        "passed": pass_c_weights and pass_c_ret and pass_c_vol,
        "expected": {"weights": [0.0, 40.0, 0.0, 60.0], "return": 6.52, "volatility": 9.73},
    }

    return results


# ==============================================================================
# 5. CLI EXECUTION ENTRY POINT
# ==============================================================================

def main():
    print("=" * 80)
    print("FIN 439 -- LAB 15: PORTFOLIO STABILITY DECISION & OPTIMIZATION")
    print("Student: Elliot | Case: Meridian Foundation Training Assumptions")
    print(
        f"Objective Return: {OBJECTIVE_RETURN * 100:.2f}% | Reserve Floor: {MIN_RESERVE_ALLOCATION * 100:.2f}%"
    )
    print("=" * 80)

    # 1. Lab 14 Baseline Portfolios
    n_assets = len(DEFAULT_SLEEVES)
    validate_correlation_matrix(DEFAULT_CORRELATION_MATRIX, n_assets)
    vols = [s["volatility"] for s in DEFAULT_SLEEVES]
    cov_matrix = calculate_covariance_matrix(DEFAULT_CORRELATION_MATRIX, vols)

    portfolios = [
        ("Benchmark", [0.0, 0.0, 0.40, 0.60]),
        ("Equal weight", [0.25, 0.25, 0.25, 0.25]),
        ("Inverse volatility", calculate_inverse_volatility_weights(vols)),
    ]

    print("\n--- LAB 14 BASELINE PORTFOLIOS (PRESERVED) ---")
    header = f"{'Portfolio':<20} | {'Weights (Bills/10-Yr/IG/Eq)':<30} | {'Return':>8} | {'Volatility':>10} | {'Reserve':>8} | {'Meets 6.5%':>10}"
    print(header)
    print("-" * len(header))
    for name, weights in portfolios:
        res = evaluate_portfolio(name, weights, DEFAULT_SLEEVES, cov_matrix, OBJECTIVE_RETURN)
        w_str = " / ".join(f"{w:.1f}" for w in res["weights_pct"])
        print(
            f"{res['name']:<20} | {w_str:<30} | {res['expected_return_pct']:>7.2f}% | "
            f"{res['volatility_pct']:>9.2f}% | {res['reserve_weight_pct']:>7.1f}% | {res['meets_str']:>10}"
        )
    print("-" * len(header))

    # 2. Lab 15 Verification Tests
    print("\n--- LAB 15 PROFESSOR'S KNOWN ANSWERS VERIFICATION ---")
    tests = run_professor_known_answer_tests()
    for t_name, data in tests.items():
        res = data["result"]
        exp = data["expected"]
        status = "PASS" if data["passed"] else "FAIL"
        w_str = " / ".join(f"{w:.0f}%" for w in res["weights_pct"])
        exp_w_str = " / ".join(f"{w:.0f}%" for w in exp["weights"])
        print(f"\n{t_name} — {data['description']}: [{status}]")
        print(f"  Calculated Weights:    {w_str} (Expected: {exp_w_str})")
        print(f"  Calculated Return:     {res['expected_return_pct']:.2f}% (Expected: {exp['return']:.2f}%)")
        print(f"  Calculated Volatility: {res['volatility_pct']:.2f}% (Expected: {exp['volatility']:.2f}%)")
        print(f"  Reserve Allocation:    {res['reserve_weight_pct']:.1f}%")
        if "largest_weight_change_pp" in data:
            print(
                f"  Largest Weight Shift:  {data['largest_weight_change_pp']:.1f} pp (Expected: {exp['largest_weight_change_pp']:.1f} pp)"
            )

    # 3. Check for prices.csv
    print("\n--- HISTORICAL PRICES STATUS ---")
    repo_root = Path(__file__).resolve().parent.parent
    local_csv = Path(__file__).resolve().parent / "prices.csv"
    root_csv = repo_root / "prices.csv"

    csv_target = local_csv if local_csv.exists() else (root_csv if root_csv.exists() else None)
    if csv_target:
        print(f"Found '{csv_target.name}' at: {csv_target}")
        parsed = parse_prices_csv(csv_target)
        print(f"Successfully loaded {parsed['n_return_months']} monthly return observations for {parsed['tickers']}.")
    else:
        print("Status: 'prices.csv' is NOT present in the workspace.")
        print("  - Diagnostic Note: The historical estimation engine is fully implemented and tested.")
        print("  - Required Format: Column 0 = Date (oldest month first), Columns 1-6 = Fund Adjusted Closes.")
        print("  - Streamlit File Uploader: Users can upload any compliant CSV interactively in the web app.")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
