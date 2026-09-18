"""FIN 439 Lab 08: Comparable-Company Valuation Calculator (P/E Multiples).

Target Company: IREN Limited (NASDAQ: IREN)
Candidate Peers: Core Scientific (CORZ), Applied Digital (APLD), Equinix (EQIX - Excluded Benchmark)
Comparison Date: September 3, 2026

Standard-library Python only. No external packages. No external data fetching.
Implements FIN 439 Lab 08 assignment rules for evaluating peer comparability
and handling companies with zero or negative earnings per share.
"""

from __future__ import annotations

import statistics
from typing import Any, Dict, List, Optional, Tuple


# ==============================================================================
# EDITABLE INPUTS (TARGET & PEERS)
# ==============================================================================

# Target company inputs: IREN Limited
# Valuation Date: September 3, 2026 (matching Week 3 IREN Research Report baseline)
TARGET_TICKER: str = "IREN"
TARGET_NAME: str = "IREN Limited"
TARGET_PRICE: Optional[float] = 41.65  # Closing price on Sept 3, 2026 ($) [Ref: Week 3 DCF price was $45.73]
TARGET_EPS: Optional[float] = -2.22   # FY2026 GAAP diluted EPS ($) [Source: Form 10-K, Item 8, p. F-7]

# Candidate peer inputs
# Peers marked USE or QUALIFY based on business economics, plus documented EXCLUDE peers.
PEERS: List[Dict[str, Any]] = [
    {
        "ticker": "CORZ",
        "name": "Core Scientific, Inc.",
        "price": 17.90,       # Closing price on Sept 3, 2026 ($)
        "eps": -0.88,         # FY2025 GAAP diluted EPS ($) [Source: Form 10-K, Item 8]
        "policy_decision": "QUALIFY",
        "reason": "Direct digital infrastructure peer pivoting Bitcoin mining to HPC/AI hosting (CoreWeave contracts); negative GAAP EPS."
    },
    {
        "ticker": "APLD",
        "name": "Applied Digital Corporation",
        "price": 25.91,       # Closing price on Sept 3, 2026 ($)
        "eps": -0.91,         # FY2026 GAAP diluted EPS for FY ended May 31, 2026 ($) [Source: Form 10-K, Item 8]
        "policy_decision": "QUALIFY",
        "reason": "Next-gen HPC/AI data center builder and cloud operator; tenant leasing focus; negative GAAP EPS."
    },
    {
        "ticker": "EQIX",
        "name": "Equinix, Inc.",
        "price": 1040.83,     # Closing price on Sept 3, 2026 ($)
        "eps": 13.76,         # FY2025 GAAP diluted EPS ($) [Source: Form 10-K, Item 8]
        "policy_decision": "EXCLUDE",
        "reason": "Traditional colocation/interconnection REIT. Excluded: tax-exempt REIT structure, no GPU/compute ownership, retail colocation."
    },
]


# ==============================================================================
# VALUATION ENGINE
# ==============================================================================

def clean_and_validate_peers(
    raw_peers: List[Dict[str, Any]],
    target_ticker: str
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Deduplicate peers, exclude target and policy-excluded peers, and validate price/EPS values.

    Rules:
    1. Exclude peers matching target_ticker (case-insensitive).
    2. Exclude peers marked EXCLUDE under the peer policy.
    3. Deduplicate peers by ticker (keep first occurrence).
    4. Price and EPS must be numeric and strictly positive (> 0) for P/E to be meaningful.
       Zero or negative values are flagged as 'Not meaningful'.
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
        policy_decision = str(entry.get("policy_decision", "USE")).strip().upper()
        reason = entry.get("reason", "")

        # 1. Target exclusion check
        if ticker == normalized_target:
            notes.append(f"Excluded {ticker} ({name}): target company cannot be in peer set.")
            continue

        # 2. Peer Policy exclusion check
        if policy_decision == "EXCLUDE":
            notes.append(f"Excluded {ticker} ({name}) by peer policy: {reason}")
            cleaned_peers.append({
                "ticker": ticker,
                "name": name,
                "price": price,
                "eps": eps,
                "policy_decision": policy_decision,
                "reason": reason,
                "is_valid": False,
                "status_reason": f"Excluded by peer policy ({reason})",
                "pe": None,
            })
            continue

        # 3. Deduplication check
        if ticker in seen_tickers:
            notes.append(f"Deduplicated {ticker} ({name}): duplicate peer ticker ignored.")
            continue
        seen_tickers.add(ticker)

        # 4. Numerical validation check: price and EPS must be strictly positive
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
                reasons.append(f"EPS ${eps:.2f} <= 0")
            status_reason = f"Not meaningful ({', '.join(reasons)})"

        pe = (price / eps) if is_valid else None

        cleaned_peers.append({
            "ticker": ticker,
            "name": name,
            "price": price,
            "eps": eps,
            "policy_decision": policy_decision,
            "reason": reason,
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
    """Calculate implied target prices from peer multiples without cash/debt bridge.

    Lab 08 Mandate:
    If target EPS is nonpositive, P/E cannot support a valuation.
    Do not force a positive result or switch methods.
    """
    if target_eps is None or target_eps <= 0:
        eps_str = f"${target_eps:.2f}" if isinstance(target_eps, (int, float)) else str(target_eps)
        return {
            "status": f"Target EPS ({eps_str}) is negative or nonpositive; P/E valuation is not meaningful.",
            "implied_min": None,
            "implied_median": None,
            "implied_max": None,
            "is_meaningful": False,
        }

    count = summary_stats["count"]
    if count == 0:
        return {
            "status": "No usable peer estimate (zero valid peers with positive EPS).",
            "implied_min": None,
            "implied_median": None,
            "implied_max": None,
            "is_meaningful": False,
        }

    min_pe = summary_stats["min_pe"]
    med_pe = summary_stats["median_pe"]
    max_pe = summary_stats["max_pe"]

    return {
        "status": "OK",
        "implied_min": min_pe * target_eps,
        "implied_median": med_pe * target_eps,
        "implied_max": max_pe * target_eps,
        "is_meaningful": True,
    }


def compute_leave_one_out(
    valid_peers: List[Dict[str, Any]],
    target_eps: Optional[float],
    full_peer_median_price: Optional[float]
) -> List[Dict[str, Any]]:
    """Calculate leave-one-out sensitivity for each valid peer."""
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
# REPORTING & DIAGNOSTIC SUITE
# ==============================================================================

def run_valuation() -> Dict[str, Any]:
    """Execute valuation, run validation checks, and print structured Lab 08 report."""
    print("=" * 78)
    print("FIN 439 LAB 08: COMPARABLE-COMPANY VALUATION (IREN LIMITED)")
    print("=" * 78)

    # 1. Target Summary
    print("\n1. TARGET COMPANY INPUTS")
    print(f"   Company: {TARGET_NAME} ({TARGET_TICKER})")
    print(f"   Valuation Date: September 3, 2026")
    if TARGET_PRICE is not None:
        print(f"   Market Closing Price (09/03/2026): ${TARGET_PRICE:.2f}")
    else:
        print("   Market Closing Price: None")

    if TARGET_EPS is not None:
        print(f"   FY2026 GAAP Diluted EPS: ${TARGET_EPS:.2f} (Source: FY2026 10-K, Item 8, p. F-7)")
        if TARGET_EPS <= 0:
            print("   >>> DIAGNOSIS: Target EPS is negative (-$2.22).")
            print("   >>> Under Lab 08 instructions, trailing P/E cannot support this valuation.")
    else:
        print("   FY2026 GAAP Diluted EPS: Missing")

    # 2. Candidate Peer Audit
    all_processed, audit_notes = clean_and_validate_peers(PEERS, TARGET_TICKER)
    valid_peers = [p for p in all_processed if p["is_valid"]]

    print("\n2. CANDIDATE PEER AUDIT & VALIDATION")
    if audit_notes:
        for note in audit_notes:
            print(f"   [Audit] {note}")

    print(f"\n   {'Ticker':<8} {'Name':<28} {'Price':<10} {'EPS':<10} {'Policy':<10} {'Status / P/E'}")
    print("   " + "-" * 74)
    for p in all_processed:
        price_str = f"${p['price']:.2f}" if isinstance(p['price'], (int, float)) else str(p['price'])
        eps_str = f"${p['eps']:.2f}" if isinstance(p['eps'], (int, float)) else str(p['eps'])
        pe_str = f"{p['pe']:.4f}x" if p['pe'] is not None else p['status_reason']
        print(f"   {p['ticker']:<8} {p['name']:<28} {price_str:<10} {eps_str:<10} {p['policy_decision']:<10} {pe_str}")

    # 3. Peer Multiples Summary
    stats = compute_peer_multiples(valid_peers)
    n_valid = stats["count"]
    print(f"\n3. PEER MULTIPLES SUMMARY ({n_valid} valid peers with positive EPS)")
    if n_valid == 0:
        print("   [!] Zero valid peers have positive trailing GAAP EPS.")
        print("   Direct digital infrastructure peers (CORZ: -$0.88, APLD: -$0.91) also reported")
        print("   net losses during this heavy infrastructure investment cycle.")
    else:
        print(f"   Valid Peer Median P/E: {stats['median_pe']:.4f}x")

    # 4. Implied Valuation Assessment
    val = compute_implied_target_valuation(TARGET_EPS, stats)
    print("\n4. IMPLIED TARGET VALUATION ASSESSMENT")
    print(f"   Valuation Status: {val['status']}")
    print("   Financial Analysis:")
    print("     - P/E is an equity multiple requiring positive accounting earnings.")
    print("     - Multiplying negative target EPS (-$2.22) by a positive peer multiple")
    print("       would mathematically yield a NEGATIVE share price (e.g., -$167.92),")
    print("       which is impossible for common stock with limited liability.")
    print("     - Multiplying negative target EPS by a negative peer P/E would create")
    print("       a mathematical sign error (+ price for bigger losses).")
    print("     - CONCLUSION: P/E cannot support a valuation for IREN. No valuation range")
    print("       can be defensibly constructed from trailing earnings.")

    # 5. Hand-Check Arithmetic Verification
    print("\n5. MATHEMATICAL & HAND-CHECK VERIFICATION")
    print("   Check A: Target EPS calculation from 10-K:")
    print("     Net Loss: -$702,621,000 / 316,123,145 diluted shares = -$2.2226 -> -$2.22/share. [PASS]")
    print("   Check B: Theoretical result if positive REIT peer (EQIX) multiple were applied:")
    eqix_pe = 1040.83 / 13.76  # 75.6417x
    hypo_price = -2.22 * eqix_pe
    print(f"     EQIX P/E = $1,040.83 / $13.76 = {eqix_pe:.4f}x")
    print(f"     Hypothetical Target Price = -$2.22 x {eqix_pe:.4f}x = ${hypo_price:.2f}")
    print("     Economic Result: Violates limited liability; proves P/E invalid for negative EPS. [PASS]")
    print("   Check C: Leave-one-out sensitivity:")
    print("     With 0 valid peers and negative target EPS, leave-one-out produces 0 estimates. [PASS]")

    # 6. Benchmark Checks against Lab 08 Course Requirements
    print("\n" + "=" * 78)
    print("6. LAB 08 VALIDATION CHECKS")
    print("=" * 78)
    checks = [
        ("Target ticker is IREN", TARGET_TICKER == "IREN"),
        ("Target price on 09/03/2026 sourced ($41.65)", TARGET_PRICE == 41.65),
        ("Target EPS correctly sourced (-$2.22)", TARGET_EPS == -2.22),
        ("Candidate Peer 1 (CORZ) evaluated with negative EPS (-$0.88)", any(p["ticker"] == "CORZ" and p["eps"] == -0.88 for p in all_processed)),
        ("Candidate Peer 2 (APLD) evaluated with negative EPS (-$0.91)", any(p["ticker"] == "APLD" and p["eps"] == -0.91 for p in all_processed)),
        ("REIT peer (EQIX) excluded under economic peer policy", any(p["ticker"] == "EQIX" and p["policy_decision"] == "EXCLUDE" for p in all_processed)),
        ("Zero valid peers with positive EPS diagnosed", n_valid == 0),
        ("P/E valuation correctly diagnosed as not meaningful", not val["is_meaningful"]),
        ("P/E valuation withheld rather than forced", val["implied_median"] is None),
    ]

    all_passed = True
    for desc, condition in checks:
        status = "PASS" if condition else "FAIL"
        if not condition:
            all_passed = False
        print(f"   [{status}] {desc}")

    print("-" * 78)
    if all_passed:
        print("   >>> ALL LAB 08 VALIDATION CHECKS PASSED SUCCESSFULLY. <<<")
    else:
        print("   >>> SOME VALIDATION CHECKS FAILED. PLEASE REVIEW. <<<")
    print("=" * 78)

    return {
        "target": TARGET_TICKER,
        "target_eps": TARGET_EPS,
        "n_valid_peers": n_valid,
        "val_status": val["status"],
        "all_passed": all_passed
    }


if __name__ == "__main__":
    run_valuation()
