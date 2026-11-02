"""
run_tests.py - Comprehensive Test Suite for FIN 439 Lab 18
Verifies all professor requirements, reference numbers, missing-data handling,
and unsupported-number detection.
"""

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import buffett_sec

def test_costco_reference():
    print("=" * 70)
    print("TEST 1: Costco (COST) Reference Table Validation")
    print("=" * 70)

    # Professor's exact reference table
    expected_table = {
        "2022-08-28": {"rev": 226954, "ni": 5844, "ocf": 7392, "capex": 3891, "eq": 20642, "roe": 0.283, "oe": 3501},
        "2023-09-03": {"rev": 242290, "ni": 6292, "ocf": 11068, "capex": 4323, "eq": 25058, "roe": 0.251, "oe": 6745},
        "2024-09-01": {"rev": 254453, "ni": 7367, "ocf": 11339, "capex": 4710, "eq": 23622, "roe": 0.312, "oe": 6629},
        "2025-08-31": {"rev": 275235, "ni": 8099, "ocf": 13335, "capex": 5498, "eq": 29164, "roe": 0.278, "oe": 7837},
        "2026-08-30": {"rev": 303154, "ni": 9226, "ocf": 15817, "capex": 6435, "eq": 35803, "roe": 0.258, "oe": 9382},
    }

    cache_dir = os.path.join(current_dir, "data_cache")
    cik, title = buffett_sec.lookup_cik("COST", cache_dir=cache_dir)
    facts = buffett_sec.fetch_company_facts(cik, cache_dir=cache_dir)
    tags, rows = buffett_sec.extract_buffett_metrics(facts)
    checks = buffett_sec.evaluate_buffett_checks(rows)

    mismatches = []
    print(f"{'End Date':<12} | {'Metric':<18} | {'Retrieved':>12} | {'Expected':>12} | {'Status':>8}")
    print("-" * 70)

    for r in rows:
        d = r["fiscal_year_end"]
        if d not in expected_table:
            mismatches.append(f"Unexpected date {d}")
            continue
        exp = expected_table[d]

        # Check Revenue
        rev_m = round(r["revenue"] / 1e6)
        status_rev = "MATCH" if rev_m == exp["rev"] else "MISMATCH"
        print(f"{d:<12} | {'Revenue ($M)':<18} | {rev_m:>12,d} | {exp['rev']:>12,d} | {status_rev:>8}")
        if status_rev == "MISMATCH":
            mismatches.append(f"{d} Revenue: got {rev_m}, expected {exp['rev']}")

        # Check Net Income
        ni_m = round(r["net_income"] / 1e6)
        status_ni = "MATCH" if ni_m == exp["ni"] else "MISMATCH"
        print(f"{d:<12} | {'Net Income ($M)':<18} | {ni_m:>12,d} | {exp['ni']:>12,d} | {status_ni:>8}")
        if status_ni == "MISMATCH":
            mismatches.append(f"{d} Net Income: got {ni_m}, expected {exp['ni']}")

        # Check OCF
        ocf_m = round(r["operating_cash_flow"] / 1e6)
        status_ocf = "MATCH" if ocf_m == exp["ocf"] else "MISMATCH"
        print(f"{d:<12} | {'Oper Cash Flow ($M)':<18} | {ocf_m:>12,d} | {exp['ocf']:>12,d} | {status_ocf:>8}")
        if status_ocf == "MISMATCH":
            mismatches.append(f"{d} OCF: got {ocf_m}, expected {exp['ocf']}")

        # Check CapEx
        capex_m = round(r["capex"] / 1e6)
        status_capex = "MATCH" if capex_m == exp["capex"] else "MISMATCH"
        print(f"{d:<12} | {'CapEx ($M)':<18} | {capex_m:>12,d} | {exp['capex']:>12,d} | {status_capex:>8}")
        if status_capex == "MISMATCH":
            mismatches.append(f"{d} CapEx: got {capex_m}, expected {exp['capex']}")

        # Check Equity
        eq_m = round(r["equity"] / 1e6)
        status_eq = "MATCH" if eq_m == exp["eq"] else "MISMATCH"
        print(f"{d:<12} | {'Equity ($M)':<18} | {eq_m:>12,d} | {exp['eq']:>12,d} | {status_eq:>8}")
        if status_eq == "MISMATCH":
            mismatches.append(f"{d} Equity: got {eq_m}, expected {exp['eq']}")

        # Check ROE
        roe_pct = round(r["roe"], 3)
        status_roe = "MATCH" if roe_pct == exp["roe"] else "MISMATCH"
        print(f"{d:<12} | {'ROE':<18} | {roe_pct*100:>11.1f}% | {exp['roe']*100:>11.1f}% | {status_roe:>8}")
        if status_roe == "MISMATCH":
            mismatches.append(f"{d} ROE: got {roe_pct}, expected {exp['roe']}")

        # Check Owner Earnings
        oe_m = round(r["owner_earnings"] / 1e6)
        status_oe = "MATCH" if oe_m == exp["oe"] else "MISMATCH"
        print(f"{d:<12} | {'Owner Earnings ($M)':<18} | {oe_m:>12,d} | {exp['oe']:>12,d} | {status_oe:>8}")
        if status_oe == "MISMATCH":
            mismatches.append(f"{d} Owner Earnings: got {oe_m}, expected {exp['oe']}")

    print("-" * 70)
    print("Buffett Checks:")
    print(f"  Check 1 (ROE >= 15%): {checks['check1']['status']} (Expected: PASS)")
    print(f"  Check 2 (Owner Earnings > 0): {checks['check2']['status']} (Expected: PASS)")
    print(f"  Check 3 (Owner Earnings Growth): {checks['check3']['status']} (Expected: PASS)")

    assert len(mismatches) == 0, f"Found mismatches: {mismatches}"
    assert checks["check1"]["status"] == "PASS"
    assert checks["check2"]["status"] == "PASS"
    assert checks["check3"]["status"] == "PASS"
    print("\n>>> TEST 1 RESULT: ALL 35 COSTCO NUMBERS AND CHECKS MATCH EXACTLY (PASS)\n")


def test_jpmorgan_missing_data():
    print("=" * 70)
    print("TEST 2: JPMorgan (JPM) Missing-Data Handling")
    print("=" * 70)
    cache_dir = os.path.join(current_dir, "data_cache")
    cik, title = buffett_sec.lookup_cik("JPM", cache_dir=cache_dir)
    facts = buffett_sec.fetch_company_facts(cik, cache_dir=cache_dir)
    tags, rows = buffett_sec.extract_buffett_metrics(facts)
    checks = buffett_sec.evaluate_buffett_checks(rows)

    print(f"CapEx Tag: {tags.get('CapEx')}")
    print(f"Check 1 (ROE): {checks['check1']['status']}")
    print(f"Check 2 (Owner Earnings > 0): {checks['check2']['status']}")
    print(f"Check 3 (Owner Earnings Growth): {checks['check3']['status']}")

    assert tags.get("CapEx") == "not found", f"Expected CapEx 'not found', got {tags.get('CapEx')}"
    for r in rows:
        assert r["capex"] is None, f"Expected CapEx None, got {r['capex']}"
        assert r["owner_earnings"] == "not found", f"Expected Owner Earnings 'not found', got {r['owner_earnings']}"

    assert checks["check2"]["status"] == "NOT KNOWN", f"Expected Check 2 NOT KNOWN, got {checks['check2']['status']}"
    assert checks["check3"]["status"] == "NOT KNOWN", f"Expected Check 3 NOT KNOWN, got {checks['check3']['status']}"

    # Verify JPM memo acknowledges missing Owner Earnings and contains no fabricated figures
    jpm_memo = buffett_sec.generate_investment_memo("JPM", title, rows, tags, checks)
    assert "owner earnings cannot be evaluated" in jpm_memo.lower(), "JPM memo must acknowledge owner earnings cannot be evaluated"
    jpm_flags = buffett_sec.detect_unsupported_numbers(jpm_memo, rows)
    assert len(jpm_flags) == 0, f"JPM memo contained unexpected unsupported numbers: {jpm_flags}"
    print(f"JPM Memo Check: Successfully generated ticker-specific memo with 0 unsupported flags.")

    print("\n>>> TEST 2 RESULT: JPMORGAN MISSING-DATA HANDLING VERIFIED (PASS)\n")


def test_fabricated_number_detection():
    print("=" * 70)
    print("TEST 3: Unsupported / Fabricated Number Detection")
    print("=" * 70)
    cache_dir = os.path.join(current_dir, "data_cache")
    cik, _ = buffett_sec.lookup_cik("COST", cache_dir=cache_dir)
    facts = buffett_sec.fetch_company_facts(cik, cache_dir=cache_dir)
    tags, rows = buffett_sec.extract_buffett_metrics(facts)
    checks = buffett_sec.evaluate_buffett_checks(rows)
    memo = buffett_sec.generate_costco_investment_memo(rows, tags, checks)

    # 1. Clean memo must have 0 flags
    clean_flags = buffett_sec.detect_unsupported_numbers(memo, rows)
    print(f"Clean memo flags count: {len(clean_flags)}")
    assert len(clean_flags) == 0, f"Clean memo contained unexpected flags: {clean_flags}"

    # 2. Fabricated memo with 'ROE was 40.0%.' must flag '40.0%'
    fabricated_memo = memo + "\n\nAccording to an unverified report, Costco's ROE was 40.0% in 2024.\n"
    fab_flags = buffett_sec.detect_unsupported_numbers(fabricated_memo, rows)
    print(f"Fabricated memo flags count: {len(fab_flags)}")
    print(f"Detected flags: {fab_flags}")

    tokens = [f["token"] for f in fab_flags]
    assert any("40.0%" in t for t in tokens), f"Detector failed to flag 40.0%: {tokens}"
    print("\n>>> TEST 3 RESULT: FABRICATED NUMBER DETECTOR VERIFIED (PASS)\n")


if __name__ == "__main__":
    test_costco_reference()
    test_jpmorgan_missing_data()
    test_fabricated_number_detection()
    print("=" * 70)
    print("ALL FIN 439 LAB 18 AUTOMATED TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)

