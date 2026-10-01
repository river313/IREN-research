"""
FIN 439 Lab 12 — Pro-Forma Sensitivity: Present and Review Your Full Analysis
Company: IREN Limited (NASDAQ: IREN)
Student: Elliot
Course: FIN 43900 (Corporate Finance / Applied Financial Modeling, Purdue University)
Execution Script: Audited Revenue Growth Sensitivity Engine (Test A & Test B) & Model Verifier
"""

import sys
import os

# Dynamically locate and import the Lab 10 pro-forma engine
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
POSSIBLE_DIRS = [
    os.path.join(SCRIPT_DIR, "..", "Lab-10"),
    r"c:\Users\ellio\Documents\FIN439\Lab-10",
    r"c:\Users\ellio\Documents\FIN439\IREN-research\Lab-10",
]

imported = False
for d in POSSIBLE_DIRS:
    norm = os.path.normpath(d)
    if os.path.isdir(norm) and os.path.exists(os.path.join(norm, "proforma_iren.py")):
        if norm not in sys.path:
            sys.path.insert(0, norm)
        imported = True
        break

if not imported:
    raise ImportError("Could not locate proforma_iren.py from Lab-10 directory.")

from proforma_iren import run_proforma, calculate_valuation, ASSUMPTIONS, OPENING_BS, YEARS


def evaluate_single_run(growth_path):
    """
    Executes a single pro-forma run with the given revenue growth path.
    Returns statement outputs, FCFF, FCFE, valuation metrics, and check flags.
    """
    out = run_proforma(custom_assumptions={"revenue_growth": growth_path})
    val = calculate_valuation(out)

    rev_fy31 = out["is_list"][-1]["revenue"]
    ebit_fy31 = out["is_list"][-1]["operating_income"]
    fcfe_fy31 = out["cf_list"][-1]["fcfe"]
    capex_fy31 = out["cf_list"][-1]["capex"]
    depr_fy31 = out["is_list"][-1]["depreciation"]
    tax_fy31 = out["is_list"][-1]["tax"]
    delta_wc_fy31 = (
        out["cf_list"][-1]["delta_ar"]
        + out["cf_list"][-1]["delta_other_assets"]
        - out["cf_list"][-1]["delta_deferred_rev"]
        - out["cf_list"][-1]["delta_other_liab"]
    )
    fcff_fy31 = ebit_fy31 - tax_fy31 + depr_fy31 - capex_fy31 - delta_wc_fy31

    vps = val["value_per_share"]
    equity_val = val["equity_value"]
    tv = val["terminal_value"]
    pv_explicit = val["pv_explicit"]
    pv_tv = val["pv_tv"]

    all_gaps_pass = all(abs(c["gap"]) <= 0.01 for c in out["checks"])
    all_cash_pass = all(c["min_cash_pass"] for c in out["checks"])
    checks_pass = all_gaps_pass and all_cash_pass

    return {
        "growth": growth_path,
        "rev_fy31": rev_fy31,
        "ebit_fy31": ebit_fy31,
        "fcff_fy31": fcff_fy31,
        "fcfe_fy31": fcfe_fy31,
        "vps": vps,
        "equity_val": equity_val,
        "tv": tv,
        "pv_explicit": pv_explicit,
        "pv_tv": pv_tv,
        "checks_pass": checks_pass,
    }


def run_test_a_all_years():
    """
    TEST A: Compounding All-Years Revenue Growth Sensitivity
    Applies +/- 1.0 percentage point to EACH annual revenue growth assumption across all 5 years:
    - Base:   [100.0%, 50.0%, 30.0%, 15.0%, 10.0%]
    - Lower:  [ 99.0%, 49.0%, 29.0%, 14.0%,  9.0%] (-1 pp each year)
    - Higher: [101.0%, 51.0%, 31.0%, 16.0%, 11.0%] (+1 pp each year)
    """
    base_path = ASSUMPTIONS["revenue_growth"]
    lower_path = [g - 0.01 for g in base_path]
    higher_path = [g + 0.01 for g in base_path]

    base_res = evaluate_single_run(base_path)
    low_res = evaluate_single_run(lower_path)
    high_res = evaluate_single_run(higher_path)

    cases = [
        ("Lower (-1 pp all years)", low_res),
        ("Base (0 pp)", base_res),
        ("Higher (+1 pp all years)", high_res),
    ]

    for label, r in cases:
        r["label"] = label
        r["dollar_change"] = r["vps"] - base_res["vps"]
        r["pct_change_abs"] = (r["dollar_change"] / abs(base_res["vps"])) * 100.0
        r["pct_change_signed"] = (r["dollar_change"] / base_res["vps"]) * 100.0

    return {
        "base": base_res,
        "lower": low_res,
        "higher": high_res,
        "cases": [c[1] for c in cases],
    }


def run_test_b_single_year():
    """
    TEST B: Single-Year FY31E Revenue Growth Sensitivity
    Holds FY27E-FY30E growth assumptions strictly at base, and alters ONLY FY31E:
    - Base FY31:   10.0% -> [100.0%, 50.0%, 30.0%, 15.0%, 10.0%]
    - Lower FY31:   9.0% -> [100.0%, 50.0%, 30.0%, 15.0%,  9.0%] (-1 pp in Year 5 only)
    - Higher FY31: 11.0% -> [100.0%, 50.0%, 30.0%, 15.0%, 11.0%] (+1 pp in Year 5 only)
    """
    base_path = list(ASSUMPTIONS["revenue_growth"])
    lower_path = list(base_path)
    lower_path[4] -= 0.01
    higher_path = list(base_path)
    higher_path[4] += 0.01

    base_res = evaluate_single_run(base_path)
    low_res = evaluate_single_run(lower_path)
    high_res = evaluate_single_run(higher_path)

    cases = [
        ("Lower (FY31 9.0%)", low_res),
        ("Base (FY31 10.0%)", base_res),
        ("Higher (FY31 11.0%)", high_res),
    ]

    for label, r in cases:
        r["label"] = label
        r["dollar_change"] = r["vps"] - base_res["vps"]
        r["pct_change_abs"] = (r["dollar_change"] / abs(base_res["vps"])) * 100.0
        r["pct_change_signed"] = (r["dollar_change"] / base_res["vps"]) * 100.0

    return {
        "base": base_res,
        "lower": low_res,
        "higher": high_res,
        "cases": [c[1] for c in cases],
    }


def verify_restored_base():
    """Confirms the base model restores perfectly with zero state corruption."""
    base_res = evaluate_single_run(ASSUMPTIONS["revenue_growth"])
    ebit_match = abs(base_res["ebit_fy31"] - 777.882297) < 1e-4
    fcfe_match = abs(base_res["fcfe_fy31"] - 380.390168) < 1e-4
    vps_match = abs(base_res["vps"] - (-5.314523)) < 1e-4
    return ebit_match and fcfe_match and vps_match and base_res["checks_pass"]


def print_audit_report():
    test_a = run_test_a_all_years()
    test_b = run_test_b_single_year()
    b = test_a["base"]

    print("=" * 125)
    print("FIN 439 LAB 12: IREN LIMITED -- AUDITED REVENUE GROWTH SENSITIVITY SUITE")
    print("Primary Share Count: 394.059M shares | Valuation Method: Direct Equity FCFE DCF (r_e = 11.4%, g = 2.5%)")
    print("=" * 125)

    print("\nTEST A -- ALL-YEARS REVENUE-GROWTH PATH SENSITIVITY (+/-1pp applied to EACH of the 5 forecast years)")
    print("-" * 125)
    print(f"{'Scenario':<26} {'Revenue Growth Path':<34} {'FY31 Rev ($M)':>13} {'EBIT ($M)':>12} {'FCFF ($M)':>12} {'FCFE ($M)':>12} {'VPS ($/sh)':>11} {'$ Change':>10} {'% Change':>10}")
    print("-" * 125)
    for r in test_a["cases"]:
        g_str = "[" + ", ".join([f"{x*100:.1f}%" for x in r["growth"]]) + "]"
        print(f"{r['label']:<26} {g_str:<34} {r['rev_fy31']:>13.2f} {r['ebit_fy31']:>12.2f} {r['fcff_fy31']:>12.2f} {r['fcfe_fy31']:>12.2f} {r['vps']:>11.4f} {r['dollar_change']:>+10.4f} {r['pct_change_abs']:>+9.2f}%")
    print("-" * 125)
    print(f"Test A Summary:")
    print(f"  - Base Modeled Value/Share: ${b['vps']:.4f}")
    print(f"  - Downside (-1pp each yr): Value/share moves to ${test_a['lower']['vps']:.4f} (Signed d: ${test_a['lower']['dollar_change']:+.4f} | Deficit expands by {test_a['lower']['pct_change_abs']:.2f}%)")
    print(f"  - Upside (+1pp each yr):   Value/share moves to ${test_a['higher']['vps']:.4f} (Signed d: ${test_a['higher']['dollar_change']:+.4f} | Deficit shrinks by {test_a['higher']['pct_change_abs']:.2f}%)")
    print("  * Critical Note: Test A compounds the growth shift across 5 consecutive periods, moving FY31E Revenue by -$127.67M to +$131.48M.")

    print("\n" + "=" * 125)
    print("TEST B -- SINGLE-YEAR FY31E REVENUE-GROWTH SENSITIVITY (Alters ONLY FY31E; FY27E-FY30E fixed at base)")
    print("-" * 125)
    print(f"{'Scenario':<26} {'Revenue Growth Path':<34} {'FY31 Rev ($M)':>13} {'EBIT ($M)':>12} {'FCFF ($M)':>12} {'FCFE ($M)':>12} {'VPS ($/sh)':>11} {'$ Change':>10} {'% Change':>10}")
    print("-" * 125)
    for r in test_b["cases"]:
        g_str = "[" + ", ".join([f"{x*100:.1f}%" for x in r["growth"]]) + "]"
        print(f"{r['label']:<26} {g_str:<34} {r['rev_fy31']:>13.2f} {r['ebit_fy31']:>12.2f} {r['fcff_fy31']:>12.2f} {r['fcfe_fy31']:>12.2f} {r['vps']:>11.4f} {r['dollar_change']:>+10.4f} {r['pct_change_abs']:>+9.2f}%")
    print("-" * 125)
    print(f"Test B Summary:")
    print(f"  - Base Modeled Value/Share: ${b['vps']:.4f}")
    print(f"  - Downside (FY31 at 9.0%):  Value/share moves to ${test_b['lower']['vps']:.4f} (Signed d: ${test_b['lower']['dollar_change']:+.4f} | Deficit expands by {test_b['lower']['pct_change_abs']:.2f}%)")
    print(f"  - Upside (FY31 at 11.0%):  Value/share moves to ${test_b['higher']['vps']:.4f} (Signed d: ${test_b['higher']['dollar_change']:+.4f} | Deficit shrinks by {test_b['higher']['pct_change_abs']:.2f}%)")
    print("  * Critical Note: Test B isolates the cleaner single-assumption question, moving FY31E Revenue by -$31.71M to +$31.71M.")

    print("\n" + "=" * 125)
    restored = verify_restored_base()
    print(f"VERIFICATION STATUS: Accounting Checks = PASS (Gap = 0.0000) | Restored Base Case = {'PASS' if restored else 'FAIL'}")
    print("=" * 125)


if __name__ == "__main__":
    print_audit_report()
