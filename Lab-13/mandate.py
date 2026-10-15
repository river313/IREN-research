#!/usr/bin/env python3
"""
================================================================================
FIN 439: Applied Financial Modeling & Corporate Valuation
Lab 13 — Portfolio Mandate Defense (Week 8)
Student: Elliot
Script: mandate.py

Description:
    Evaluates candidate portfolios against the Meridian Foundation investment
    mandate. Implements mechanical constraint checks for:
      1. Weights sum to 100%
      2. Long-only constraint (lowest weight >= 0.0%)
      3. Reserve requirement (reserve-eligible weight >= reserve minimum)
      4. Five-business-day liquidity requirement (redeemable <= 5 days >= 90.0%)
      5. Single-company issuer concentration ceiling (aggregate <= 8.0%)
      6. Calendar-year loss rule (flagged as "requires CIO clarification")

    Standard library only. Computes all values dynamically from editable inputs.
================================================================================
"""

import sys

# ==============================================================================
# EDITABLE INPUTS (Meridian Foundation Reserve Case)
# ==============================================================================

# Case Financial Parameters
RESERVE_SIZE = 100.0            # Reserve portfolio size in USD millions
QUARTERLY_DISTRIBUTION = 0.75   # Payout in USD millions every quarter
QUARTERS_TO_COVER = 4           # Twelve months of payouts (4 quarters)
LIQUIDITY_WINDOW = 5            # Liquidity window in business days
MINIMUM_LIQUID_SHARE = 90.0     # Minimum percent redeemable within window
ISSUER_LIMIT = 8.0              # Maximum percent allocated to any single company

# Holdings Reference Table
# Format: (Holding Name, Issuer, Business Days to Redeem, Reserve-Eligible)
HOLDINGS = [
    ("Cash", "none", 0, True),
    ("Treasury bills", "U.S. Treasury", 1, True),
    ("Treasury 10-year note", "U.S. Treasury", 1, True),
    ("Global equity index fund", "diversified fund", 2, False),
    ("Investment-grade bond fund", "diversified fund", 3, False),
    ("Private real estate fund", "diversified fund", 90, False),
    ("Acme Corp bonds", "Acme Corp", 4, False),
    ("Acme Corp stock", "Acme Corp", 1, False),
]

# Issuer Exemptions: Cash, U.S. Treasury, and diversified funds are exempt.
# All securities of one non-exempt company count together toward the 8% limit.
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}

# Candidate Portfolios (Percent Weights)
CANDIDATES = {
    "A": {
        "Cash": 2.0,
        "Treasury bills": 2.0,
        "Treasury 10-year note": 10.0,
        "Global equity index fund": 60.0,
        "Investment-grade bond fund": 26.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 0.0,
    },
    "B": {
        "Cash": 1.0,
        "Treasury bills": 0.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 55.0,
        "Investment-grade bond fund": 20.0,
        "Private real estate fund": 15.0,
        "Acme Corp bonds": 5.0,
        "Acme Corp stock": 4.0,
    },
    "C": {
        "Cash": 1.0,
        "Treasury bills": 1.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 70.0,
        "Investment-grade bond fund": 20.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 8.0,
    },
    # Candidate D: Passes every mechanical checkable rule but offends S4/S9 (Suitability concern)
    "D": {
        "Cash": 3.0,
        "Treasury bills": 0.0,
        "Treasury 10-year note": 0.0,
        "Global equity index fund": 97.0,
        "Investment-grade bond fund": 0.0,
        "Private real estate fund": 0.0,
        "Acme Corp bonds": 0.0,
        "Acme Corp stock": 0.0,
    },
}


# ==============================================================================
# COMPUTATION ENGINE
# ==============================================================================

def calculate_reserve_minimum(quarters: int, distribution: float, reserve_size: float) -> float:
    """Computes reserve minimum: quarters * distribution / reserve_size as a percent."""
    return (quarters * distribution / reserve_size) * 100.0


def evaluate_portfolio(weights: dict, holdings_table: list, reserve_min_pct: float) -> dict:
    """
    Evaluates a candidate portfolio against mandate constraints.
    Returns calculated metrics, status strings, and final rule failure count.
    """
    # Create lookup mappings from holdings table
    issuer_map = {row[0]: row[1] for row in holdings_table}
    days_map = {row[0]: row[2] for row in holdings_table}
    reserve_eligible_map = {row[0]: row[3] for row in holdings_table}

    # 1. Weights sum to 100%
    total_weight = sum(weights.values())
    sum_pass = abs(total_weight - 100.0) < 1e-4

    # 2. Lowest weight not negative (long-only)
    min_weight = min(weights.values())
    long_only_pass = min_weight >= -1e-7

    # 3. Reserve-eligible weight at least reserve minimum
    reserve_weight = sum(w for h, w in weights.items() if reserve_eligible_map.get(h, False))
    reserve_pass = reserve_weight >= (reserve_min_pct - 1e-7)

    # 4. Weight redeemable within liquidity window at least minimum liquid share
    liquid_weight = sum(w for h, w in weights.items() if days_map.get(h, 999) <= LIQUIDITY_WINDOW)
    liquid_pass = liquid_weight >= (MINIMUM_LIQUID_SHARE - 1e-7)

    # 5. Largest single company at most issuer limit (non-exempt issuers aggregated together)
    company_totals = {}
    for h, w in weights.items():
        issuer = issuer_map.get(h, "none")
        if issuer not in EXEMPT_ISSUERS:
            company_totals[issuer] = company_totals.get(issuer, 0.0) + w

    largest_company_weight = max(company_totals.values()) if company_totals else 0.0
    issuer_pass = largest_company_weight <= (ISSUER_LIMIT + 1e-7)

    # Count checkable failures
    checkable_passes = [sum_pass, long_only_pass, reserve_pass, liquid_pass, issuer_pass]
    fails_count = sum(1 for p in checkable_passes if not p)

    if fails_count == 0:
        verdict = "passes every checkable rule"
    else:
        verdict = f"fails {fails_count} rule(s)"

    return {
        "total_weight": total_weight,
        "sum_pass": sum_pass,
        "sum_str": f"{total_weight:.1f} {'pass' if sum_pass else 'FAIL'}",
        "min_weight": min_weight,
        "long_only_pass": long_only_pass,
        "long_only_str": f"{min_weight:.1f} {'pass' if long_only_pass else 'FAIL'}",
        "reserve_weight": reserve_weight,
        "reserve_pass": reserve_pass,
        "reserve_str": f"{reserve_weight:.1f} {'pass' if reserve_pass else 'FAIL'}",
        "liquid_weight": liquid_weight,
        "liquid_pass": liquid_pass,
        "liquid_str": f"{liquid_weight:.1f} {'pass' if liquid_pass else 'FAIL'}",
        "largest_company_weight": largest_company_weight,
        "issuer_pass": issuer_pass,
        "issuer_str": f"{largest_company_weight:.1f} {'pass' if issuer_pass else 'FAIL'}",
        "calendar_loss_str": "requires CIO clarification",
        "fails_count": fails_count,
        "verdict": verdict,
    }


def run_probe_test(reserve_min_pct: float):
    """
    Executes the professor's probe test:
    In Candidate A, set Cash to -2.0% and Global Equity to 64.0%.
    Verifies lowest weight reads -2.0 FAIL, reserve passes at 10.0 pass, and nothing else fails.
    """
    print("\n" + "=" * 78)
    print("MANDATE CHECKER PROBE TEST (Negative Weight Validation)")
    print("=" * 78)
    print("Modifying Candidate A: Cash = -2.0%, Global equity index fund = 64.0%")

    probe_weights = dict(CANDIDATES["A"])
    probe_weights["Cash"] = -2.0
    probe_weights["Global equity index fund"] = 64.0

    res = evaluate_portfolio(probe_weights, HOLDINGS, reserve_min_pct)

    print(f"Weights sum to 100:            {res['sum_str']}")
    print(f"Long-only (lowest weight):     {res['long_only_str']}")
    print(f"Reserve >= {reserve_min_pct:.1f}%:                {res['reserve_str']}")
    print(f"Redeemable in 5 days >= {MINIMUM_LIQUID_SHARE:.0f}%:   {res['liquid_str']}")
    print(f"Largest single company <= {ISSUER_LIMIT:.0f}%: {res['issuer_str']}")
    print(f"Calendar-year loss:            {res['calendar_loss_str']}")
    print(f"Verdict:                       {res['verdict']}")

    expected_probe = (
        res["sum_pass"] is True and
        res["long_only_pass"] is False and
        res["reserve_pass"] is True and
        abs(res["reserve_weight"] - 10.0) < 1e-4 and
        res["liquid_pass"] is True and
        res["issuer_pass"] is True and
        res["fails_count"] == 1
    )
    print("\nProbe Verification Status: " + ("CONFIRMED (Behaves exactly as expected)" if expected_probe else "FAILED"))
    print("=" * 78 + "\n")


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    # 1. Compute and print reserve minimum first
    reserve_min_pct = calculate_reserve_minimum(QUARTERS_TO_COVER, QUARTERLY_DISTRIBUTION, RESERVE_SIZE)
    print(f"Reserve minimum: {reserve_min_pct:.1f}% of the portfolio.\n")

    # 2. Check each candidate portfolio
    results = {}
    for name, weights in CANDIDATES.items():
        results[name] = evaluate_portfolio(weights, HOLDINGS, reserve_min_pct)
        print(f"Candidate {name}:")
        print(f"  Weights sum to 100:          {results[name]['sum_str']}")
        print(f"  Long-only (lowest weight):   {results[name]['long_only_str']}")
        print(f"  Reserve >= {reserve_min_pct:.1f}%:              {results[name]['reserve_str']}")
        print(f"  Redeemable in 5 days >= {MINIMUM_LIQUID_SHARE:.0f}%: {results[name]['liquid_str']}")
        print(f"  Largest single company <= {ISSUER_LIMIT:.0f}%: {results[name]['issuer_str']}")
        print(f"  Calendar-year loss:          {results[name]['calendar_loss_str']}")
        print(f"  Verdict:                     {results[name]['verdict']}\n")

    # 3. Print Side-by-Side Verification Summary Table
    print("-" * 78)
    print("MANDATE DEFENSE VERIFICATION TABLE")
    print("-" * 78)
    header = f"{'Rule':<28} | {'A':<12} | {'B':<12} | {'C':<12} | {'D':<12}"
    print(header)
    print("-" * len(header))
    print(f"{'Weights sum to 100':<28} | {results['A']['sum_str']:<12} | {results['B']['sum_str']:<12} | {results['C']['sum_str']:<12} | {results['D']['sum_str']:<12}")
    print(f"{'Long-only (lowest weight)':<28} | {results['A']['long_only_str']:<12} | {results['B']['long_only_str']:<12} | {results['C']['long_only_str']:<12} | {results['D']['long_only_str']:<12}")
    print(f"{f'Reserve >= {reserve_min_pct:.1f}%':<28} | {results['A']['reserve_str']:<12} | {results['B']['reserve_str']:<12} | {results['C']['reserve_str']:<12} | {results['D']['reserve_str']:<12}")
    print(f"{f'Redeemable in 5 days >= {MINIMUM_LIQUID_SHARE:.0f}%':<28} | {results['A']['liquid_str']:<12} | {results['B']['liquid_str']:<12} | {results['C']['liquid_str']:<12} | {results['D']['liquid_str']:<12}")
    print(f"{f'Largest single company <= {ISSUER_LIMIT:.0f}%':<28} | {results['A']['issuer_str']:<12} | {results['B']['issuer_str']:<12} | {results['C']['issuer_str']:<12} | {results['D']['issuer_str']:<12}")
    print(f"{'Calendar-year loss':<28} | {'requires CIO clarification':<12} | {'same':<12} | {'same':<12} | {'same':<12}")
    print("-" * len(header))
    print(f"{'Verdict':<28} | {results['A']['verdict']:<12} | {results['B']['verdict']:<12} | {results['C']['verdict']:<12} | {results['D']['verdict']:<12}")
    print("-" * 78)

    # 4. Optional Probe Test Execution
    if "--probe" in sys.argv:
        run_probe_test(reserve_min_pct)


if __name__ == "__main__":
    main()

