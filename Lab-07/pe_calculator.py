"""FIN 439 Lab 07: Comparable-Company Valuation Calculator (P/E Multiples).

Case: Asbury Automotive Group (ABG) and Candidate Peers (AN, GPI).
Standard-library only. No external packages. No data fetching.
"""

from __future__ import annotations

import statistics
from typing import Any, Dict, List, Optional, Tuple


# ==============================================================================
# EDITABLE INPUTS (TARGET & PEERS)
# ==============================================================================

# Target company inputs
TARGET_TICKER: str = "ABG"
TARGET_NAME: str = "Asbury Automotive"
TARGET_PRICE: Optional[float] = 243.03  # Dec 31, 2024 closing price ($)
TARGET_EPS: Optional[float] = 21.50    # FY2024 GAAP diluted EPS ($)

# Candidate peer inputs
PEERS: List[Dict[str, Any]] = [
    {
        "ticker": "AN",
        "name": "AutoNation",
        "price": 169.84,
        "eps": 16.92,
    },
    {
        "ticker": "GPI",
        "name": "Group 1 Automotive",
        "price": 421.48,
        "eps": 36.81,
    },
]


# ==============================================================================
# VALUATION ENGINE
# ==============================================================================

def clean_and_validate_peers(
    raw_peers: List[Dict[str, Any]],
    target_ticker: str
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Deduplicate peers, exclude target, and validate price/EPS values.

    Rules:
    1. Exclude peers whose ticker matches target_ticker (case-insensitive).
    2. Deduplicate peers by ticker (keep first occurrence).
    3. Retain full precision; mark missing or nonpositive price/EPS as not meaningful.
    """
    cleaned_peers: List[Dict[str, Any]] = []
    notes: List[str] = []
    seen_tickers: set[str] = set()

    normalized_target = target_ticker.strip().upper()

    for entry in raw_peers:
        ticker = str(entry.get("ticker", "")).strip().upper()
        name = str(entry.get("name", ticker))
        price = entry.get("price")
        eps = entry.get("eps")

        # 1. Target exclusion check
        if ticker == normalized_target:
            notes.append(f"Excluded {ticker} ({name}): target company cannot be in peer set.")
            continue

        # 2. Deduplication check
        if ticker in seen_tickers:
            notes.append(f"Deduplicated {ticker} ({name}): duplicate peer ticker ignored.")
            continue
        seen_tickers.add(ticker)

        # 3. Validation check: price and EPS must be positive numbers
        is_valid = True
        status_reason = "Valid"

        if price is None or eps is None:
            is_valid = False
            status_reason = "Not meaningful (missing price or EPS)"
        elif not isinstance(price, (int, float)) or not isinstance(eps, (int, float)):
            is_valid = False
            status_reason = "Not meaningful (price and EPS must be numeric)"
        elif price <= 0 or eps <= 0:
            is_valid = False
            reasons = []
            if price <= 0:
                reasons.append(f"price ${price} <= 0")
            if eps <= 0:
                reasons.append(f"EPS ${eps} <= 0")
            status_reason = f"Not meaningful ({', '.join(reasons)})"

        pe = (price / eps) if is_valid else None

        cleaned_peers.append({
            "ticker": ticker,
            "name": name,
            "price": price,
            "eps": eps,
            "is_valid": is_valid,
            "status_reason": status_reason,
            "pe": pe,
        })

    return cleaned_peers, notes


def compute_peer_multiples(
    valid_peers: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Compute summary P/E statistics (min, median, max) across valid peers."""
    n = len(valid_peers)
    if n == 0:
        return {
            "count": 0,
            "min_pe": None,
            "median_pe": None,
            "max_pe": None,
        }

    pe_list = [p["pe"] for p in valid_peers]
    return {
        "count": n,
        "min_pe": min(pe_list),
        "median_pe": statistics.median(pe_list),
        "max_pe": max(pe_list),
    }


def compute_implied_target_valuation(
    target_eps: Optional[float],
    summary_stats: Dict[str, Any]
) -> Dict[str, Any]:
    """Calculate implied target prices from peer multiples without cash/debt bridge."""
    if target_eps is None or target_eps <= 0:
        return {
            "status": "Target EPS is missing or nonpositive; implied valuation not meaningful.",
            "implied_min": None,
            "implied_median": None,
            "implied_max": None,
        }

    count = summary_stats["count"]
    if count == 0:
        return {
            "status": "No usable peer estimate (zero valid peers).",
            "implied_min": None,
            "implied_median": None,
            "implied_max": None,
        }

    min_pe = summary_stats["min_pe"]
    med_pe = summary_stats["median_pe"]
    max_pe = summary_stats["max_pe"]

    return {
        "status": "OK",
        "implied_min": min_pe * target_eps,
        "implied_median": med_pe * target_eps,
        "implied_max": max_pe * target_eps,
    }


def compute_leave_one_out(
    valid_peers: List[Dict[str, Any]],
    target_eps: Optional[float],
    full_peer_median_price: Optional[float]
) -> List[Dict[str, Any]]:
    """Calculate leave-one-out sensitivity for each valid peer.

    For each removed peer:
      - Compute remaining peer median P/E.
      - Calculate remaining implied target price.
      - Calculate unrounded dollar change vs full-peer median estimate.
    """
    results: List[Dict[str, Any]] = []

    if target_eps is None or target_eps <= 0:
        return results

    for removed_peer in valid_peers:
        remaining = [p for p in valid_peers if p["ticker"] != removed_peer["ticker"]]
        rem_count = len(remaining)

        if rem_count == 0:
            results.append({
                "removed_ticker": removed_peer["ticker"],
                "removed_name": removed_peer["name"],
                "remaining_count": 0,
                "remaining_median_pe": None,
                "remaining_implied_price": None,
                "dollar_change": None,
                "status": "No estimate (no remaining peers)",
            })
        else:
            rem_pes = [p["pe"] for p in remaining]
            rem_med_pe = statistics.median(rem_pes)
            rem_implied_price = rem_med_pe * target_eps
            dollar_change = (
                rem_implied_price - full_peer_median_price
                if full_peer_median_price is not None else None
            )

            results.append({
                "removed_ticker": removed_peer["ticker"],
                "removed_name": removed_peer["name"],
                "remaining_count": rem_count,
                "remaining_peers": [p["ticker"] for p in remaining],
                "remaining_median_pe": rem_med_pe,
                "remaining_implied_price": rem_implied_price,
                "dollar_change": dollar_change,
                "status": "OK",
            })

    return results


# ==============================================================================
# REPORTING & DISPLAY
# ==============================================================================

def run_valuation() -> None:
    """Execute valuation, run validation checks, and print structured report."""
    print("=" * 78)
    print("FIN 439 LAB 07: COMPARABLE-COMPANY VALUATION (P/E MULTIPLES)")
    print("=" * 78)

    # 1. Target Summary
    print("\n1. TARGET COMPANY INPUTS")
    print(f"   Company: {TARGET_NAME} ({TARGET_TICKER})")
    if TARGET_PRICE is not None:
        print(f"   Market Closing Price (12/31/2024): ${TARGET_PRICE:.2f}")
    else:
        print("   Market Closing Price: None")

    if TARGET_EPS is not None and TARGET_EPS > 0:
        print(f"   FY2024 GAAP Diluted EPS: ${TARGET_EPS:.2f}")
        abg_pe = (TARGET_PRICE / TARGET_EPS) if TARGET_PRICE and TARGET_PRICE > 0 else None
        if abg_pe:
            print(f"   Target's Own Actual P/E: {abg_pe:.6f}x")
    else:
        print(f"   FY2024 GAAP Diluted EPS: {TARGET_EPS} (Not meaningful for P/E valuation)")

    # 2. Peer Processing
    all_processed, audit_notes = clean_and_validate_peers(PEERS, TARGET_TICKER)
    valid_peers = [p for p in all_processed if p["is_valid"]]

    print("\n2. CANDIDATE PEER AUDIT & P/E MULTIPLES")
    if audit_notes:
        for note in audit_notes:
            print(f"   [Audit] {note}")

    print(f"   {'Ticker':<8} {'Name':<24} {'Price':<10} {'EPS':<10} {'P/E Multiple':<16} {'Status'}")
    print("   " + "-" * 74)
    for p in all_processed:
        price_str = f"${p['price']:.2f}" if isinstance(p['price'], (int, float)) else str(p['price'])
        eps_str = f"${p['eps']:.2f}" if isinstance(p['eps'], (int, float)) else str(p['eps'])
        pe_str = f"{p['pe']:.6f}x" if p['pe'] is not None else "N/A"
        print(f"   {p['ticker']:<8} {p['name']:<24} {price_str:<10} {eps_str:<10} {pe_str:<16} {p['status_reason']}")

    # 3. Peer Multiples Summary
    stats = compute_peer_multiples(valid_peers)
    n_valid = stats["count"]
    print(f"\n3. PEER MULTIPLE SUMMARY ({n_valid} valid peer{'s' if n_valid != 1 else ''})")

    if n_valid == 0:
        print("   [!] No usable peers available. Cannot compute multiple summary.")
    elif n_valid == 1:
        print(f"   Reference Peer P/E: {stats['median_pe']:.6f}x")
        print("   Notice: With only 1 valid peer, a reference estimate is generated without a range.")
    else:
        print(f"   Peer Minimum P/E: {stats['min_pe']:.6f}x")
        print(f"   Peer Median P/E:  {stats['median_pe']:.6f}x")
        print(f"   Peer Maximum P/E: {stats['max_pe']:.6f}x")

    # 4. Implied Valuation
    val = compute_implied_target_valuation(TARGET_EPS, stats)
    print("\n4. IMPLIED TARGET VALUATION (P/E x Target EPS)")
    print("   Note: P/E is an equity multiple; enterprise debt and cash are never bridged.")

    if val["status"] != "OK":
        print(f"   Status: {val['status']}")
    else:
        if n_valid == 1:
            print(f"   Single Peer Reference Implied Price: ${val['implied_median']:.2f}")
            print("   Implied Range: None (requires >= 2 valid peers)")
        else:
            print(f"   Implied Target Price Range: ${val['implied_min']:.2f} to ${val['implied_max']:.2f}")
            print(f"   Implied Target at Peer Median: ${val['implied_median']:.2f}")
            if TARGET_PRICE is not None:
                diff = TARGET_PRICE - val['implied_median']
                pct = (diff / val['implied_median']) * 100.0
                sign = "+" if diff >= 0 else "-"
                print(f"   Target Actual Price vs Peer Median: ${TARGET_PRICE:.2f} vs ${val['implied_median']:.2f} "
                      f"({sign}${abs(diff):.2f} or {pct:+.2f}%)")

    # 5. Leave-One-Out Sensitivity Analysis
    print("\n5. LEAVE-ONE-OUT SENSITIVITY ANALYSIS")
    print("   Evaluating target implied price if one peer is excluded:")
    loo_results = compute_leave_one_out(valid_peers, TARGET_EPS, val["implied_median"])

    if not loo_results:
        print("   No leave-one-out sensitivity possible.")
    else:
        for r in loo_results:
            rem_ticker = r["removed_ticker"]
            rem_name = r["removed_name"]
            if r["remaining_count"] == 0:
                print(f"   Remove {rem_ticker} ({rem_name}): {r['status']}")
            elif r["remaining_count"] == 1:
                other_ticker = r["remaining_peers"][0]
                price = r["remaining_implied_price"]
                delta = r["dollar_change"]
                sign = "+" if delta >= 0 else "-"
                print(f"   Remove {rem_ticker} ({rem_name}):")
                print(f"     Remaining Peer: {other_ticker} (Reference Multiple = {r['remaining_median_pe']:.6f}x)")
                print(f"     Remaining Target Estimate: ${price:.2f}")
                print(f"     Change from Full Two-Peer Median: {sign}${abs(delta):.2f}")
            else:
                price = r["remaining_implied_price"]
                delta = r["dollar_change"]
                sign = "+" if delta >= 0 else "-"
                print(f"   Remove {rem_ticker} ({rem_name}):")
                print(f"     Remaining Peers: {', '.join(r['remaining_peers'])} "
                      f"(Median P/E = {r['remaining_median_pe']:.6f}x)")
                print(f"     Remaining Implied Target Price: ${price:.2f}")
                print(f"     Change from Full Peer Median: {sign}${abs(delta):.2f}")

    # 6. Automated Validation Check Against Course Benchmarks
    print("\n" + "=" * 78)
    print("6. CASE VALIDATION BENCHMARK CHECKS")
    print("=" * 78)

    expected_checks = [
        ("AutoNation P/E", 10.037825, next((p["pe"] for p in valid_peers if p["ticker"] == "AN"), None), 6),
        ("Group 1 P/E", 11.450149, next((p["pe"] for p in valid_peers if p["ticker"] == "GPI"), None), 6),
        ("Peer median P/E", 10.743987, stats["median_pe"], 6),
        ("Asbury peer-implied min", 215.81, val["implied_min"], 2),
        ("Asbury peer-implied max", 246.18, val["implied_max"], 2),
        ("Asbury at peer median", 231.00, val["implied_median"], 2),
    ]

    # Find leave-one-out for GPI
    loo_gpi = next((r for r in loo_results if r["removed_ticker"] == "GPI"), None)
    if loo_gpi:
        expected_checks.append(
            ("Remove GPI: remaining AN estimate", 215.81, loo_gpi["remaining_implied_price"], 2)
        )
        expected_checks.append(
            ("Remove GPI: change from midpoint", -15.18, loo_gpi["dollar_change"], 2)
        )

    # Find leave-one-out for AN
    loo_an = next((r for r in loo_results if r["removed_ticker"] == "AN"), None)
    if loo_an:
        expected_checks.append(
            ("Remove AN: remaining GPI estimate", 246.18, loo_an["remaining_implied_price"], 2)
        )
        expected_checks.append(
            ("Remove AN: change from midpoint", 15.18, loo_an["dollar_change"], 2)
        )

    all_passed = True
    for label, expected, actual, decimals in expected_checks:
        if actual is None:
            status = "FAILED (Missing)"
            all_passed = False
            print(f"   [FAIL] {label:<36}: Expected {expected}, got None")
        else:
            diff = abs(actual - expected)
            tolerance = 10 ** (-decimals) / 2 + 1e-6
            is_close = diff < tolerance
            if is_close:
                fmt = f".{decimals}f"
                print(f"   [PASS] {label:<36}: Expected {expected:{fmt}}, Calculated {actual:{fmt}} (Match)")
            else:
                all_passed = False
                print(f"   [FAIL] {label:<36}: Expected {expected}, Calculated {actual} (Diff = {diff})")

    print("-" * 78)
    if all_passed:
        print("   >>> ALL CASE VALIDATION CHECKS PASSED SUCCESSFULLY. <<<")
    else:
        print("   >>> SOME VALIDATION CHECKS FAILED. PLEASE REVIEW. <<<")
    print("=" * 78)


if __name__ == "__main__":
    run_valuation()
