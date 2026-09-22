# FIN 439 Lab 09 — Pro-Forma Financial Modeling I: Build the Base Case
**Target Company:** Asbury Automotive Group, Inc. (NYSE: ABG)  
**Valuation / Projection Horizon:** FY2026E – FY2030E (Five-Year Explicit Forecast)  
**Student:** Elliott  
**Course:** FIN 43900 (AI Finance Applications, Purdue University)  
**Date:** September 22, 2026  

---

## 1. Executive Summary & Case Overview

This laboratory constructs and validates a fully integrated five-year, three-statement pro-forma financial model for **Asbury Automotive Group, Inc. (ABG)** covering fiscal years 2026 through 2030, anchored to an audited FY2025 opening balance sheet.

### Key Deliverables & Benchmark Calibration
1. **Three Fully Articulated Financial Statements:** Projected income statement, balance sheet, and equity cash flow statement with explicit operating and financing schedules.
2. **Strict Double-Entry Integrity:** Cash is computed **last** as the residual plug of all operating, investing, and financing decisions. The balance sheet identity ($\text{Assets} = \text{Liabilities} + \text{Equity}$) balances to **$0.0$** across every year of the projection.
3. **Automated Enforcement Barrier (`assert_balanced`):** The model halts and refuses valuation if any projected year exhibits a non-zero balance-sheet gap ($|\text{Gap}| \ge \$0.05\text{M}$) or violates the minimum liquidity requirement ($\text{Cash} \ge \$25.0\text{M}$).
4. **Exact Benchmark Calibration:** The base case reproduces the professor's known reference values to the exact decimal:
   - **FY2026E:** Revenue **$18,323.0M**, Operating Income **$844.2M**, Net Income **$413.6M**, FCFE **$211.4M**, Ending Cash **$101.8M**, Balance Gap **$0.0M**.
   - **FY2030E:** Revenue **$19,678.3M**, Operating Income **$971.4M**, Net Income **$527.5M**, FCFE **$342.3M**, Ending Cash **$719.8M**, Balance Gap **$0.0M**.
   - **Valuation Metrics:** Present Value of Explicit FCFE **$1,059.87M**, Discounted Terminal Value **$4,177.46M**, Total Implied Equity Value **$5,237.34M**, Terminal Value Share of Value **79.8%** (~80%), and Implied Value per Share of **$291.75** (exact match against the instructor target of $291.75).
5. **Broken-Cash Verification:** Overriding FY2026E cash with opening cash ($40.4M) triggers an immediate valuation refusal, correctly isolating `FY2026E` and reporting an exact **-$61.4 million** balance-sheet gap.

---

## 2. Define & Conceptual Answers

### Central Valuation Question
> **What are five years of a company's statements worth, built from assumptions you can defend, and how do you know the statements are right?**

### Prework Conceptual Q&A

#### 1. Which three judgments carry the ABG valuation?
While macroeconomic discount rates (Cost of Equity at 10.0% and Terminal Growth at 2.5%) set the discounting denominator, the three operational judgments that govern the numerator and carry ABG's intrinsic value are:
1. **Organic Revenue Growth (1.8% annually):** Asbury operates in a mature, cyclical automotive retail market. Assuming modest organic growth of 1.8% reflects steady dealership foot-traffic and parts/service demand without speculative acquisition ramp-ups.
2. **Gross Margin (17.05%):** Automotive dealership gross margins blend new vehicle sales (low single-digit margin), used vehicle sales, finance & insurance (F&I, nearly 100% margin), and parts & service (high margin). Fixing gross margin at 17.05% locks in post-pandemic normalization across sales and high-margin service lanes.
3. **SG&A Operating Leverage Trajectory (66.5% $\rightarrow$ 65.5% $\rightarrow$ 64.5% of Gross Profit):** In franchised dealerships, SG&A consists largely of salesperson commissions, advertising, and corporate overhead. Projecting SG&A to decline from 66.5% in 2026 to 64.5% by 2028 and remain flat thereafter represents structural cost rationalization and digital sales platform efficiencies. This 200 bps margin expansion is the primary engine driving operating income from $844.2M to $971.4M.

#### 2. Why is cash the last line the model computes?
In financial accounting, **cash is not an independent forecasting assumption; it is an economic residual (the "plug")**. 
- Every operating activity (revenue, gross margin, operating expenses, working capital changes), investing activity (capital expenditures), and financing decision (debt service, share repurchases, interest expenses) either deposits dollars into or drains dollars from the firm's bank account.
- If an analyst arbitrarily forecasts cash (e.g., assuming cash grows at 5% per year), the double-entry accounting identity ($\text{Assets} = \text{Liabilities} + \text{Equity}$) will fail unless another arbitrary line item is forced to absorb the discrepancy.
- Computing cash last guarantees **conservation of value**: cash equals prior cash plus net cash generated during the year minus distributions. It also avoids circular circularity between cash balances, debt draws, and interest income/expense.

#### 3. Why is a balance sheet that does not balance a bug, not a forecast?
An unbalanced balance sheet means debits do not equal credits somewhere in the model's logic. In economic terms, value has either been spontaneously created out of nothing or destroyed into a void. Any DCF or equity valuation derived from an unbalanced model is mathematically meaningless because the cash flows discounting into equity do not reconcile with the capital structure supporting the business.

#### 4. Floor-Plan Financing: Mechanics and the -$1.1B Impact
- **What it is:** Floor-plan financing consists of specialized, asset-backed inventory revolving lines of credit extended to automobile dealerships by vehicle manufacturers' captive finance arms (e.g., Ford Motor Credit, GM Financial) and commercial banks.
- **How it works:** When a dealership orders new vehicles from the factory, the floor-plan lender pays the manufacturer directly. The loan is collateralized by the specific vehicle vehicle identification numbers (VINs). As Asbury sells cars off the lot, it immediately pays off the corresponding floor-plan note. Consequently, floor-plan debt expands and contracts directly with inventory ($2,027.0M \div 2,135.8M = 94.906\%$). Interest expense is incurred on the opening balance (4.67%).
- **Why it is treated as operating inside FCFE:** Because dealerships cannot operate or hold inventory without floor-plan lines, changes in floor-plan debt are treated as an operating working capital source/use rather than corporate capital structure debt.
- **Why removing the floor-plan line crashes cash to -$1.1 Billion:** Asbury holds over $2.1 billion of vehicle inventory. In the pro-forma engine, 94.9% of that inventory is funded by floor-plan lenders. If floor-plan loans are removed or classified outside operating cash flow, Asbury would have to fund $2.1B+ in physical car inventory entirely out of its own equity cash reserves. Lacking over $2 billion in operating cash flow to cover working capital, Asbury would burn through its starting cash of $40.4M immediately and plunge into a catastrophic cumulative cash deficit of approximately -$1.1 billion by 2030.

---

## 3. Represent — Assumption Set & Opening Financial Position

### Model Assumption Set (FY2026E – FY2030E)

The table below catalogs every model input, categorized under the strict taxonomy of **History**, **Guidance**, **Judgment**, or **Fact**, along with the exact mathematical formulation:

| Assumption Metric | Model Value | Label | Sourced Origin & Exact Computational Formula |
| :--- | :---: | :---: | :--- |
| **Organic Revenue Growth** | 1.8% per year | **judgment** | Mature automotive retail industry baseline; applied as $\text{Rev}_t = \text{Rev}_{t-1} \times (1 + 0.018)$. |
| **Gross Margin** | 17.05% | **judgment** | Dealership blended product/service margin; $\text{Gross Profit}_t = \text{Rev}_t \times 0.1705$. |
| **SG&A $\div$ Gross Profit** | 66.5%, 65.5%, 64.5%, 64.5%, 64.5% | **judgment** | Operating leverage trajectory: 2026: 66.5%; 2027: 65.5%; 2028–2030: 64.5%. |
| **Depreciation $\div$ Opening PP&E** | 82.4 $\div$ 3,070.4 (2.68369%) | **history** | Historical FY2025 ratio of depreciation (\$82.4M) to year-end PP&E (\$3,070.4M). |
| **Impairment (Non-Cash)** | $120.0M per year | **judgment** | Normalized annual non-cash franchise/goodwill amortization and impairment charge. |
| **Capital Expenditures (Capex)** | $250.0M per year | **guidance** | Dealership facility maintenance, upgrades, and IT infrastructure investments. |
| **Effective Tax Rate** | 25.5% | **judgment** | Statutory federal plus blended state corporate tax rate; $\text{Tax} = \max(0, \text{EBT}) \times 0.255$. |
| **Inventory Days** | 52.2274 days | **history** | $\frac{2,135.8}{17,999.0 - 3,071.7} \times 365 = \frac{2,135.8}{14,927.3} \times 365$. $\text{Inv}_t = \text{COGS}_t \times \frac{\text{Days}}{365}$. |
| **Floor Plan $\div$ Inventory** | 2,027.0 $\div$ 2,135.8 (94.90589%) | **history** | Historical FY2025 loan-to-inventory ratio; $\text{Floor Plan}_t = \text{Inv}_t \times 0.9490589$. |
| **Other Working Capital Ratio** | 0.8% of $\Delta\text{Revenue}$ | **judgment** | $\Delta\text{OWC}_t = 0.008 \times (\text{Rev}_t - \text{Rev}_{t-1})$; $\text{Other Assets}_t = \text{Other Assets}_{t-1} + \Delta\text{OWC}_t - \text{Impairment}_t$. |
| **Minimum Cash Requirement** | $25.0M | **history** | Minimum operating cash liquidity buffer required across dealership store network. |
| **Revolver Facility Limit** | $850.0M | **judgment** | Maximum borrowing capacity under senior revolving credit agreement. |
| **Revolver Borrowing Rate** | 6.00% | **judgment** | Benchmark short-term borrowing spread; applied to opening revolver balance. |
| **Floor-Plan Interest Rate** | 4.67% | **history** | FY2025 effective borrowing rate on floor-plan notes; applied to opening floor plan. |
| **Term Debt Interest Rate** | 5.44% | **history** | FY2025 effective contractual coupon on long-term notes; applied to opening term debt. |
| **Term Debt Annual Repayment** | $150.0M per year | **judgment** | Contractual principal amortization schedule; $\text{Debt}_t = \text{Debt}_{t-1} - 150.0$. |
| **Share Repurchase (Buyback)** | $150.0M per year | **judgment** | Capital return policy; cash outflow of \$150.0M, reduces ending equity by \$150.0M. |
| **Cost of Equity ($r_e$)** | 10.0% | **judgment** | Equity hurdle rate reflecting dealership market risk and financial leverage. |
| **Terminal Growth Rate ($g$)** | 2.5% | **judgment** | Perpetual long-term growth rate aligned with long-run GDP expansion. |
| **Diluted Common Shares** | 17.951349 million | **fact** | Official share count from Asbury Form 10-Q for the quarter ended June 30, 2026. |

---

### Opening Balance Sheet (FY2025, USD millions)

The model is initialized on Asbury's actual FY2025 year-end balance sheet, verifying exact equality:

$$\text{Total Assets} = 40.4 + 2,135.8 + 3,070.4 + 6,371.6 = \mathbf{\$11,618.2\text{ million}}$$
$$\text{Total Liabilities \& Equity} = 2,027.0 + 3,572.0 + 0.0 + 2,127.5 + 3,891.7 = \mathbf{\$11,618.2\text{ million}}$$
$$\text{Balance Sheet Gap} = \$11,618.2 - \$11,618.2 = \mathbf{\$0.0\text{ million}}$$

| Line Item | FY2025 Balance ($M) | Line Item | FY2025 Balance ($M) |
| :--- | :---: | :--- | :---: |
| **Cash and Cash Equivalents** | $40.4 | **Floor-Plan Notes Payable** | $2,027.0 |
| **Inventories** | $2,135.8 | **Long-Term Term Debt** | $3,572.0 |
| **Property, Plant & Equipment (net)** | $3,070.4 | **Revolving Credit Facility** | $0.0 |
| **Other Assets** | $6,371.6 | **Other Liabilities** | $2,127.5 |
| | | **Shareholders' Equity** | $3,891.7 |
| **TOTAL ASSETS** | **$11,618.2** | **TOTAL LIABILITIES & EQUITY** | **$11,618.2** |

---

## 4. Implement — The Five-Year Three-Statement Engine

The simulation engine was developed in standard Python (`proforma.py`), requiring zero external dependencies. Each projected year executes in a strict four-stage sequence:

```
┌────────────────────────────────────────────────────────────────────────┐
│ STAGE 1: INCOME STATEMENT                                              │
│ Revenue -> Gross Profit -> SG&A -> D&A -> Impairment -> EBIT           │
│ Interest (on Opening Balances) -> Pretax Income -> Tax -> Net Income   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ STAGE 2: BALANCE SHEET (EXCEPT CASH)                                   │
│ Inventory (Days) -> Floor Plan (Ratio) -> PP&E (Capex/Depr)            │
│ Other Assets (OWC/Impairment) -> Debt (Repayment) -> Equity (Buyback)  │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ STAGE 3: FREE CASH FLOW TO EQUITY (FCFE)                               │
│ NI + D&A + Impairment - Capex - dInv - dOWC + dFloorPlan - Repayment   │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
┌──────────────────────────────────▼─────────────────────────────────────┐
│ STAGE 4: CASH & REVOLVER LIQUIDITY (CASH CALCULATED LAST)              │
│ Unadjusted Cash = Opening Cash + FCFE - Buyback                        │
│ If Cash < Min: Draw Revolver | If Cash > Min & Revolver > 0: Repay     │
│ Enforce: Total Assets = Total Liabilities + Shareholders' Equity       │
└────────────────────────────────────────────────────────────────────────┘
```

### 1. Pro-Forma Income Statement (FY2025 – FY2030E)

*(USD millions, displayed to one decimal place)*

| Line / Metric | FY2025 | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Revenue** | 17,999.0 | **18,323.0** | 18,652.8 | 18,988.5 | 19,330.3 | **19,678.3** |
| Cost of Sales | 14,927.3 | 15,198.9 | 15,472.5 | 15,751.0 | 16,034.5 | 16,323.1 |
| **Gross Profit** | 3,071.7 | 3,124.1 | 3,180.3 | 3,237.5 | 3,295.8 | 3,355.1 |
| SG&A Expense | — | 2,077.5 | 2,083.1 | 2,088.2 | 2,125.8 | 2,164.1 |
| Depreciation Expense | — | 82.4 | 86.9 | 91.3 | 95.5 | 99.7 |
| Impairment (Non-Cash) | — | 120.0 | 120.0 | 120.0 | 120.0 | 120.0 |
| **Operating Income (EBIT)** | — | **844.2** | 890.3 | 938.1 | 954.5 | **971.4** |
|   Floor-Plan Interest | — | 94.7 | 96.4 | 98.1 | 99.9 | 101.7 |
|   Term Debt Interest | — | 194.3 | 186.2 | 178.0 | 169.8 | 161.7 |
|   Revolver Interest | — | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Total Interest Expense | — | 289.0 | 282.5 | 276.1 | 269.7 | 263.4 |
| Pretax Income (EBT) | — | 555.2 | 607.8 | 661.9 | 684.8 | 708.0 |
| Income Tax Expense (25.5%) | — | 141.6 | 155.0 | 168.8 | 174.6 | 180.5 |
| **Net Income** | — | **413.6** | 452.8 | 493.1 | 510.1 | **527.5** |

---

### 2. Pro-Forma Balance Sheet (FY2025 – FY2030E)

*(USD millions, displayed to one decimal place)*

| Line / Metric | FY2025 | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **ASSETS:** | | | | | | |
|   Cash and Cash Equivalents | 40.4 | **101.8** | 206.9 | 356.6 | 527.5 | **719.8** |
|   Inventories | 2,135.8 | 2,174.7 | 2,213.8 | 2,253.7 | 2,294.2 | 2,335.5 |
|   Property, Plant & Equipment (net) | 3,070.4 | 3,238.0 | 3,401.1 | 3,559.8 | 3,714.3 | 3,864.6 |
|   Other Assets | 6,371.6 | 6,254.2 | 6,136.8 | 6,019.5 | 5,902.3 | 5,785.0 |
| **TOTAL ASSETS** | **11,618.2** | **11,768.7** | **11,958.6** | **12,189.6** | **12,438.2** | **12,704.9** |
| **LIABILITIES & EQUITY:** | | | | | | |
|   Floor-Plan Notes Payable | 2,027.0 | 2,063.9 | 2,101.0 | 2,138.9 | 2,177.4 | 2,216.5 |
|   Term Debt | 3,572.0 | 3,422.0 | 3,272.0 | 3,122.0 | 2,972.0 | 2,822.0 |
|   Revolving Credit Facility | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
|   Other Liabilities | 2,127.5 | 2,127.5 | 2,127.5 | 2,127.5 | 2,127.5 | 2,127.5 |
| **TOTAL LIABILITIES** | **7,726.5** | **7,613.4** | **7,500.5** | **7,388.4** | **7,276.9** | **7,166.0** |
|   Shareholders' Equity | 3,891.7 | 4,155.3 | 4,458.1 | 4,801.2 | 5,161.4 | 5,538.9 |
| **TOTAL LIABILITIES & EQUITY** | **11,618.2** | **11,768.7** | **11,958.6** | **12,189.6** | **12,438.2** | **12,704.9** |

---

### 3. Pro-Forma Cash Flow & Equity Financing Schedule (FY2025 – FY2030E)

*(USD millions, displayed to one decimal place)*

| Line / Metric | FY2025 | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Net Income** | — | 413.6 | 452.8 | 493.1 | 510.1 | 527.5 |
| (+) Depreciation Expense | — | 82.4 | 86.9 | 91.3 | 95.5 | 99.7 |
| (+) Impairment (Non-Cash) | — | 120.0 | 120.0 | 120.0 | 120.0 | 120.0 |
| (-) Capital Expenditures (Capex) | — | -250.0 | -250.0 | -250.0 | -250.0 | -250.0 |
| (-) Change in Inventories | — | -38.9 | -39.1 | -39.8 | -40.6 | -41.3 |
| (-) Change in Other Working Capital | — | -2.6 | -2.6 | -2.7 | -2.7 | -2.8 |
| (+) Change in Floor-Plan Notes | — | 36.9 | 37.1 | 37.8 | 38.5 | 39.2 |
| (-) Term Debt Principal Repayment | — | -150.0 | -150.0 | -150.0 | -150.0 | -150.0 |
| **FREE CASH FLOW TO EQUITY (FCFE)** | — | **211.4** | 255.1 | 299.7 | 320.9 | **342.3** |
| *--- CASH RECONCILIATION ---* | | | | | | |
| Beginning Cash Balance | — | 40.4 | 101.8 | 206.9 | 356.6 | 527.5 |
| (+) Free Cash Flow to Equity | — | 211.4 | 255.1 | 299.7 | 320.9 | 342.3 |
| (-) Share Repurchases (Buyback) | — | -150.0 | -150.0 | -150.0 | -150.0 | -150.0 |
| (+) Revolver Borrowing / (-) Repayment | — | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **ENDING CASH BALANCE** | **40.4** | **101.8** | **206.9** | **356.6** | **527.5** | **719.8** |

---

## 5. Validate — Benchmark Comparison & Refusal Proof

### Side-by-Side Comparison Against Professor's Reference Table

The table below contrasts our engine output against every reference benchmark specified in the Lab 09 instructions:

| Model Line Item | Lab 09 FY2026E Target | Model FY2026E Result | Lab 09 FY2030E Target | Model FY2030E Result | Status / Audit |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Revenue** | $18,323.0 | **$18,323.0** | $19,678.3 | **$19,678.3** | **PASS (Exact Match)** |
| **Operating Income (EBIT)** | $844.2 | **$844.2** | $971.4 | **$971.4** | **PASS (Exact Match)** |
| **Net Income** | $413.6 | **$413.6** | $527.5 | **$527.5** | **PASS (Exact Match)** |
| **Free Cash Flow to Equity** | $211.4 | **$211.4** | $342.3 | **$342.3** | **PASS (Exact Match)** |
| **Ending Cash Balance** | $101.8 | **$101.8** | $719.8 | **$719.8** | **PASS (Exact Match)** |
| **Assets − Liabilities − Equity** | $0.0 | **$0.0** | $0.0 | **$0.0** | **PASS (Exact Match)** |
| **Share of Value After 2030** | ~80% | **79.8%** | — | — | **PASS (Consistent)** |
| **Implied Value per Share** | **$291.75** | **$291.75** | — | — | **PASS (Exact Match)** |

---

### Valuation Mathematics & Terminal Value Formulation

$$\text{PV of Explicit FCFE} = \sum_{t=1}^{5} \frac{\text{FCFE}_t}{(1 + r_e)^t} = \frac{211.4}{1.10^1} + \frac{255.1}{1.10^2} + \frac{299.7}{1.10^3} + \frac{320.9}{1.10^4} + \frac{342.3}{1.10^5} = \mathbf{\$1,059.87\text{ million}}$$

$$\text{Terminal Value}_{2030} = \frac{(\text{FCFE}_{2030} + \text{Repayment}_{2030}) \times (1 + g)}{r_e - g} = \frac{(342.327 + 150.0) \times (1 + 0.025)}{0.10 - 0.025} = \mathbf{\$6,727.85\text{ million}}$$

$$\text{PV of Terminal Value} = \frac{\$6,727.85}{(1.10)^5} = \mathbf{\$4,177.46\text{ million}}$$

$$\text{Total Equity Value} = \$1,059.87 + \$4,177.46 = \mathbf{\$5,237.34\text{ million}}$$

$$\text{Share of Value After 2030} = \frac{\$4,177.46}{\$5,237.34} = \mathbf{79.76\% \approx 79.8\%}$$

$$\text{Value per Diluted Share} = \frac{\$5,237.336\text{ million}}{17.951349\text{ million shares}} = \mathbf{\$291.7517} \rightarrow \mathbf{\$291.75}$$

---

## 6. The Broken-Cash Test & Integrity Diagnostics

### Verification Protocol
Per Section V of the instructor instructions:
> *"In your partner's file, set 2026 cash to the opening 40.4 instead of the computed figure and run it. Expect: the model refuses, naming FY2026E and a gap of −61.4 — the year's change in cash with the sign flipped. Undo the change. A model that does not refuse has not been checked."*

We executed this exact failure test using `python proforma.py --broken-cash`.

### Execution Log
```
################################################################################
RUNNING REQUIRED BROKEN-CASH TEST: Overriding FY2026E cash with opening $40.4M...
################################################################################

Validation checks output:
  FY2026E: Gap = -61.44, Cash = $40.4M, Min Cash = True
  FY2027E: Gap = -61.44, Cash = $145.5M, Min Cash = True
  FY2028E: Gap = -61.44, Cash = $295.2M, Min Cash = True
  FY2029E: Gap = -61.44, Cash = $466.0M, Min Cash = True
  FY2030E: Gap = -61.44, Cash = $658.3M, Min Cash = True

Calling assert_balanced()...

SUCCESS: assert_balanced() refused valuation as expected!
Caught Exception: Balance sheet does not balance in FY2026E: gap of -61.4 million (Assets: 11707.3, Liab+Equity: 11768.7). Model refuses to calculate valuation.
```

### What the -$61.4 Million Tells You Before Opening a Single Cell
1. **Mathematical Meaning:** During FY2026E, Asbury generated $\$211.4\text{M}$ in Free Cash Flow to Equity and spent $\$150.0\text{M}$ on share repurchases, yielding a net positive cash generation of:
   $$\Delta\text{Cash}_{2026} = \text{FCFE}_{2026} - \text{Buyback}_{2026} = \$211.44\text{M} - \$150.00\text{M} = \mathbf{+\$61.44\text{ million}}$$
   Ending cash should have increased from $\$40.4\text{M}$ to $\$101.8\text{M}$.
2. **The Nature of the Bug:** By arbitrarily pinning ending cash at $\$40.4\text{M}$, total assets were underreported by exactly $\$61.44\text{M}$, while liabilities and equity remained fully updated to reflect $\$413.6\text{M}$ in net income.
3. **The Balance-Sheet Diagnostic:** The resulting gap is:
   $$\text{Gap} = \text{Assets} - (\text{Liabilities} + \text{Equity}) = -\$61.44\text{ million}$$
   Before inspecting any code, seeing a gap of $-\$61.4\text{M}$ immediately signals that **the balance sheet is missing the exact net cash generation of the period**. The model is leaking $\$61.4\text{M}$ of equity value into thin air.

---

## 7. Primary Traceable Sources

1. **Asbury Automotive Group, Inc. — Form 10-K for the Fiscal Year Ended December 31, 2025**
   - **Filing Date:** February 2026
   - **Commission File Number:** 001-31261
   - **SEC EDGAR Search:** [SEC EDGAR ABG Filings](https://www.sec.gov/edgar/browse/?CIK=0001144980)
   - **Sourced Inputs:** FY2025 Revenue ($17,999.0M), Gross Profit ($3,071.7M), Depreciation ($82.4M), Inventory ($2,135.8M), Net PP&E ($3,070.4M), Other Assets ($6,371.6M), Cash ($40.4M), Floor-Plan Notes ($2,027.0M), Term Debt ($3,572.0M), Other Liabilities ($2,127.5M), Common Equity ($3,891.7M).
2. **Asbury Automotive Group, Inc. — Form 10-Q for the Period Ended June 30, 2026**
   - **Filing Date:** July 2026
   - **Sourced Input:** Diluted common shares outstanding of **17,951,349 shares** (Cover page and Item 1 note on share count).
3. **FIN 439 Course Materials & Tutorial Reference Key**
   - **Tutorial:** *Pro-Forma Valuation with AI, Part 1 — Build the base case* (Prof. Lecture Slides & Spoken Notes, `pro-forma-abg-tutorial.md`).
   - **Lab Assignment:** *FIN 439 Week 5: Lab 09 — Pro-Forma Build: the Engine and the Known Answer*.
   - **Benchmark Reference Values:** FY2026E/FY2030E target lines, TV formula, and Target Value per Share of **$291.75**.

---

## 8. Academic Integrity & AI Assistance Disclosure

This report, financial model (`proforma.py`), and documentation were completed for **FIN 43900 (AI Finance Applications, Purdue University)** as part of Laboratory 09.

**AI Assistance Disclosure:**  
Model development and documentation were drafted with the assistance of **Google Antigravity / AI Coding Assistant**. In accordance with course guidelines:
- All financial assumptions, formulas, and balance sheet linkages were audited against the instructor's Lab 09 specification.
- The Python pro-forma simulation engine was constructed using the Python Standard Library only.
- All validation checks, benchmark comparisons ($291.75 target share price), and broken-cash refusal diagnostics (-$61.4M gap) were executed and independently verified by the student.
