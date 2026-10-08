"""Five-year FCFF discounted cash flow model (USD millions).

HISTORICAL ARTIFACT & FAILURE RECORD (Week 3 Baseline):
This script represents the early Week 3 DCF engine adapted from Lab 05. 
When applied to IREN Limited with STARTING_FCFF = -2191.19M (FY2026 actual),
applying positive growth rates directly to a negative cash flow base compounds
the negative deficit (reaching -$6,321M in Year 5), producing an enterprise value
of -$60.4B and an implied equity value of -$196.34 per share. This also causes
the Reverse DCF bisection solver to fail because positive target share prices
cannot be bracketed with negative cash flows.

This script is preserved intact as required historical evidence under the project
rubric. The mechanical failure was diagnosed and superseded by the 5-year 
three-statement integrated pro-forma engine built in Lab 10 and run_analysis.py.
"""

# Editable inputs (USD millions, except rates and diluted shares)
STARTING_FCFF = 100.0
GROWTH_RATES = [0.08, 0.06, 0.05, 0.04, 0.03]
WACC = 0.10
TERMINAL_GROWTH = 0.03
NON_OPERATING_CASH = 50.0
DEBT = 300.0
DILUTED_SHARES = 50.0
# Configured for IREN Limited (FY2026 Form 10-K)
STARTING_FCFF = -2191.19
GROWTH_RATES = [0.50, 0.35, 0.20, 0.12, 0.06]
WACC = 0.114
TERMINAL_GROWTH = 0.025
NON_OPERATING_CASH = 5895.59
DEBT = 7592.94
DILUTED_SHARES = 316.12

# Sensitivity grid inputs
WACC_LIST = [0.104, 0.114, 0.124]
TERMINAL_GROWTH_LIST = [0.020, 0.025, 0.030]

# Reverse DCF inputs
TARGET_SHARE_PRICE = 45.73  # IREN closing share price ($)
REVERSE_DCF_LOWER_BOUND = -5.0   # in percentage points
REVERSE_DCF_UPPER_BOUND = 10.0   # in percentage points


def calculate_dcf(starting_fcff, growth_rates, wacc, terminal_growth, cash, debt, shares):
    """Calculate DCF valuation metrics."""
    if len(growth_rates) != 5:
        raise ValueError("Enter exactly five yearly growth rates.")
    if terminal_growth >= wacc:
        return None
    if shares <= 0:
        raise ValueError("Diluted shares must be greater than zero.")

    fcff = starting_fcff
    yearly_fcff = []
    for growth_rate in growth_rates:
        fcff *= 1.0 + growth_rate
        yearly_fcff.append(fcff)

    pv_explicit = sum(
        cf / (1.0 + wacc) ** year
        for year, cf in enumerate(yearly_fcff, start=1)
    )
    terminal_value_year_5 = (
        yearly_fcff[-1] * (1.0 + terminal_growth) / (wacc - terminal_growth)
    )
    pv_terminal_value = terminal_value_year_5 / (1.0 + wacc) ** 5
    enterprise_value = pv_explicit + pv_terminal_value
    equity_value = enterprise_value + cash - debt
    value_per_diluted_share = equity_value / shares
    tv_share_ev = (
        pv_terminal_value / enterprise_value if enterprise_value != 0 else 0.0
    )

    return {
        "yearly_fcff": yearly_fcff,
        "pv_explicit": pv_explicit,
        "tv5": terminal_value_year_5,
        "pv_tv": pv_terminal_value,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "value_per_diluted_share": value_per_diluted_share,
        "tv_share_ev": tv_share_ev,
    }


def solve_reverse_dcf(starting_fcff, base_growth_rates, wacc, terminal_growth,
                      cash, debt, shares, target_price, lower_pct, upper_pct):
    """Solve for uniform growth rate shift using bisection."""
    min_growth = min(base_growth_rates)
    if (min_growth + lower_pct / 100.0) <= -1.0:
        return None, "Bracket refused: pushes an annual growth rate to -100% or below."
    if (min_growth + upper_pct / 100.0) <= -1.0:
        return None, "Bracket refused: pushes an annual growth rate to -100% or below."

    def price_for_shift(shift_pct):
        shift = shift_pct / 100.0
        shifted_rates = [g + shift for g in base_growth_rates]
        res = calculate_dcf(
            starting_fcff, shifted_rates, wacc, terminal_growth, cash, debt, shares
        )
        if res is None:
            return None
        return res["value_per_diluted_share"]

    p_low = price_for_shift(lower_pct)
    p_high = price_for_shift(upper_pct)

    if p_low is None or p_high is None:
        return None, "Invalid DCF calculation at search boundaries."

    f_low = p_low - target_price
    f_high = p_high - target_price

    if f_low * f_high > 0:
        return (
            None,
            f"No solution in that bracket [{lower_pct:+.2f}%, {upper_pct:+.2f}%]: "
            f"model price range is [${p_low:.2f}, ${p_high:.2f}] vs target ${target_price:.2f}."
        )

    low = lower_pct
    high = upper_pct
    for _ in range(100):
        mid = (low + high) / 2.0
        p_mid = price_for_shift(mid)
        f_mid = p_mid - target_price
        if abs(f_mid) < 1e-7 or abs(high - low) < 1e-7:
            return mid, None
        if f_low * f_mid > 0:
            low = mid
            f_low = f_mid
        else:
            high = mid
            f_high = f_mid

    return mid, None


def main():
    if len(GROWTH_RATES) != 5:
        raise ValueError("Enter exactly five yearly growth rates.")
    if TERMINAL_GROWTH >= WACC:
        raise ValueError(
            "Terminal growth must be less than WACC; the Gordon-growth formula "
            "is not valid when terminal growth is greater than or equal to WACC."
        )
    if DILUTED_SHARES <= 0:
        raise ValueError("Diluted shares must be greater than zero.")

    # 1. Base DCF - Exact twelve lines printed
    base_res = calculate_dcf(
        STARTING_FCFF, GROWTH_RATES, WACC, TERMINAL_GROWTH,
        NON_OPERATING_CASH, DEBT, DILUTED_SHARES
    )

    for year, cash_flow in enumerate(base_res["yearly_fcff"], start=1):
        print(f"FCFF Year {year}: {cash_flow:.4f}")
    print(f"Present Value of Explicit FCFF: {base_res['pv_explicit']:.4f}")
    print(f"Terminal Value at Year 5: {base_res['tv5']:.4f}")
    print(f"Present Value of Terminal Value: {base_res['pv_tv']:.4f}")
    print(f"Enterprise Value: {base_res['enterprise_value']:.4f}")
    print(f"Equity Value: {base_res['equity_value']:.4f}")
    print(f"Value per Diluted Share: {base_res['value_per_diluted_share']:.4f}")
    print(f"PV Terminal Value as Share of Enterprise Value: {base_res['tv_share_ev']:.4f}")

    # 2. Sensitivity Grid
    print("\n--- Sensitivity Grid: Value per Diluted Share ($) ---")
    header = f"{'WACC \\ g_term':<15}" + "".join(f"{tg*100:>10.1f}%" for tg in TERMINAL_GROWTH_LIST)
    print(header)
    print("-" * len(header))
    for w in WACC_LIST:
        row_str = f"{w*100:>6.1f}%        "
        for tg in TERMINAL_GROWTH_LIST:
            if tg >= w:
                row_str += f"{'Invalid':>11}"
            else:
                grid_res = calculate_dcf(
                    STARTING_FCFF, GROWTH_RATES, w, tg,
                    NON_OPERATING_CASH, DEBT, DILUTED_SHARES
                )
                if grid_res is None:
                    row_str += f"{'Invalid':>11}"
                else:
                    row_str += f"{grid_res['value_per_diluted_share']:>11.2f}"
        print(row_str)

    # 3. Reverse DCF
    print("\n--- Reverse DCF Analysis ---")
    solved_shift, err_msg = solve_reverse_dcf(
        STARTING_FCFF, GROWTH_RATES, WACC, TERMINAL_GROWTH,
        NON_OPERATING_CASH, DEBT, DILUTED_SHARES,
        TARGET_SHARE_PRICE, REVERSE_DCF_LOWER_BOUND, REVERSE_DCF_UPPER_BOUND
    )
    print(f"Target Share Price: ${TARGET_SHARE_PRICE:.2f}")
    print("Fixed Inputs Held Fixed:")
    print(f"  Starting FCFF: ${STARTING_FCFF:.2f}M")
    print(f"  Base Growth Rates: {[f'{g*100:.1f}%' for g in GROWTH_RATES]}")
    print(f"  WACC: {WACC*100:.2f}%")
    print(f"  Terminal Growth: {TERMINAL_GROWTH*100:.2f}%")
    print(f"  Non-Operating Cash: ${NON_OPERATING_CASH:.2f}M")
    print(f"  Debt: ${DEBT:.2f}M")
    print(f"  Diluted Shares: {DILUTED_SHARES:.2f}M")
    print(f"Search Bounds for Uniform Shift: [{REVERSE_DCF_LOWER_BOUND:+.2f} pts, {REVERSE_DCF_UPPER_BOUND:+.2f} pts]")

    if solved_shift is not None:
        print(f"Solved Uniform Shift: {solved_shift:+.4f} percentage points ({solved_shift:+.2f} pts)")
        implied_rates = [g + solved_shift / 100.0 for g in GROWTH_RATES]
        print(f"Implied Explicit Growth Rates: {[f'{r*100:.2f}%' for r in implied_rates]}")
    else:
        print(f"Reverse DCF Status: {err_msg}")


if __name__ == "__main__":
    main()
