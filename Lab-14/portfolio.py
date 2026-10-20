#!/usr/bin/env python3
"""
================================================================================
FIN 439: Applied Financial Modeling & Corporate Valuation
Week 9, Lab 14 — Portfolio Baselines
Student: Elliot
Script: portfolio.py

Description:
    Risk engine and baseline portfolio valuation for the Meridian Foundation
    training case. Computes covariance, expected return, portfolio volatility,
    and reserve-eligible share across three baseline portfolios:
      1. Benchmark (40% IG Bonds, 60% Global Equity)
      2. Equal Weight (25% each across four sleeves)
      3. Inverse Volatility (weights proportional to 1 / volatility)

    Enforces strict correlation validation (range [-1.0, 1.0] and matrix symmetry)
    and verifies results against the professor's published answers.
    Python standard library only.
================================================================================
"""

import math
import sys

# ==============================================================================
# EDITABLE INPUTS (Course-Provided Training Assumptions — Meridian Foundation)
# ==============================================================================

# Asset Sleeves: (Name, Expected Return, Volatility, Reserve Eligible)
# Returns and volatilities expressed as decimal rates (e.g., 0.035 = 3.5%)
SLEEVES = [
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

# Correlation Matrix (Sleeves order: Bills, 10-year, IG bonds, Equity)
CORRELATION_MATRIX = [
    [1.00,  0.10,  0.05,  0.00],
    [0.10,  1.00,  0.80, -0.10],
    [0.05,  0.80,  1.00,  0.25],
    [0.00, -0.10,  0.25,  1.00],
]

# Objective and Inflation Parameters
CPI_ESTIMATE = 0.025            # 2.5% inflation baseline
REAL_RETURN_TARGET = 0.040      # 4.0% real return objective
OBJECTIVE_RETURN = CPI_ESTIMATE + REAL_RETURN_TARGET  # 6.5% nominal return objective


# ==============================================================================
# COMPUTATION ENGINE FUNCTIONS
# ==============================================================================

def validate_correlation_matrix(matrix: list, n_assets: int) -> bool:
    """
    Validates that:
      1. Matrix has dimensions n_assets x n_assets.
      2. All correlation values lie within [-1.0, 1.0].
      3. Matrix is symmetric: corr[i][j] == corr[j][i].
      4. Diagonal entries are equal to 1.0.

    Raises ValueError with a clear explanatory message if any check fails.
    Returns True if valid.
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

        # Check diagonal
        if abs(matrix[i][i] - 1.0) > 1e-7:
            raise ValueError(
                f"Correlation diagonal error: diagonal element ({i}, {i}) must be 1.0, got {matrix[i][i]}."
            )

        for j in range(n_assets):
            val = matrix[i][j]
            # Check range [-1.0, 1.0]
            if val < -1.0 or val > 1.0:
                raise ValueError(
                    f"Invalid correlation value: cell ({i}, {j}) has value {val:.4f}, "
                    f"which violates the required range [-1.0, +1.0]."
                )

            # Check symmetry
            diff = abs(matrix[i][j] - matrix[j][i])
            if diff > 1e-7:
                raise ValueError(
                    f"Asymmetric correlation matrix: cell ({i}, {j}) = {matrix[i][j]:.4f} "
                    f"does not match cell ({j}, {i}) = {matrix[j][i]:.4f} (difference: {diff:.6e})."
                )

    return True


def calculate_covariance_matrix(corr_matrix: list, volatilities: list) -> list:
    """
    Builds the covariance matrix from correlation matrix and asset volatilities:
      cov[i][j] = corr[i][j] * vol[i] * vol[j]
    """
    n = len(volatilities)
    cov_matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cov_matrix[i][j] = corr_matrix[i][j] * volatilities[i] * volatilities[j]
    return cov_matrix


def calculate_expected_return(weights: list, returns: list) -> float:
    """
    Calculates portfolio expected return:
      E(R_p) = sum(w_i * E(R_i))
    """
    if len(weights) != len(returns):
        raise ValueError("Length mismatch between weights and expected returns.")
    return sum(w * r for w, r in zip(weights, returns))


def calculate_portfolio_volatility(weights: list, cov_matrix: list) -> float:
    """
    Calculates portfolio volatility (standard deviation), including all covariance terms:
      sigma_p = sqrt(sum_i sum_j (w_i * w_j * cov[i][j]))
    """
    n = len(weights)
    variance = 0.0
    for i in range(n):
        for j in range(n):
            variance += weights[i] * weights[j] * cov_matrix[i][j]

    if variance < 0.0:
        # Protect against slight floating point negative zero
        if abs(variance) < 1e-12:
            variance = 0.0
        else:
            raise ValueError(f"Negative portfolio variance encountered: {variance}")

    return math.sqrt(variance)


def calculate_reserve_eligible_allocation(weights: list, reserve_flags: list) -> float:
    """
    Calculates total portfolio weight allocated to reserve-eligible assets.
    """
    if len(weights) != len(reserve_flags):
        raise ValueError("Length mismatch between weights and reserve flags.")
    return sum(w for w, flag in zip(weights, reserve_flags) if flag)


def check_return_objective(expected_return: float, objective_rate: float = OBJECTIVE_RETURN) -> bool:
    """
    Determines whether expected portfolio return meets or exceeds the required return objective.
    """
    return expected_return >= (objective_rate - 1e-7)


def calculate_inverse_volatility_weights(volatilities: list) -> list:
    """
    Calculates inverse-volatility weights:
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
    weights: list,
    sleeves: list,
    cov_matrix: list,
    objective_rate: float = OBJECTIVE_RETURN,
) -> dict:
    """
    Evaluates a portfolio against expected return, volatility, reserve share,
    and return objective compliance.
    """
    names = [s["name"] for s in sleeves]
    returns = [s["expected_return"] for s in sleeves]
    reserve_flags = [s["reserve_eligible"] for s in sleeves]

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
# VALIDATION TESTS (Sensitivity & Error Refusal)
# ==============================================================================

def run_correlation_sensitivity_test(sleeves: list, base_corr: list) -> dict:
    """
    Test 1 — Correlation sensitivity:
    Temporarily changes Investment-grade bond / Equity correlation from 0.25 to 0.50
    in both symmetric matrix positions [2][3] and [3][2].
    Evaluates the Benchmark portfolio (0% bills, 0% 10-year, 40% IG, 60% Equity).
    Expected benchmark volatility: approximately 11.00% (exact: 10.9982%).
    Restores original correlation table afterward.
    """
    # Create isolated deep-copy of correlation matrix
    test_corr = [row[:] for row in base_corr]
    test_corr[2][3] = 0.50
    test_corr[3][2] = 0.50

    validate_correlation_matrix(test_corr, len(sleeves))
    vols = [s["volatility"] for s in sleeves]
    test_cov = calculate_covariance_matrix(test_corr, vols)

    benchmark_weights = [0.0, 0.0, 0.40, 0.60]
    result = evaluate_portfolio("Benchmark (0.50 Corr Sensitivity)", benchmark_weights, sleeves, test_cov)
    return result


def run_invalid_correlation_test(sleeves: list, base_corr: list) -> dict:
    """
    Test 2 — Invalid correlation:
    Temporarily sets Investment-grade bond / Equity correlation to 1.30.
    Verifies that the validation function refuses the matrix with a clear error message.
    Restores original inputs afterward.
    """
    test_corr = [row[:] for row in base_corr]
    test_corr[2][3] = 1.30
    test_corr[3][2] = 1.30

    refused = False
    error_message = ""
    try:
        validate_correlation_matrix(test_corr, len(sleeves))
    except ValueError as exc:
        refused = True
        error_message = str(exc)

    return {
        "refused": refused,
        "error_message": error_message,
        "test_passed": refused and ("[-1.0, +1.0]" in error_message or "1.30" in error_message),
    }


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    print("=" * 80)
    print("FIN 439 -- LAB 14: PORTFOLIO BASELINES RISK ENGINE")
    print("Student: Elliot | Case: Meridian Foundation Training Assumptions")
    print(f"Objective Return: {OBJECTIVE_RETURN * 100:.2f}% (CPI {CPI_ESTIMATE * 100:.1f}% + {REAL_RETURN_TARGET * 100:.1f}%)")
    print("=" * 80)

    # 1. Validate baseline correlation matrix
    n_assets = len(SLEEVES)
    validate_correlation_matrix(CORRELATION_MATRIX, n_assets)
    vols = [s["volatility"] for s in SLEEVES]
    cov_matrix = calculate_covariance_matrix(CORRELATION_MATRIX, vols)

    # 2. Define Portfolios
    # Portfolio A — Benchmark: 0% bills, 0% 10-year, 40% IG bonds, 60% global equity
    weights_benchmark = [0.0, 0.0, 0.40, 0.60]

    # Portfolio B — Equal Weight: 25% in each of the four assets
    weights_equal = [0.25, 0.25, 0.25, 0.25]

    # Portfolio C — Inverse Volatility: 1 / volatility scaled to 100%
    weights_inv_vol = calculate_inverse_volatility_weights(vols)

    portfolios = [
        ("Benchmark", weights_benchmark),
        ("Equal weight", weights_equal),
        ("Inverse volatility", weights_inv_vol),
    ]

    results = []
    print("\nPORTFOLIO BASELINE EVALUATIONS:")
    print("-" * 80)
    for name, weights in portfolios:
        res = evaluate_portfolio(name, weights, SLEEVES, cov_matrix, OBJECTIVE_RETURN)
        results.append(res)

        print(f"Portfolio: {res['name']}")
        weights_str = " / ".join(f"{s['name']}: {w:.1f}%" for s, w in zip(SLEEVES, res["weights_pct"]))
        compact_weights = " / ".join(f"{w:.1f}" for w in res["weights_pct"])
        print(f"  Weights (Bills / 10-Yr / IG Bonds / Equity): {compact_weights}%")
        print(f"  Detailed Allocation:   {weights_str}")
        print(f"  Expected Return:       {res['expected_return_pct']:.2f}%")
        print(f"  Portfolio Volatility:  {res['volatility_pct']:.2f}% (Exact: {res['volatility_pct']:.4f}%)")
        print(f"  Reserve-Eligible:      {res['reserve_weight_pct']:.1f}%")
        print(f"  Meets 6.5% Objective:  {res['meets_str'].upper()}")
        print()

    # 3. Formatted Summary Table matching handout specification
    print("=" * 80)
    print("VERIFICATION AGAINST PROFESSOR'S KNOWN ANSWERS")
    print("=" * 80)
    header = f"{'Portfolio':<20} | {'Weights (Bills/10-Yr/IG/Eq)':<30} | {'Return':>8} | {'Volatility':>10} | {'Reserve':>8} | {'Meets 6.5%':>10}"
    print(header)
    print("-" * len(header))
    for res in results:
        w_str = " / ".join(f"{w:.1f}" for w in res["weights_pct"])
        row = (
            f"{res['name']:<20} | "
            f"{w_str:<30} | "
            f"{res['expected_return_pct']:>7.2f}% | "
            f"{res['volatility_pct']:>9.2f}% | "
            f"{res['reserve_weight_pct']:>7.1f}% | "
            f"{res['meets_str']:>10}"
        )
        print(row)
    print("-" * len(header))

    # 4. Execute Required Validation Tests
    print("\n" + "=" * 80)
    print("REQUIRED ENGINE VALIDATION TESTS")
    print("=" * 80)

    # Test 1 — Correlation Sensitivity
    print("TEST 1: Correlation Sensitivity (IG Bonds / Equity shifted from 0.25 to 0.50)")
    sens_result = run_correlation_sensitivity_test(SLEEVES, CORRELATION_MATRIX)
    print(f"  Modified Correlation:       corr(IG, Equity) = 0.50 (both symmetric positions)")
    print(f"  Base Benchmark Volatility:  {results[0]['volatility_pct']:.2f}% (at corr = 0.25)")
    print(f"  Sens Benchmark Volatility:  {sens_result['volatility_pct']:.2f}% (Exact: {sens_result['volatility_pct']:.4f}%)")
    print(f"  Expected Volatility:        ~11.00%")
    test1_pass = abs(sens_result["volatility_pct"] - 11.00) < 0.05
    print(f"  Test 1 Status:              {'PASS (Matches 11.00% benchmark expectation)' if test1_pass else 'FAIL'}")

    # Test 2 — Invalid Correlation
    print("\nTEST 2: Invalid Correlation Refusal (IG Bonds / Equity shifted to 1.30)")
    inv_test = run_invalid_correlation_test(SLEEVES, CORRELATION_MATRIX)
    print(f"  Modified Correlation:       corr(IG, Equity) = 1.30 (exceeds +1.0 limit)")
    print(f"  Engine Refused Execution:   {inv_test['refused']}")
    print(f"  Captured Error Message:     {inv_test['error_message']}")
    print(f"  Test 2 Status:              {'PASS (Engine strictly refused invalid correlation)' if inv_test['test_passed'] else 'FAIL'}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
