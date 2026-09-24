"""
FIN 439 Lab 10 — Pro-Forma Financial Modeling: Your Company Through It
Company: IREN Limited (NASDAQ: IREN)
Five-Year, Three-Statement Financial Engine (FY2027E – FY2031E)

Built under FIN 439 Lab 10 specifications:
- Standard library only (sys, math)
- Opens with audited FY2026 balance sheet (period ended June 30, 2026)
- Company-specific modeling line: Customer Prepayments / Deferred Revenue (in place of ABG Floor Plan)
- Calculates Cash LAST
- Enforces balance sheet equality (Assets - Liabilities - Equity == 0.0)
- Explicitly accounts for negative earnings / FCFE
- Model REFUSES to value an invalid or broken forecast
"""

import sys
import math


# ==============================================================================
# 1. AUDITED OPENING BALANCE SHEET (FY2026 ended June 30, 2026, USD millions)
# Sourced from IREN Limited Form 10-K filed August 27, 2026 (Item 8, p. F-6)
# ==============================================================================
OPENING_BS = {
    # Operating Base
    "revenue": 707.007,                 # FY26 Total Revenue ($128.8M AI Cloud + $578.2M Bitcoin Mining)
    "cost_of_revenue_ex_depr": 219.706, # FY26 Cost of Revenue ex D&A ($16.9M AI Cloud + $202.8M Mining)
    "gross_profit_ex_depr": 487.301,    # FY26 Gross Profit ex D&A ($707.007M - $219.706M)

    # Assets (Audited June 30, 2026)
    "cash": 5895.591,                   # Cash and cash equivalents ($5,895,591 thousand)
    "restricted_cash": 1723.936,        # Restricted cash: $1,670.252M current + $53.684M non-current
    "ar": 21.062,                       # Accounts receivable, net ($21,062 thousand)
    "ppe": 6753.183,                    # Property, plant & equipment, net ($6,753,183 thousand)
    "other_assets": 1396.267,           # Deposits, prepaids, derivatives, intangibles, goodwill ($1,396,267 thousand)
    # Total Assets = $15,790.039M

    # Liabilities (Audited June 30, 2026)
    "deferred_rev": 1842.546,           # Customer Prepayments / Deferred Revenue: $46.491M curr + $1,796.055M non-curr
    "term_debt": 7836.740,              # Debt & finance leases: $169.37M curr debt + $7,423.57M non-curr + $243.80M leases
    "liquidity_facility": 0.0,          # Undrawn liquidity / GPU credit facility
    "other_liab": 1925.140,             # AP & accrued ($1,825.39M) + lease liab ($2.79M) + taxes & other ($96.96M)
    # Total Liabilities = $11,604.426M

    # Stockholders' Equity (Audited June 30, 2026)
    "equity": 4185.613,                 # Ordinary shares ($7,172.89M) + APIC (-$1,647.06M) + Deficit (-$1,298.79M) + AOCI (-$41.42M)
    # Total Liabilities & Equity = $15,790.039M (Balance Sheet Gap = $0.000M)
}


# ==============================================================================
# 2. MODEL ASSUMPTIONS (Labeled: History, Guidance, Judgment)
# ==============================================================================
ASSUMPTIONS = {
    # Top-line drivers
    # Trajectory reflecting management guidance: $4B contracted ARR for 2026 capacity ($1B operating ARR in Aug 2026),
    # $9.7B 5-year Microsoft contract, scaling from 0.3 GW IT (2026) to 1.2 GW gross (2027)
    "revenue_growth": [1.00, 0.50, 0.30, 0.15, 0.10],   # judgment (FLAGGED FOR APPROVAL): FY27E -> FY31E
    "gross_margin": 0.700,                              # judgment (FLAGGED FOR APPROVAL): 70.0% cash gross margin (FY26 was 68.9%)
    "sga_ratios": [0.55, 0.45, 0.40, 0.35, 0.35],       # judgment (FLAGGED FOR APPROVAL): SG&A as % of Gross Profit
    "depr_ratio": 0.085,                                # history: 8.5% of net PP&E (Note 14: 5-yr GPUs, 20-25 yr data centers)
    "impairment": 0.0,                                  # judgment: $0.0M/yr (one-time FY26 ASIC transition impairment ceased)
    
    # Capital expenditures (USD millions)
    # Guidance / Judgment: Reflects $13.8B contractual commitments; Horizon 1 delivered; Horizons 2-4 and Childress buildout
    "capex": [2500.0, 1500.0, 1000.0, 700.0, 600.0],   # guidance / judgment (FLAGGED FOR APPROVAL): FY27E -> FY31E
    "tax_rate_normalized": 0.210,                       # judgment: 21.0% US statutory rate (0% during initial NOL utilization)
    "nol_balance_start": 700.0,                         # history: Note 28 accumulated loss carryforwards available

    # Company-Specific Operating Line (Replacing ABG Floor Plan)
    # Customer Prepayments / Deferred Revenue from Hyperscaler AI Cloud Contracts
    "deferred_rev_ratio": 0.250,                        # judgment (FLAGGED FOR APPROVAL): 25.0% of forward revenue held as prepayments
    "inv_days": 0.0,                                    # history / fact: $0 inventory across all 10-K filings (stated "none")
    "ar_days": 11.0,                                    # history: 10.9 days in FY26 ($21.06M AR / $707M rev * 365)
    "owc_ratio": 0.010,                                 # judgment: other operating working capital change = 1.0% of delta revenue

    # Financing & Liquidity drivers
    "min_cash": 500.0,                                  # judgment (FLAGGED FOR APPROVAL): $500M liquidity floor for megawatt sites
    "facility_limit": 2000.0,                           # guidance: Note 23 unfunded DDTL ($1.13B) + GPU facility capacity
    "facility_rate": 0.060,                             # guidance: Note 23 GPU financing rate (6.0%)
    "debt_interest_rate": 0.045,                        # history: blended coupon on convertible notes (Note 23: 3.25% - 5.50%)
    "cash_yield": 0.035,                                # history: 3.5% interest earned on cash balances (earned $80.6M in FY26)
    "debt_repayment": 400.0,                            # judgment: $400M annual scheduled principal debt amortization
    "share_buyback": 0.0,                               # judgment: $0.0M (retained for high-growth infrastructure expansion)
    "equity_issuance": 0.0,                             # judgment: $0.0M (base case assumes no further share dilution)

    # Valuation Parameters
    "cost_of_equity": 0.114,                            # history / benchmark: 11.4% (from Project-1/dcf.py line 14 & CAPM)
    "terminal_growth": 0.025,                           # history / benchmark: 2.5% (from Project-1/dcf.py line 15)
    "shares_outstanding": 394.058648,                   # fact: 10-K cover page as of August 14, 2026 (million shares)
    "shares_bs_ending": 380.193608,                     # fact: June 30, 2026 Balance Sheet outstanding shares (million)
    "shares_weighted_avg": 316.123145,                  # fact: FY2026 diluted weighted-average shares (million)
}

YEARS = [2027, 2028, 2029, 2030, 2031]


# ==============================================================================
# 3. PRO-FORMA SIMULATION ENGINE
# ==============================================================================
def run_proforma(broken_cash_year=None, broken_cash_value=None, custom_assumptions=None):
    """
    Project 5 years of financial statements for IREN (FY2027E - FY2031E).
    Calculates cash last.
    Enforces balance sheet checks and liquidity constraints.
    Returns statement tables, validation checks, and valuation metrics.
    If broken_cash_year is specified, replaces calculated cash to test the refusal gate.
    """
    params = dict(ASSUMPTIONS)
    if custom_assumptions:
        params.update(custom_assumptions)

    is_list = []
    bs_list = []
    cf_list = []
    fcfe_list = []
    checks = []

    # Prior-year starting state (Audited FY2026)
    rev_prev = OPENING_BS["revenue"]
    cash_prev = OPENING_BS["cash"]
    restr_cash_prev = OPENING_BS["restricted_cash"]
    ar_prev = OPENING_BS["ar"]
    ppe_prev = OPENING_BS["ppe"]
    other_assets_prev = OPENING_BS["other_assets"]
    deferred_rev_prev = OPENING_BS["deferred_rev"]
    debt_prev = OPENING_BS["term_debt"]
    facility_prev = OPENING_BS["liquidity_facility"]
    other_liab_prev = OPENING_BS["other_liab"]
    equity_prev = OPENING_BS["equity"]

    nol_remaining = params["nol_balance_start"]

    for i, year in enumerate(YEARS):
        # ----------------------------------------------------------------------
        # A. INCOME STATEMENT
        # ----------------------------------------------------------------------
        growth_rate = params["revenue_growth"][i]
        revenue = rev_prev * (1.0 + growth_rate)
        gross_profit = revenue * params["gross_margin"]
        cost_of_revenue = revenue - gross_profit

        sga = gross_profit * params["sga_ratios"][i]
        depreciation = ppe_prev * params["depr_ratio"]
        impairment = params["impairment"]

        operating_income = gross_profit - sga - depreciation - impairment

        # Interest: Debt interest minus interest earned on opening cash
        debt_interest = debt_prev * params["debt_interest_rate"]
        facility_interest = facility_prev * params["facility_rate"]
        interest_income = cash_prev * params["cash_yield"]
        net_interest_expense = debt_interest + facility_interest - interest_income

        pretax_income = operating_income - net_interest_expense

        # Income taxes with NOL carryforward shield
        if pretax_income > 0.0:
            taxable_after_nol = max(0.0, pretax_income - nol_remaining)
            nol_used = min(pretax_income, nol_remaining)
            nol_remaining -= nol_used
            tax = taxable_after_nol * params["tax_rate_normalized"]
        else:
            tax = 0.0
            nol_remaining += abs(pretax_income)

        net_income = pretax_income - tax

        # ----------------------------------------------------------------------
        # B. BALANCE SHEET (EXCEPT CASH)
        # ----------------------------------------------------------------------
        # PP&E rollforward: Capex adds to PP&E, depreciation reduces
        capex_yr = params["capex"][i]
        ppe = ppe_prev + capex_yr - depreciation

        # Accounts receivable driven by collection days
        ar = revenue * (params["ar_days"] / 365.0)
        delta_ar = ar - ar_prev

        # Restricted cash: held as collateral, assumed stable/proportional
        restr_cash = restr_cash_prev

        # Other Operating Assets (deposits, connection rights)
        delta_rev = revenue - rev_prev
        delta_other_assets = params["owc_ratio"] * delta_rev
        other_assets = other_assets_prev + delta_other_assets - impairment

        # Company-Specific Line: Customer Prepayments / Deferred Revenue
        # Hyperscalers pay advance deposits on multi-year cluster contracts
        deferred_rev = revenue * params["deferred_rev_ratio"]
        delta_deferred_rev = deferred_rev - deferred_rev_prev

        # Debt repayment
        repayment = min(params["debt_repayment"], debt_prev)
        debt = debt_prev - repayment

        # Other operating liabilities (AP, accrued, operating leases)
        # Scale mildly with operating activity (0.5% of delta revenue)
        delta_other_liab = 0.005 * delta_rev
        other_liab = other_liab_prev + delta_other_liab

        # Equity rollforward: Net income increases equity, buybacks reduce
        equity = equity_prev + net_income - params["share_buyback"] + params["equity_issuance"]

        # ----------------------------------------------------------------------
        # C. CASH FLOW STATEMENT & FREE CASH FLOW TO EQUITY (FCFE)
        # ----------------------------------------------------------------------
        # Operating Cash Flow = Net Income + Non-Cash (D&A, Impairment) - Delta AR - Delta Other Assets + Delta Deferred Rev + Delta Other Liab
        ocf = (
            net_income
            + depreciation
            + impairment
            - delta_ar
            - delta_other_assets
            + delta_deferred_rev
            + delta_other_liab
        )

        # FCFE = OCF - Capex - Debt Repayment
        fcfe = ocf - capex_yr - repayment
        fcfe_list.append(fcfe)

        # ----------------------------------------------------------------------
        # D. CASH & LIQUIDITY MECHANISM (CASH CALCULATED LAST)
        # ----------------------------------------------------------------------
        unadjusted_cash = cash_prev + fcfe - params["share_buyback"] + params["equity_issuance"]

        facility = facility_prev
        facility_draw = 0.0
        facility_repay = 0.0

        if unadjusted_cash < params["min_cash"]:
            # Shortfall: draw credit facility to maintain minimum cash buffer
            shortfall = params["min_cash"] - unadjusted_cash
            max_draw = params["facility_limit"] - facility_prev
            facility_draw = min(shortfall, max(0.0, max_draw))
            facility = facility_prev + facility_draw
            cash = unadjusted_cash + facility_draw
        elif unadjusted_cash > params["min_cash"] and facility_prev > 0.0:
            # Surplus: repay outstanding facility first
            excess = unadjusted_cash - params["min_cash"]
            facility_repay = min(excess, facility_prev)
            facility = facility_prev - facility_repay
            cash = unadjusted_cash - facility_repay
        else:
            cash = unadjusted_cash

        # Broken-cash test override if requested
        if broken_cash_year == year and broken_cash_value is not None:
            cash = broken_cash_value

        # ----------------------------------------------------------------------
        # E. BALANCE SHEET INTEGRITY CHECK (ASSETS == LIAB + EQUITY)
        # ----------------------------------------------------------------------
        total_assets = cash + restr_cash + ar + ppe + other_assets
        total_liab = deferred_rev + debt + facility + other_liab
        total_liab_equity = total_liab + equity
        bs_gap = total_assets - total_liab_equity
        min_cash_pass = cash >= (params["min_cash"] - 1e-4)

        # Record statements
        is_list.append({
            "year": year,
            "revenue": revenue,
            "cost_of_revenue": cost_of_revenue,
            "gross_profit": gross_profit,
            "sga": sga,
            "depreciation": depreciation,
            "impairment": impairment,
            "operating_income": operating_income,
            "debt_interest": debt_interest,
            "facility_interest": facility_interest,
            "interest_income": interest_income,
            "net_interest": net_interest_expense,
            "pretax_income": pretax_income,
            "tax": tax,
            "net_income": net_income,
        })

        bs_list.append({
            "year": year,
            "cash": cash,
            "restricted_cash": restr_cash,
            "ar": ar,
            "ppe": ppe,
            "other_assets": other_assets,
            "total_assets": total_assets,
            "deferred_rev": deferred_rev,
            "term_debt": debt,
            "facility": facility,
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
            "delta_ar": delta_ar,
            "delta_other_assets": delta_other_assets,
            "delta_deferred_rev": delta_deferred_rev,
            "delta_other_liab": delta_other_liab,
            "operating_cash_flow": ocf,
            "capex": capex_yr,
            "debt_repayment": repayment,
            "fcfe": fcfe,
            "cash_prev": cash_prev,
            "facility_draw": facility_draw,
            "facility_repay": facility_repay,
            "ending_cash": cash,
        })

        checks.append({
            "year": year,
            "gap": bs_gap,
            "min_cash_pass": min_cash_pass,
            "cash": cash,
            "assets": total_assets,
            "liab_equity": total_liab_equity,
            "facility": facility,
        })

        # Advance state to next year
        rev_prev = revenue
        cash_prev = cash
        restr_cash_prev = restr_cash
        ar_prev = ar
        ppe_prev = ppe
        other_assets_prev = other_assets
        deferred_rev_prev = deferred_rev
        debt_prev = debt
        facility_prev = facility
        other_liab_prev = other_liab
        equity_prev = equity

    return {
        "is_list": is_list,
        "bs_list": bs_list,
        "cf_list": cf_list,
        "fcfe_list": fcfe_list,
        "checks": checks,
        "params": params,
    }


# ==============================================================================
# 4. VALUATION ENGINE & REFUSAL GATES
# ==============================================================================
def calculate_valuation(model_output):
    """
    Enforces balance integrity checks.
    REFUSES to compute valuation if any year has non-zero gap or broken cash.
    Accounts explicitly for negative earnings / FCFE.
    Does NOT invent a terminal value on negative cash flows.
    """
    checks = model_output["checks"]
    fcfe_list = model_output["fcfe_list"]
    params = model_output["params"]

    # 1. STRICT REFUSAL GATE
    for check in checks:
        if abs(check["gap"]) > 0.01:
            raise ValueError(
                f"MODEL REFUSAL: Balance sheet check failed in FY{check['year']}E! "
                f"Assets (${check['assets']:.2f}M) != Liab+Equity (${check['liab_equity']:.2f}M). "
                f"Discrepancy (Gap) = ${check['gap']:+.4f}M. "
                f"Model strictly refuses to value an invalid or out-of-balance forecast."
            )
        if not check["min_cash_pass"]:
            raise ValueError(
                f"MODEL REFUSAL: Liquidity violation in FY{check['year']}E! "
                f"Cash (${check['cash']:.2f}M) fell below minimum required floor (${params['min_cash']:.2f}M). "
                f"Model strictly refuses to value an invalid liquidity forecast."
            )

    r_e = params["cost_of_equity"]
    g = params["terminal_growth"]
    shares = params["shares_outstanding"]

    # 2. EXPLICIT ACCOUNTING FOR NEGATIVE FCFE
    # Lab 10 rule: "Write 'negative FCFE' against the years where it is, value only what is positive,
    # and say in one sentence why a terminal value on a negative cash flow is not a number."
    pv_explicit = 0.0
    discounted_fcfe = []
    negative_fcfe_years = []

    for idx, cf in enumerate(fcfe_list, start=1):
        year = YEARS[idx - 1]
        discount_factor = (1.0 + r_e) ** idx
        if cf < 0.0:
            negative_fcfe_years.append(year)
            # Record negative status; per instructions, note negative FCFE explicitly
            discounted_fcfe.append({
                "year": year,
                "fcfe": cf,
                "status": "negative FCFE",
                "pv": cf / discount_factor,
            })
            pv_explicit += cf / discount_factor
        else:
            discounted_fcfe.append({
                "year": year,
                "fcfe": cf,
                "status": "positive FCFE",
                "pv": cf / discount_factor,
            })
            pv_explicit += cf / discount_factor

    # 3. TERMINAL VALUE GATE
    terminal_cf = fcfe_list[-1]
    if terminal_cf <= 0.0:
        tv = 0.0
        pv_tv = 0.0
        tv_explanation = (
            "TERMINAL VALUE REFUSED (NOT A NUMBER): Terminal year cash flow is negative "
            f"(${terminal_cf:.2f}M). A terminal value on a negative cash flow is not a number "
            "because capitalizing an ongoing cash deficit into perpetuity implies an impossible "
            "perpetual external capital subsidy rather than a viable self-sustaining business."
        )
    else:
        tv = (terminal_cf * (1.0 + g)) / (r_e - g)
        pv_tv = tv / ((1.0 + r_e) ** 5)
        tv_explanation = "Terminal value calculated using Gordon Growth Model on positive Year 5 FCFE."

    equity_value = pv_explicit + pv_tv
    value_per_share = equity_value / shares

    # Alternate share count comparisons
    value_per_share_bs = equity_value / params["shares_bs_ending"]
    value_per_share_wa = equity_value / params["shares_weighted_avg"]

    return {
        "pv_explicit": pv_explicit,
        "terminal_value": tv,
        "pv_tv": pv_tv,
        "equity_value": equity_value,
        "value_per_share": value_per_share,
        "value_per_share_bs": value_per_share_bs,
        "value_per_share_wa": value_per_share_wa,
        "discounted_fcfe": discounted_fcfe,
        "negative_fcfe_years": negative_fcfe_years,
        "tv_explanation": tv_explanation,
    }


# ==============================================================================
# 5. FORMATTED REPORT PRINTER
# ==============================================================================
def print_model_report(model_output, valuation):
    """Prints professionally formatted 3-statement tables, checks, and valuation."""
    is_list = model_output["is_list"]
    bs_list = model_output["bs_list"]
    cf_list = model_output["cf_list"]
    checks = model_output["checks"]
    p = model_output["params"]

    print("=" * 105)
    print("FIN 439 LAB 10: IREN LIMITED (NASDAQ: IREN) FIVE-YEAR PRO-FORMA FINANCIAL ENGINE")
    print("=" * 105)

    # 1. Income Statement
    print("\n1. PRO-FORMA CONSOLIDATED INCOME STATEMENT (USD millions)")
    print("-" * 105)
    hdr = f"{'Metric / Line Item':<38} {'FY2026':>10} " + " ".join([f"FY{y}E".rjust(10) for y in YEARS])
    print(hdr)
    print("-" * 105)
    print(f"{'Total Revenue':<38} {OPENING_BS['revenue']:>10.1f} " + " ".join([f"{r['revenue']:>10.1f}" for r in is_list]))
    print(f"{'Cost of Revenues (ex D&A)':<38} {OPENING_BS['cost_of_revenue_ex_depr']:>10.1f} " + " ".join([f"{r['cost_of_revenue']:>10.1f}" for r in is_list]))
    print(f"{'Gross Profit (ex D&A)':<38} {OPENING_BS['gross_profit_ex_depr']:>10.1f} " + " ".join([f"{r['gross_profit']:>10.1f}" for r in is_list]))
    print(f"{'SG&A Expense':<38} {'449.1':>10} " + " ".join([f"{r['sga']:>10.1f}" for r in is_list]))
    print(f"{'Depreciation & Amortization':<38} {'417.7':>10} " + " ".join([f"{r['depreciation']:>10.1f}" for r in is_list]))
    print(f"{'Impairment of Assets':<38} {'638.8':>10} " + " ".join([f"{r['impairment']:>10.1f}" for r in is_list]))
    print(f"{'Operating Income (EBIT)':<38} {'-1046.7':>10} " + " ".join([f"{r['operating_income']:>10.1f}" for r in is_list]))
    print(f"{'  Debt & Lease Interest':<38} {'59.3':>10} " + " ".join([f"{r['debt_interest'] + r['facility_interest']:>10.1f}" for r in is_list]))
    print(f"{'  Interest Income on Cash':<38} {'-80.6':>10} " + " ".join([f"{-r['interest_income']:>10.1f}" for r in is_list]))
    print(f"{'Net Interest Expense':<38} {'-21.4':>10} " + " ".join([f"{r['net_interest']:>10.1f}" for r in is_list]))
    print(f"{'Pretax Income (EBT)':<38} {'-708.7':>10} " + " ".join([f"{r['pretax_income']:>10.1f}" for r in is_list]))
    print(f"{'Income Tax Expense / (Benefit)':<38} {'-6.1':>10} " + " ".join([f"{r['tax']:>10.1f}" for r in is_list]))
    print(f"{'GAAP Net Income (Loss)':<38} {'-702.6':>10} " + " ".join([f"{r['net_income']:>10.1f}" for r in is_list]))

    # 2. Balance Sheet
    print("\n2. PRO-FORMA CONSOLIDATED BALANCE SHEET (USD millions)")
    print("-" * 105)
    print(hdr)
    print("-" * 105)
    print("ASSETS:")
    print(f"{'  Cash & Cash Equivalents':<38} {OPENING_BS['cash']:>10.1f} " + " ".join([f"{r['cash']:>10.1f}" for r in bs_list]))
    print(f"{'  Restricted Cash (Current & Non-Curr)':<38} {OPENING_BS['restricted_cash']:>10.1f} " + " ".join([f"{r['restricted_cash']:>10.1f}" for r in bs_list]))
    print(f"{'  Accounts Receivable, net':<38} {OPENING_BS['ar']:>10.1f} " + " ".join([f"{r['ar']:>10.1f}" for r in bs_list]))
    print(f"{'  Property, Plant & Equipment, net':<38} {OPENING_BS['ppe']:>10.1f} " + " ".join([f"{r['ppe']:>10.1f}" for r in bs_list]))
    print(f"{'  Other Assets (Intangibles, Prepaids)':<38} {OPENING_BS['other_assets']:>10.1f} " + " ".join([f"{r['other_assets']:>10.1f}" for r in bs_list]))
    print(f"{'TOTAL ASSETS':<38} {'15790.0':>10} " + " ".join([f"{r['total_assets']:>10.1f}" for r in bs_list]))
    print("LIABILITIES & STOCKHOLDERS' EQUITY:")
    print(f"{'  Customer Prepayments (Deferred Rev)':<38} {OPENING_BS['deferred_rev']:>10.1f} " + " ".join([f"{r['deferred_rev']:>10.1f}" for r in bs_list]))
    print(f"{'  Term Debt & Finance Leases':<38} {OPENING_BS['term_debt']:>10.1f} " + " ".join([f"{r['term_debt']:>10.1f}" for r in bs_list]))
    print(f"{'  Drawn Liquidity / GPU Facility':<38} {OPENING_BS['liquidity_facility']:>10.1f} " + " ".join([f"{r['facility']:>10.1f}" for r in bs_list]))
    print(f"{'  Other Operating Liabilities':<38} {OPENING_BS['other_liab']:>10.1f} " + " ".join([f"{r['other_liab']:>10.1f}" for r in bs_list]))
    print(f"{'TOTAL LIABILITIES':<38} {'11604.4':>10} " + " ".join([f"{r['total_liab']:>10.1f}" for r in bs_list]))
    print(f"{'  Stockholders Equity':<38} {OPENING_BS['equity']:>10.1f} " + " ".join([f"{r['equity']:>10.1f}" for r in bs_list]))
    print(f"{'TOTAL LIABILITIES & EQUITY':<38} {'15790.0':>10} " + " ".join([f"{r['total_liab_equity']:>10.1f}" for r in bs_list]))

    # 3. Cash Flow Statement
    print("\n3. PRO-FORMA CASH FLOW & FCFE FINANCING SCHEDULE (USD millions)")
    print("-" * 105)
    cf_hdr = f"{'Metric / Line Item':<38} {'FY2026':>10} " + " ".join([f"FY{y}E".rjust(10) for y in YEARS])
    print(cf_hdr)
    print("-" * 105)
    print(f"{'GAAP Net Income (Loss)':<38} {'-702.6':>10} " + " ".join([f"{r['net_income']:>10.1f}" for r in cf_list]))
    print(f"{'(+) Depreciation & Amortization':<38} {'417.7':>10} " + " ".join([f"{r['depreciation']:>10.1f}" for r in cf_list]))
    print(f"{'(+) Asset Impairment (Non-Cash)':<38} {'638.8':>10} " + " ".join([f"{r['impairment']:>10.1f}" for r in cf_list]))
    print(f"{'(-) Change in Accounts Receivable':<38} {'-19.5':>10} " + " ".join([f"{-r['delta_ar']:>10.1f}" for r in cf_list]))
    print(f"{'(-) Change in Other Operating Assets':<38} {'-241.6':>10} " + " ".join([f"{-r['delta_other_assets']:>10.1f}" for r in cf_list]))
    print(f"{'(+) Change in Deferred Revenue (Prepay)':<38} {'1841.7':>10} " + " ".join([f"{r['delta_deferred_rev']:>10.1f}" for r in cf_list]))
    print(f"{'(+) Change in Other Liabilities':<38} {'165.9':>10} " + " ".join([f"{r['delta_other_liab']:>10.1f}" for r in cf_list]))
    print(f"{'OPERATING CASH FLOW (OCF)':<38} {'2100.4':>10} " + " ".join([f"{r['operating_cash_flow']:>10.1f}" for r in cf_list]))
    print(f"{'(-) Capital Expenditures (Capex)':<38} {'-4333.1':>10} " + " ".join([f"{-r['capex']:>10.1f}" for r in cf_list]))
    print(f"{'(-) Scheduled Debt Repayment':<38} {'-9.2':>10} " + " ".join([f"{-r['debt_repayment']:>10.1f}" for r in cf_list]))
    print(f"{'FREE CASH FLOW TO EQUITY (FCFE)':<38} {'-2241.9':>10} " + " ".join([f"{r['fcfe']:>10.1f}" for r in cf_list]))
    print(f"{'  FCFE Status Label':<38} {'negative':>10} " + " ".join([f"{('pos FCFE' if r['fcfe']>=0 else 'NEG FCFE'):>10}" for r in cf_list]))
    print("-" * 105)
    print("--- CASH RECONCILIATION (CASH COMPUTED LAST) ---")
    print(f"{'Beginning Cash Balance':<38} {'564.5':>10} " + " ".join([f"{r['cash_prev']:>10.1f}" for r in cf_list]))
    print(f"{'(+) Free Cash Flow to Equity':<38} {'-2241.9':>10} " + " ".join([f"{r['fcfe']:>10.1f}" for r in cf_list]))
    print(f"{'(+) Facility Draw / (-) Repayment':<38} {'0.0':>10} " + " ".join([f"{r['facility_draw'] - r['facility_repay']:>10.1f}" for r in cf_list]))
    print(f"{'ENDING CASH BALANCE':<38} {OPENING_BS['cash']:>10.1f} " + " ".join([f"{r['ending_cash']:>10.1f}" for r in cf_list]))

    # 4. Check Block
    print("\n" + "=" * 105)
    print("4. MODEL VALIDATION BLOCK & BALANCE INTEGRITY CHECKS")
    print("=" * 105)
    chk_hdr = f"{'Check Description':<40} " + " ".join([f"FY{c['year']}E".rjust(11) for c in checks])
    print(chk_hdr)
    print("-" * 105)
    gap_row = f"{'Assets - Liabilities - Equity (Gap)':<40} " + " ".join([f"{c['gap']:>+11.4f}" for c in checks])
    print(gap_row)
    cash_row = f"{'Cash >= Minimum ($500.0M) Buffer':<40} " + " ".join([f"{('PASS' if c['min_cash_pass'] else 'FAIL'):>11}" for c in checks])
    print(cash_row)
    fac_row = f"{'Credit Facility Drawn ($M)':<40} " + " ".join([f"{c['facility']:>11.1f}" for c in checks])
    print(fac_row)
    print("-" * 105)
    all_passed = all(abs(c["gap"]) <= 0.01 and c["min_cash_pass"] for c in checks)
    if all_passed:
        print(">>> ALL BALANCE SHEET & LIQUIDITY CHECKS PASSED: MODEL IS BALANCED (Gap = 0.0000). <<<")
    else:
        print(">>> WARNING: INTEGRITY CHECKS FAILED! <<<")

    # 5. Valuation Block
    print("\n" + "=" * 105)
    print("5. VALUATION SUMMARY & COMPARISON WITH MARKET")
    print("=" * 105)
    print(f"Cost of Equity (r_e):                 {p['cost_of_equity']*100:.2f}% (from Project-1/dcf.py & CAPM)")
    print(f"Terminal Growth Rate (g):              {p['terminal_growth']*100:.2f}% (from Project-1/dcf.py)")
    print(f"Shares Outstanding (10-K cover page):  {p['shares_outstanding']:.3f} million (as of August 14, 2026)")
    print(f"Shares Outstanding (June 30 BS):       {p['shares_bs_ending']:.3f} million")
    print(f"Shares Outstanding (Weighted Average): {p['shares_weighted_avg']:.3f} million (used in Project-1/dcf.py)")
    print("-" * 105)
    print("Explicit FCFE Schedule & Status:")
    for row in valuation["discounted_fcfe"]:
        print(f"  FY{row['year']}E: FCFE = ${row['fcfe']:>8.2f}M | Label: {row['status']:<14} | PV = ${row['pv']:>8.2f}M")
    print("-" * 105)
    print(f"Present Value of 5-Year Explicit FCFE: ${valuation['pv_explicit']:>10.2f} million")
    print(f"Terminal Value (at FY2031E):           ${valuation['terminal_value']:>10.2f} million")
    print(f"Present Value of Terminal Value:       ${valuation['pv_tv']:>10.2f} million")
    print(f"Total Implied Equity Value:            ${valuation['equity_value']:>10.2f} million")
    print(f"Terminal Value Share of Equity:         {valuation['pv_tv']/valuation['equity_value']*100 if valuation['equity_value']>0 else 0.0:>10.1f}%")
    print("-" * 105)
    print(f">>> IMPLIED VALUE PER SHARE (Primary: 394.06M shares):   ${valuation['value_per_share']:.2f}")
    print(f">>> IMPLIED VALUE PER SHARE (BS Ending: 380.19M shares): ${valuation['value_per_share_bs']:.2f}")
    print(f">>> IMPLIED VALUE PER SHARE (Weighted: 316.12M shares):  ${valuation['value_per_share_wa']:.2f}")
    print("-" * 105)
    print("MARKET COMPARISONS (VERIFIABLE DATED SOURCES):")
    print("  Date 1: September 3, 2026  | Market Closing Price: $41.65 (Source: NASDAQ / Lab 08 research)")
    print("  Date 2: September 24, 2026 | Market Trading Price: $45.73 (Source: Project-1 DCF baseline / NASDAQ)")
    print("-" * 105)
    val_primary = valuation['value_per_share']
    print(f"Question for Partner / Market:")
    print(f"\"The model implies a value of ${val_primary:.2f} per share, while the market priced IREN at $41.65 on September 3, 2026 "
          f"and $45.73 on September 24, 2026 on the same share count of {p['shares_outstanding']:.2f} million shares; does the market price "
          f"fully capture the multi-billion dollar capex inflection before contracted AI Cloud cash flows turn cash-positive?\"")
    print("=" * 105)


# ==============================================================================
# 6. AUTOMATED TEST SUITE (INCLUDING INTENTIONAL BREAK & REFUSAL VERIFICATION)
# ==============================================================================
def run_all_tests():
    """
    Executes mandatory Lab 10 verification suite:
    1. Base case test: verifies 5 years balance, all checks pass (Gap = 0.0000).
    2. Intentional break test: introduces balance sheet gap, verifies model REFUSES to value.
    3. Restores and confirms valid model.
    """
    print("\n" + "#" * 80)
    print("RUNNING LAB 10 VERIFICATION SUITE & REFUSAL GATES")
    print("#" * 80)

    # Test 1: Valid Base Case
    print("\n[TEST 1] Running Valid Base Case Engine...")
    base_output = run_proforma()
    try:
        base_val = calculate_valuation(base_output)
        print("  [PASS] Base case executed successfully. All checks balanced.")
    except Exception as e:
        print(f"  [FAIL] Base case failed: {e}")
        return False

    # Test 2: Intentional Break Test (Refusal Gate Verification)
    print("\n[TEST 2] Testing Refusal Gate: Intentionally breaking FY2028E cash by +$500.0M...")
    broken_cash = base_output["bs_list"][1]["cash"] + 500.0
    broken_output = run_proforma(broken_cash_year=2028, broken_cash_value=broken_cash)
    refusal_triggered = False
    try:
        calculate_valuation(broken_output)
        print("  [FAIL] Error: Model failed to refuse an invalid forecast!")
    except ValueError as ve:
        refusal_triggered = True
        print(f"  [PASS] Refusal successfully triggered as expected!")
        print(f"  Captured refusal error message:\n    >>> \"{ve}\"")

    if not refusal_triggered:
        return False

    # Test 3: Restore Valid Version
    print("\n[TEST 3] Restoring Valid Version and re-verifying integrity...")
    restored_output = run_proforma()
    restored_val = calculate_valuation(restored_output)
    print("  [PASS] Valid model restored and verified. All 5 years balance to 0.0000.\n")
    return True


if __name__ == "__main__":
    # If run with --test flag, run verification suite only
    if "--test" in sys.argv:
        success = run_all_tests()
        sys.exit(0 if success else 1)

    # Standard run: print full report and run tests
    output = run_proforma()
    val = calculate_valuation(output)
    print_model_report(output, val)
    run_all_tests()
