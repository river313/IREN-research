"""
FIN 439 Lab 09 — Pro-Forma Financial Modeling I: Build the Base Case
Company: Asbury Automotive Group (NYSE: ABG)
Five-Year, Three-Statement Financial Engine (FY2026E – FY2030E)

Standard library only. Computes cash last, enforces balance sheet equality,
and refuses valuation if any balance-sheet gap or cash violation occurs.
"""

import sys
import math

# ==============================================================================
# 1. OPENING BALANCE SHEET (FY2025, USD millions)
# ==============================================================================
OPENING_BS = {
    "revenue": 17999.0,
    "cost_of_sales": 17999.0 - 3071.7,  # 14927.3
    "gross_profit": 3071.7,
    "inventory": 2135.8,
    "ppe": 3070.4,
    "other_assets": 6371.6,
    "cash": 40.4,
    "floor_plan": 2027.0,
    "term_debt": 3572.0,
    "revolver": 0.0,
    "other_liab": 2127.5,
    "equity": 3891.7,
}

# ==============================================================================
# 2. MODEL ASSUMPTIONS (Labeled: History, Guidance, Judgment, Fact)
# ==============================================================================
ASSUMPTIONS = {
    # Income statement drivers
    "organic_growth": 0.018,                  # judgment: 1.8% per year
    "gross_margin": 0.1705,                   # judgment: 17.05%
    "sga_ratios": [0.665, 0.655, 0.645, 0.645, 0.645], # judgment: 2026->2030
    "depr_ratio": 82.4 / 3070.4,              # history: FY25 depr / FY25 PP&E
    "impairment": 120.0,                      # judgment: non-cash write-down per year
    "capex": 250.0,                           # guidance: capital spending per year
    "tax_rate": 0.255,                        # judgment: 25.5%

    # Working capital & operating debt drivers
    "inv_days": (2135.8 / (17999.0 - 3071.7)) * 365.0,  # history: 52.2274 days
    "floor_plan_ratio": 2027.0 / 2135.8,      # history: floor plan / inventory
    "owc_ratio": 0.008,                       # judgment: 0.8% of change in revenue

    # Financing & liquidity drivers
    "min_cash": 25.0,                         # history: minimum liquidity buffer
    "revolver_limit": 850.0,                  # judgment: maximum facility capacity
    "revolver_rate": 0.060,                   # judgment: 6.0% interest rate
    "debt_repayment": 150.0,                  # judgment: principal reduction per year
    "share_buyback": 150.0,                   # judgment: share repurchase per year
    "floor_plan_rate": 0.0467,                # history: 4.67% interest rate
    "debt_rate": 0.0544,                      # history: 5.44% interest rate

    # Valuation parameters
    "cost_of_equity": 0.10,                   # judgment: 10.0% discount rate
    "terminal_growth": 0.025,                 # judgment: 2.5% perpetual growth
    "shares_outstanding": 17.951349,          # fact: 10-Q June 30, 2026 (million)
}

YEARS = [2026, 2027, 2028, 2029, 2030]


# ==============================================================================
# 3. PRO-FORMA SIMULATION ENGINE
# ==============================================================================
def run_proforma(broken_cash_year=None, broken_cash_value=None):
    """
    Project 5 years of financial statements (FY2026E - FY2030E).
    Calculates cash last.
    If broken_cash_year is specified, replaces calculated cash for that year
    to test assert_balanced().
    """
    is_list = []
    bs_list = []
    cf_list = []
    fcfe_list = []
    checks = []

    # Prior-year starting state (FY2025)
    rev_prev = OPENING_BS["revenue"]
    cash_prev = OPENING_BS["cash"]
    inv_prev = OPENING_BS["inventory"]
    ppe_prev = OPENING_BS["ppe"]
    other_assets_prev = OPENING_BS["other_assets"]
    fp_prev = OPENING_BS["floor_plan"]
    debt_prev = OPENING_BS["term_debt"]
    revolver_prev = OPENING_BS["revolver"]
    equity_prev = OPENING_BS["equity"]
    other_liab = OPENING_BS["other_liab"]

    for i, year in enumerate(YEARS):
        # ----------------------------------------------------------------------
        # A. INCOME STATEMENT
        # ----------------------------------------------------------------------
        revenue = rev_prev * (1.0 + ASSUMPTIONS["organic_growth"])
        gross_profit = revenue * ASSUMPTIONS["gross_margin"]
        cost_of_sales = revenue - gross_profit
        sga = gross_profit * ASSUMPTIONS["sga_ratios"][i]
        depreciation = ppe_prev * ASSUMPTIONS["depr_ratio"]
        impairment = ASSUMPTIONS["impairment"]
        operating_income = gross_profit - sga - depreciation - impairment

        # Interest on OPENING debt and floor-plan balances
        fp_interest = fp_prev * ASSUMPTIONS["floor_plan_rate"]
        debt_interest = debt_prev * ASSUMPTIONS["debt_rate"]
        revolver_interest = revolver_prev * ASSUMPTIONS["revolver_rate"]
        total_interest = fp_interest + debt_interest + revolver_interest

        pretax_income = operating_income - total_interest
        tax = max(0.0, pretax_income) * ASSUMPTIONS["tax_rate"]
        net_income = pretax_income - tax

        # ----------------------------------------------------------------------
        # B. BALANCE SHEET (EXCEPT CASH)
        # ----------------------------------------------------------------------
        inventory = cost_of_sales * ASSUMPTIONS["inv_days"] / 365.0
        floor_plan = inventory * ASSUMPTIONS["floor_plan_ratio"]
        ppe = ppe_prev + ASSUMPTIONS["capex"] - depreciation
        delta_rev = revenue - rev_prev
        delta_owc = ASSUMPTIONS["owc_ratio"] * delta_rev
        other_assets = other_assets_prev + delta_owc - impairment
        debt = debt_prev - ASSUMPTIONS["debt_repayment"]
        equity = equity_prev + net_income - ASSUMPTIONS["share_buyback"]

        # ----------------------------------------------------------------------
        # C. CASH FLOW STATEMENT & FREE CASH FLOW TO EQUITY (FCFE)
        # ----------------------------------------------------------------------
        delta_inv = inventory - inv_prev
        delta_fp = floor_plan - fp_prev

        # FCFE = Net Income + D&A + Impairment - Capex - Delta Inventory - Delta Other WC + Delta Floor Plan - Repayment
        fcfe = (
            net_income
            + depreciation
            + impairment
            - ASSUMPTIONS["capex"]
            - delta_inv
            - delta_owc
            + delta_fp
            - ASSUMPTIONS["debt_repayment"]
        )
        fcfe_list.append(fcfe)

        # ----------------------------------------------------------------------
        # D. CASH & REVOLVER LIQUIDITY MECHANISM (CASH CALCULATED LAST)
        # ----------------------------------------------------------------------
        # Cash before financing adjustments
        unadjusted_cash = cash_prev + fcfe - ASSUMPTIONS["share_buyback"]

        revolver = revolver_prev
        revolver_draw = 0.0
        revolver_repayment = 0.0

        if unadjusted_cash < ASSUMPTIONS["min_cash"]:
            # Deficit: draw revolver to preserve minimum cash
            shortfall = ASSUMPTIONS["min_cash"] - unadjusted_cash
            max_borrow = ASSUMPTIONS["revolver_limit"] - revolver_prev
            revolver_draw = min(shortfall, max_borrow)
            revolver = revolver_prev + revolver_draw
            cash = unadjusted_cash + revolver_draw
        elif unadjusted_cash > ASSUMPTIONS["min_cash"] and revolver_prev > 0.0:
            # Surplus: repay outstanding revolver first
            excess = unadjusted_cash - ASSUMPTIONS["min_cash"]
            revolver_repayment = min(excess, revolver_prev)
            revolver = revolver_prev - revolver_repayment
            cash = unadjusted_cash - revolver_repayment
        else:
            cash = unadjusted_cash

        # Broken-cash test override if requested
        if broken_cash_year == year and broken_cash_value is not None:
            cash = broken_cash_value

        # ----------------------------------------------------------------------
        # E. BALANCE SHEET INTEGRITY CHECK
        # ----------------------------------------------------------------------
        total_assets = cash + inventory + ppe + other_assets
        total_liab = floor_plan + debt + revolver + other_liab
        total_liab_equity = total_liab + equity
        bs_gap = total_assets - total_liab_equity
        min_cash_pass = cash >= (ASSUMPTIONS["min_cash"] - 1e-4)

        # Store records
        is_list.append({
            "year": year,
            "revenue": revenue,
            "cost_of_sales": cost_of_sales,
            "gross_profit": gross_profit,
            "sga": sga,
            "depreciation": depreciation,
            "impairment": impairment,
            "operating_income": operating_income,
            "fp_interest": fp_interest,
            "debt_interest": debt_interest,
            "revolver_interest": revolver_interest,
            "total_interest": total_interest,
            "pretax_income": pretax_income,
            "tax": tax,
            "net_income": net_income,
        })

        bs_list.append({
            "year": year,
            "cash": cash,
            "inventory": inventory,
            "ppe": ppe,
            "other_assets": other_assets,
            "total_assets": total_assets,
            "floor_plan": floor_plan,
            "term_debt": debt,
            "revolver": revolver,
            "other_liab": other_liab,
            "total_liab": total_liab,
            "equity": equity,
            "total_liab_equity": total_liab_equity,
            "gap": bs_gap,
            "min_cash_pass": min_cash_pass,
        })

        cf_list.append({
            "year": year,
            "net_income": net_income,
            "depreciation": depreciation,
            "impairment": impairment,
            "capex": ASSUMPTIONS["capex"],
            "delta_inv": delta_inv,
            "delta_owc": delta_owc,
            "delta_fp": delta_fp,
            "debt_repayment": ASSUMPTIONS["debt_repayment"],
            "fcfe": fcfe,
            "cash_prev": cash_prev,
            "share_buyback": ASSUMPTIONS["share_buyback"],
            "revolver_draw": revolver_draw,
            "revolver_repayment": revolver_repayment,
            "ending_cash": cash,
        })

        checks.append({
            "year": year,
            "gap": bs_gap,
            "min_cash_pass": min_cash_pass,
            "cash": cash,
            "assets": total_assets,
            "liab_equity": total_liab_equity,
        })

        # Advance state to next year
        rev_prev = revenue
        cash_prev = cash
        inv_prev = inventory
        ppe_prev = ppe
        other_assets_prev = other_assets
        fp_prev = floor_plan
        debt_prev = debt
        revolver_prev = revolver
        equity_prev = equity

    return is_list, bs_list, cf_list, fcfe_list, checks


# ==============================================================================
# 4. ASSERT BALANCED FUNCTION (REFUSES VALUATION IF INTEGRITY FAILS)
# ==============================================================================
def assert_balanced(checks):
    """
    Verify that every projected year's balance sheet balances exactly
    and meets the minimum cash requirement.
    Raises ValueError naming the year and gap if any check fails.
    """
    for chk in checks:
        year_label = f"FY{chk['year']}E"
        # Tolerance of 0.05 to account for floating-point rounding
        if abs(chk["gap"]) >= 0.05:
            raise ValueError(
                f"Balance sheet does not balance in {year_label}: "
                f"gap of {chk['gap']:+.1f} million "
                f"(Assets: {chk['assets']:.1f}, Liab+Equity: {chk['liab_equity']:.1f}). "
                f"Model refuses to calculate valuation."
            )
        if not chk["min_cash_pass"]:
            raise ValueError(
                f"Cash requirement violated in {year_label}: "
                f"ending cash ${chk['cash']:.1f}M is below minimum ${ASSUMPTIONS['min_cash']:.1f}M. "
                f"Model refuses to calculate valuation."
            )


# ==============================================================================
# 5. VALUATION ENGINE
# ==============================================================================
def calculate_valuation(fcfe_list):
    """
    Value equity as the present value of explicit 5-year FCFE
    plus terminal value:
    TV = (2030 FCFE + 2030 repayment) * (1 + g) / (r_e - g)
    Discounted 5 years at cost of equity.
    """
    r_e = ASSUMPTIONS["cost_of_equity"]
    g = ASSUMPTIONS["terminal_growth"]
    shares = ASSUMPTIONS["shares_outstanding"]
    repayment_2030 = ASSUMPTIONS["debt_repayment"]

    # Explicit PV
    pv_explicit = sum(cf / ((1.0 + r_e) ** (idx + 1)) for idx, cf in enumerate(fcfe_list))

    # Terminal Value: steady-state adds back debt repayment
    fcfe_2030 = fcfe_list[-1]
    tv_numerator = (fcfe_2030 + repayment_2030) * (1.0 + g)
    tv = tv_numerator / (r_e - g)
    pv_tv = tv / ((1.0 + r_e) ** 5)

    equity_value = pv_explicit + pv_tv
    share_of_tv = (pv_tv / equity_value) * 100.0
    value_per_share = equity_value / shares

    return {
        "pv_explicit": pv_explicit,
        "tv_nominal": tv,
        "pv_tv": pv_tv,
        "equity_value": equity_value,
        "share_of_tv": share_of_tv,
        "value_per_share": value_per_share,
    }


# ==============================================================================
# 6. TABLE DISPLAY FORMATTERS
# ==============================================================================
def print_model_output(is_list, bs_list, cf_list, checks, val_res):
    """Print complete three statements, validation checks, and valuation."""
    header_years = ["FY2025"] + [f"FY{y}E" for y in YEARS]
    col_w = 11
    label_w = 36

    print("\n" + "=" * 105)
    print("FIN 439 LAB 09: ASBURY AUTOMOTIVE GROUP (ABG) FIVE-YEAR PRO-FORMA MODEL")
    print("=" * 105)

    # --------------------------------------------------------------------------
    # 1. INCOME STATEMENT TABLE
    # --------------------------------------------------------------------------
    print("\n1. PRO-FORMA INCOME STATEMENT (USD millions)")
    print("-" * 105)
    header_str = f"{'Line / Metric':<{label_w}}" + "".join(f"{h:>{col_w}}" for h in header_years)
    print(header_str)
    print("-" * 105)

    rows_is = [
        ("Revenue", [OPENING_BS["revenue"]] + [d["revenue"] for d in is_list]),
        ("Cost of Sales", [OPENING_BS["cost_of_sales"]] + [d["cost_of_sales"] for d in is_list]),
        ("Gross Profit", [OPENING_BS["gross_profit"]] + [d["gross_profit"] for d in is_list]),
        ("SG&A Expense", ["-"] + [f"{d['sga']:.1f}" for d in is_list]),
        ("Depreciation Expense", ["-"] + [f"{d['depreciation']:.1f}" for d in is_list]),
        ("Impairment (Non-Cash)", ["-"] + [f"{d['impairment']:.1f}" for d in is_list]),
        ("Operating Income (EBIT)", ["-"] + [f"{d['operating_income']:.1f}" for d in is_list]),
        ("  Floor Plan Interest", ["-"] + [f"{d['fp_interest']:.1f}" for d in is_list]),
        ("  Term Debt Interest", ["-"] + [f"{d['debt_interest']:.1f}" for d in is_list]),
        ("  Revolver Interest", ["-"] + [f"{d['revolver_interest']:.1f}" for d in is_list]),
        ("Total Interest Expense", ["-"] + [f"{d['total_interest']:.1f}" for d in is_list]),
        ("Pretax Income (EBT)", ["-"] + [f"{d['pretax_income']:.1f}" for d in is_list]),
        ("Income Tax (25.5%)", ["-"] + [f"{d['tax']:.1f}" for d in is_list]),
        ("Net Income", ["-"] + [f"{d['net_income']:.1f}" for d in is_list]),
    ]

    for label, vals in rows_is:
        row_str = f"{label:<{label_w}}"
        for v in vals:
            if isinstance(v, float):
                row_str += f"{v:>{col_w}.1f}"
            else:
                row_str += f"{v:>{col_w}}"
        print(row_str)

    # --------------------------------------------------------------------------
    # 2. BALANCE SHEET TABLE
    # --------------------------------------------------------------------------
    print("\n2. PRO-FORMA BALANCE SHEET (USD millions)")
    print("-" * 105)
    print(header_str)
    print("-" * 105)

    opening_tot_assets = (
        OPENING_BS["cash"]
        + OPENING_BS["inventory"]
        + OPENING_BS["ppe"]
        + OPENING_BS["other_assets"]
    )
    opening_tot_liab = (
        OPENING_BS["floor_plan"]
        + OPENING_BS["term_debt"]
        + OPENING_BS["revolver"]
        + OPENING_BS["other_liab"]
    )
    opening_tot_liab_eq = opening_tot_liab + OPENING_BS["equity"]

    rows_bs = [
        ("ASSETS:", [""] * 6),
        ("  Cash & Cash Equivalents", [OPENING_BS["cash"]] + [d["cash"] for d in bs_list]),
        ("  Inventories", [OPENING_BS["inventory"]] + [d["inventory"] for d in bs_list]),
        ("  Property, Plant & Equipment (net)", [OPENING_BS["ppe"]] + [d["ppe"] for d in bs_list]),
        ("  Other Assets", [OPENING_BS["other_assets"]] + [d["other_assets"] for d in bs_list]),
        ("TOTAL ASSETS", [opening_tot_assets] + [d["total_assets"] for d in bs_list]),
        ("LIABILITIES & SHAREHOLDERS' EQUITY:", [""] * 6),
        ("  Floor Plan Notes Payable", [OPENING_BS["floor_plan"]] + [d["floor_plan"] for d in bs_list]),
        ("  Term Debt", [OPENING_BS["term_debt"]] + [d["term_debt"] for d in bs_list]),
        ("  Revolving Credit Facility", [OPENING_BS["revolver"]] + [d["revolver"] for d in bs_list]),
        ("  Other Liabilities", [OPENING_BS["other_liab"]] + [d["other_liab"] for d in bs_list]),
        ("TOTAL LIABILITIES", [opening_tot_liab] + [d["total_liab"] for d in bs_list]),
        ("  Shareholders' Equity", [OPENING_BS["equity"]] + [d["equity"] for d in bs_list]),
        ("TOTAL LIABILITIES & EQUITY", [opening_tot_liab_eq] + [d["total_liab_equity"] for d in bs_list]),
    ]

    for label, vals in rows_bs:
        if not label.strip().isupper() or "TOTAL" in label:
            row_str = f"{label:<{label_w}}"
        else:
            row_str = f"{label:<{label_w}}"
        for v in vals:
            if isinstance(v, float):
                row_str += f"{v:>{col_w}.1f}"
            else:
                row_str += f"{v:>{col_w}}"
        print(row_str)

    # --------------------------------------------------------------------------
    # 3. CASH FLOW STATEMENT & FINANCING SCHEDULE
    # --------------------------------------------------------------------------
    print("\n3. PRO-FORMA CASH FLOW & EQUITY FINANCING SCHEDULE (USD millions)")
    print("-" * 105)
    print(header_str)
    print("-" * 105)

    rows_cf = [
        ("Net Income", ["-"] + [f"{d['net_income']:.1f}" for d in cf_list]),
        ("(+) Depreciation Expense", ["-"] + [f"{d['depreciation']:.1f}" for d in cf_list]),
        ("(+) Impairment (Non-Cash)", ["-"] + [f"{d['impairment']:.1f}" for d in cf_list]),
        ("(-) Capital Expenditures (Capex)", ["-"] + [f"-{d['capex']:.1f}" for d in cf_list]),
        ("(-) Change in Inventories", ["-"] + [f"-{d['delta_inv']:.1f}" for d in cf_list]),
        ("(-) Change in Other Working Capital", ["-"] + [f"-{d['delta_owc']:.1f}" for d in cf_list]),
        ("(+) Change in Floor Plan Notes", ["-"] + [f"{d['delta_fp']:.1f}" for d in cf_list]),
        ("(-) Term Debt Principal Repayment", ["-"] + [f"-{d['debt_repayment']:.1f}" for d in cf_list]),
        ("FREE CASH FLOW TO EQUITY (FCFE)", ["-"] + [f"{d['fcfe']:.1f}" for d in cf_list]),
        ("--- CASH RECONCILIATION ---", [""] * 6),
        ("Beginning Cash Balance", ["-"] + [f"{d['cash_prev']:.1f}" for d in cf_list]),
        ("(+) Free Cash Flow to Equity", ["-"] + [f"{d['fcfe']:.1f}" for d in cf_list]),
        ("(-) Share Repurchases (Buyback)", ["-"] + [f"-{d['share_buyback']:.1f}" for d in cf_list]),
        ("(+) Revolver Borrowing / (-) Repayment", ["-"] + [f"{d['revolver_draw'] - d['revolver_repayment']:.1f}" for d in cf_list]),
        ("ENDING CASH BALANCE", [OPENING_BS["cash"]] + [d["ending_cash"] for d in cf_list]),
    ]

    for label, vals in rows_cf:
        row_str = f"{label:<{label_w}}"
        for v in vals:
            if isinstance(v, float):
                row_str += f"{v:>{col_w}.1f}"
            else:
                row_str += f"{v:>{col_w}}"
        print(row_str)

    # --------------------------------------------------------------------------
    # 4. VALIDATION BLOCK
    # --------------------------------------------------------------------------
    print("\n" + "=" * 105)
    print("4. MODEL VALIDATION BLOCK & BALANCE INTEGRITY CHECKS")
    print("=" * 105)
    val_header = f"{'Check Description':<{label_w}}" + "".join(f"{h:>{col_w}}" for h in header_years[1:])
    print(val_header)
    print("-" * 105)

    gaps = [f"{c['gap']:+.1f}" for c in checks]
    min_cash_checks = ["PASS" if c["min_cash_pass"] else "FAIL" for c in checks]

    print(f"{'Assets - Liabilities - Equity (Gap)':<{label_w}}" + "".join(f"{g:>{col_w}}" for g in gaps))
    print(f"{'Cash >= Minimum ($25.0M) Buffer':<{label_w}}" + "".join(f"{m:>{col_w}}" for m in min_cash_checks))
    print("-" * 105)
    all_balanced = all(abs(c["gap"]) < 0.05 for c in checks)
    all_cash_ok = all(c["min_cash_pass"] for c in checks)

    if all_balanced and all_cash_ok:
        print(">>> ALL BALANCE SHEET & LIQUIDITY CHECKS PASSED: MODEL IS BALANCED (Gap = 0.0). <<<")
    else:
        print(">>> INTEGRITY CHECK FAILED: DO NOT PROCEED TO VALUATION. <<<")

    # --------------------------------------------------------------------------
    # 5. VALUATION BLOCK
    # --------------------------------------------------------------------------
    print("\n" + "=" * 105)
    print("5. VALUATION SUMMARY & COMPARISON WITH REFERENCE BENCHMARKS")
    print("=" * 105)
    print(f"Cost of Equity (r_e):                 {ASSUMPTIONS['cost_of_equity']*100:.1f}%")
    print(f"Terminal Growth Rate (g):              {ASSUMPTIONS['terminal_growth']*100:.1f}%")
    print(f"Diluted Shares Outstanding:            {ASSUMPTIONS['shares_outstanding']:.6f} million")
    print("-" * 105)
    print(f"Present Value of 5-Year Explicit FCFE: ${val_res['pv_explicit']:,.2f} million")
    print(f"Terminal Value (at FY2030E):           ${val_res['tv_nominal']:,.2f} million")
    print(f"Present Value of Terminal Value:       ${val_res['pv_tv']:,.2f} million")
    print(f"Total Implied Equity Value:            ${val_res['equity_value']:,.2f} million")
    print(f"Share of Value After 2030 (PV TV / EV):{val_res['share_of_tv']:>7.1f}%  (Reference: ~80%)")
    print("-" * 105)
    print(f">>> IMPLIED VALUE PER SHARE:           ${val_res['value_per_share']:.2f}")
    print(f">>> PROFESSOR'S TARGET VALUE PER SHARE: $291.75")
    match_status = "EXACT MATCH (to nearest cent)" if abs(val_res["value_per_share"] - 291.75) < 0.01 else "MISMATCH"
    print(f">>> BENCHMARK COMPARISON RESULT:       {match_status}")
    print("=" * 105 + "\n")


# ==============================================================================
# 7. MAIN ORCHESTRATION FUNCTION
# ==============================================================================
def main():
    # Check for CLI test flag: --broken-cash
    test_broken_cash = "--broken-cash" in sys.argv or "--test-broken-cash" in sys.argv

    if test_broken_cash:
        print("\n" + "#" * 80)
        print("RUNNING REQUIRED BROKEN-CASH TEST: Overriding FY2026E cash with opening $40.4M...")
        print("#" * 80)
        is_list, bs_list, cf_list, fcfe_list, checks = run_proforma(
            broken_cash_year=2026, broken_cash_value=40.4
        )
        print("\nValidation checks output:")
        for chk in checks:
            print(f"  FY{chk['year']}E: Gap = {chk['gap']:+.2f}, Cash = ${chk['cash']:.1f}M, Min Cash = {chk['min_cash_pass']}")

        print("\nCalling assert_balanced()...")
        try:
            assert_balanced(checks)
            print("ERROR: assert_balanced() failed to raise an exception!")
        except ValueError as e:
            print(f"\nSUCCESS: assert_balanced() refused valuation as expected!\nCaught Exception: {e}")
            return 0
    else:
        # Standard run: build model, assert balanced, compute valuation
        is_list, bs_list, cf_list, fcfe_list, checks = run_proforma()

        # Integrity barrier: MUST pass before valuation
        assert_balanced(checks)

        # Value company
        val_res = calculate_valuation(fcfe_list)

        # Print outputs
        print_model_output(is_list, bs_list, cf_list, checks, val_res)
        return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
