"""
FIN 439 Lab 12 — Pro-Forma Sensitivity: Present and Review Your Full Analysis
Company: IREN Limited (NASDAQ: IREN)
Student: Elliot
Course: FIN 43900 (Corporate Finance / Applied Financial Modeling, Purdue University)
Execution Script: ±1 Percentage-Point Revenue Growth Sensitivity Engine & Model Verifier
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


def run_1pp_revenue_sensitivity():
    """
    Executes the required +/- 1 percentage point revenue growth sensitivity:
    - Base revenue growth path: [100.0%, 50.0%, 30.0%, 15.0%, 10.0%]
    - Lower path (-1 pp):       [ 99.0%, 49.0%, 29.0%, 14.0%,  9.0%]
    - Higher path (+1 pp):      [101.0%, 51.0%, 31.0%, 16.0%, 11.0%]
    Calculates exact FY31 Revenue, Operating Profit (EBIT), FCFF, FCFE,
    Modeled Value per Share, $ change vs Base, and % change vs Base.
    """
    base_growth = ASSUMPTIONS["revenue_growth"]
    lower_growth = [g - 0.01 for g in base_growth]
    higher_growth = [g + 0.01 for g in base_growth]

    scenarios = [
        ("Lower (-1 pp)", lower_growth),
        ("Base (0 pp)", base_growth),
        ("Higher (+1 pp)", higher_growth),
    ]

    results = []
    for label, g_path in scenarios:
        out = run_proforma(custom_assumptions={"revenue_growth": g_path})
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

        results.append({
            "label": label,
            "growth": g_path,
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
        })

    base_res = results[1]
    low_res = results[0]
    high_res = results[2]

    # Calculate differences
    for r in results:
        r["dollar_change"] = r["vps"] - base_res["vps"]
        r["pct_change_abs"] = (r["dollar_change"] / abs(base_res["vps"])) * 100.0
        r["pct_change_signed"] = (r["dollar_change"] / base_res["vps"]) * 100.0

    return {
        "results": results,
        "base": base_res,
        "lower": low_res,
        "higher": high_res,
    }


def print_table():
    data = run_1pp_revenue_sensitivity()
    res = data["results"]
    b = data["base"]
    l = data["lower"]
    h = data["higher"]

    print("=" * 115)
    print("FIN 439 LAB 12: IREN LIMITED -- +/-1 PERCENTAGE-POINT REVENUE GROWTH SENSITIVITY")
    print("=" * 115)
    print(f"{'Scenario':<16} {'Revenue Growth Path':<30} {'FY31 Rev ($M)':>14} {'FY31 EBIT ($M)':>15} {'FY31 FCFF ($M)':>15} {'VPS ($/sh)':>12} {'$ Change':>10} {'% Change':>10}")
    print("-" * 115)
    for r in res:
        g_str = "[" + ", ".join([f"{x*100:.1f}%" for x in r["growth"]]) + "]"
        print(f"{r['label']:<16} {g_str:<30} {r['rev_fy31']:>14.2f} {r['ebit_fy31']:>15.2f} {r['fcff_fy31']:>15.2f} {r['vps']:>12.4f} {r['dollar_change']:>+10.4f} {r['pct_change_abs']:>+9.2f}%")
    print("-" * 115)
    print(f"Base Value per Share: ${b['vps']:.4f}")
    print(f"Upside Sensitivity (+1pp):  Value/share moves from ${b['vps']:.4f} to ${h['vps']:.4f} (Signed d: ${h['dollar_change']:+.4f} or {h['pct_change_abs']:+.2f}% vs |Base|)")
    print(f"Downside Sensitivity (-1pp): Value/share moves from ${b['vps']:.4f} to ${l['vps']:.4f} (Signed d: ${l['dollar_change']:+.4f} or {l['pct_change_abs']:+.2f}% vs |Base|)")
    print("=" * 115)


if __name__ == "__main__":
    print_table()
