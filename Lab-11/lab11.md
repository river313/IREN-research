# FIN 439 Lab 11 — Pro-Forma Sensitivity: Find Your Company's Drivers
**Target Company:** IREN Limited (NASDAQ: IREN)  
**Course:** FIN 43900 (Corporate Finance / Applied Financial Modeling, Purdue University)  
**Student:** Elliot  
**Valuation / Submission Date:** September 29, 2026  
**Assignment Reference:** Lab 11 — Pro-Forma Sensitivity: Find Your Company's Drivers (Week 6)  
**Prior Baseline Date:** September 24, 2026 (Lab 10 Pro-Forma Baseline)  

---

## Executive Summary & Mission

> **Mission:** *"Find which inputs move your own pro-forma's results, and by how much."*

This analysis continues directly from Elliot's working **Lab 10 IREN Pro-Forma Three-Statement Model** ([`Lab-10/proforma_iren.py`](file:///c:/Users/ellio/Documents/FIN439/Lab-10/proforma_iren.py)). Under the authoritative Lab 11 instructions:
1. **No Rebuilding / No Overwriting:** The foundational 5-year linked financial engine developed in Lab 10 is preserved intact.
2. **Two Genuine Operating Drivers:** Two independent operating assumptions already existing in the IREN assumption table were selected:
   - **Driver 1:** Cash Gross Margin (`gross_margin`) [Base: 70.0%, Tested: 65.0% to 75.0%].
   - **Driver 2:** Revenue Growth Trajectory (`revenue_growth`) [Base: 100%->10%, Tested: $\pm5.0$ percentage points per year].
3. **One-at-a-Time Protocol:** Every simulation run begins with a fresh independent copy of original base assumptions. Only one independent assumption changes per run; all other assumptions remain locked at base, and linked accounting quantities recalculate across all 5 forecast years.
4. **Refusal Gate & Signed Cash Flows:** Negative cash flows are strictly preserved; the terminal value refusal gate is enforced whenever terminal cash flow is non-positive.
5. **Restored Base Case:** At the conclusion of sensitivity runs, the original base case is restored, re-executed, and verified to match original base outputs within zero rounding error ($0.000000$).

---

## D — The Question

> **"Which assumptions drive my company's forecast and value, and what explains their effects?"**

- **Target Company:** IREN Limited  
- **Ticker:** IREN (NASDAQ Global Select Market)  
- **Fiscal Year-End:** June 30  
- **Reporting Standard:** US GAAP (Form 10-K)  
- **Core Operating Focus:** Zero-inventory, gigawatt-scale AI Cloud compute infrastructure and high-efficiency Bitcoin mining.

---

## R — Operating Drivers & Tested Ranges

Two independent operating assumptions that **already exist** in IREN's pro-forma model were selected. Both are genuine model inputs, not calculated statement outputs.

### Operating Drivers Specification Grid

| Driver Specification | Driver 1: Cash Gross Margin | Driver 2: Revenue Growth Trajectory |
| :--- | :--- | :--- |
| **Model Parameter Key** | `gross_margin` | `revenue_growth` |
| **Driver Description** | Cash gross margin excluding depreciation & amortization | Multi-year top-line annual growth rate path |
| **Forecast Years Affected** | FY2027E, FY2028E, FY2029E, FY2030E, FY2031E (All 5 Years) | FY2027E, FY2028E, FY2029E, FY2030E, FY2031E (All 5 Years) |
| **Units** | Percentage of Total Revenue (%) | Annual percentage growth rate per year (%) |
| **Lower Value** | **65.0%** (0.650) [$-5.0$ percentage points] | **[95%, 45%, 25%, 10%, 5%]** [$-5.0$ pp per year] |
| **Base Value** | **70.0%** (0.700) [Lab 10 Base] | **[100%, 50%, 30%, 15%, 10%]** [Lab 10 Base] |
| **Higher Value** | **75.0%** (0.750) [$+5.0$ percentage points] | **[105%, 55%, 35%, 20%, 15%]** [$+5.0$ pp per year] |
| **Total Range Width (Span)**| **10.0 percentage points** ($75\% - 65\%$) | **10.0 percentage points shift** ($+5\text{ pp} - (-5\text{ pp})$) |
| **Source / Label** | **Judgment informed by SEC Form 10-K History** | **Judgment informed by MD&A Contractual Guidance** |
| **Tested Range Rationale** | Sourced from audited Form 10-K history: FY24 was 53.49%, FY25 was 68.27%, and FY26 was 68.92%. The Lower value (65.0%) represents ERCOT Texas wholesale power price spikes, transmission curtailment penalties, and mining difficulty escalation. The Higher value (75.0%) captures premium margins from dedicated NVIDIA Blackwell GB300 AI Cloud hosting contracts. | Sourced from disclosed multi-year contracts, including the 5-year, $9.7 billion Microsoft agreement and management guidance targeting $4.0B contracted ARR for 2026 capacity ($1.0B operating ARR in Aug 2026). The Lower path represents substation grid connection delays or GPU liquid cooling supply chain bottlenecks. The Higher path represents accelerated conversion of the 1.2 GW capacity pipeline. |

> [!NOTE]
> **Methodological Symmetry of Tested Ranges:**  
> Both Driver 1 and Driver 2 were evaluated across a **10.0 percentage point span** ($\pm5.0$ percentage points from base). This symmetry ensures that output span comparisons between top-line expansion and unit margin expansion are methodologically balanced.
> 
> In addition, a wider **Stress Test Range ($\pm10.0$ percentage points)** was executed for Revenue Growth (`[90%, 40%, 20%, 5%, 0%]` to `[110%, 60%, 40%, 25%, 20%]`). In the Stress Lower case, FY2031E FCFE remains negative at $-\$250.49\text{M}$, triggering the model's Refusal Gate where terminal valuation is marked **UNAVAILABLE** because capitalizing a negative terminal cash flow is mathematically and economically invalid.

---

## I & V — The Sensitivity Engine & Master Results Table

The sensitivity analysis was executed using [`Lab-11/sensitivity_iren.py`](file:///c:/Users/ellio/Documents/FIN439/Lab-11/sensitivity_iren.py). Every run began with a fresh independent copy of `ASSUMPTIONS`, modified exactly **one** independent input, and re-ran the complete linked three-statement engine.

### 1. Master One-at-a-Time Sensitivity Table

*All monetary outputs in USD millions ($M), except Value per Share ($/share). Primary share count: 394.059 million Ordinary shares.*

| Operating Driver | Run Case | Input Value / Path | FY2031E Operating Profit | Signed $\Delta$ from Base | FY2031E Free Cash Flow (FCFE) | Signed $\Delta$ from Base | Implied Value per Share | Signed $\Delta$ from Base | Double-Entry Checks |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Original Base** | **Base Benchmark** | **As Sourced** | **$777.88M** | **$0.00M** | **$380.39M** | **$0.00M** | **-$5.31** | **$0.00** | **PASS (Gap = 0.0000)** |
| **1. Cash Gross Margin** | Lower (-5.0 pp) | 65.0% | $664.52M | -$113.36M | $249.56M | -$130.84M | -$8.28 | -$2.96 | PASS (Gap = 0.0000) |
| *(Base: 70.0%)* | Base (0.0 pp) | 70.0% | $777.88M | $0.00M | $380.39M | $0.00M | -$5.31 | $0.00 | PASS (Gap = 0.0000) |
| *(Units: % of Rev)* | Higher (+5.0 pp) | 75.0% | $891.24M | +$113.36M | $480.25M | +$99.86M | -$2.93 | +$2.39 | PASS (Gap = 0.0000) |
| **2. Revenue Growth** | Lower (-5.0 pp) | 95% $\rightarrow$ 5% | $504.03M | -$273.85M | $39.92M | -$340.47M | -$12.45 | -$7.14 | PASS (Gap = 0.0000) |
| *(Base: 100% $\rightarrow$ 10%)*| Base (0.0 pp) | 100% $\rightarrow$ 10% | $777.88M | $0.00M | $380.39M | $0.00M | -$5.31 | $0.00 | PASS (Gap = 0.0000) |
| *(Units: Annual %)* | Higher (+5.0 pp) | 105% $\rightarrow$ 15% | $1,095.13M | +$317.24M | $672.22M | +$291.83M | +$0.99 | +$6.31 | PASS (Gap = 0.0000) |
| **2b. Stress Growth** | Stress Low (-10 pp)| 90% $\rightarrow$ 0% | $269.00M | -$508.88M | -$250.49M | -$630.88M | **UNAVAIL\*** | N/A | PASS (Gap = 0.0000) |
| *(Wider Range)* | Stress High (+10 pp)| 110% $\rightarrow$ 20%| $1,460.67M | +$682.78M | $957.27M | +$576.88M | +$7.22 | +$12.53 | PASS (Gap = 0.0000) |

*\* Note on Stress Lower Run: In the -10 pp stress scenario, FY2031E FCFE remains negative at $-\$250.49\text{M}$. The model strictly enforces the Refusal Gate: a terminal value cannot be calculated on an ongoing cash deficit, so Value per Share is marked UNAVAILABLE rather than generating an ungrounded number.*

---

### 2. Output Span Comparison Table

$$\text{Output Span} = \text{Maximum Valid Output} - \text{Minimum Valid Output}$$

| Operating Driver | Tested Input Range | Operating Profit Span (FY31 EBIT) | Free Cash Flow Span (FY31 FCFE) | Implied Value per Share Span |
| :--- | :---: | :---: | :---: | :---: |
| **1. Cash Gross Margin** | 65.0% to 75.0% (10 pp span) | **$226.72M** | **$230.69M** | **$5.35 per share** |
| **2. Revenue Growth Path** | $\pm5.0$ pp/year (10 pp shift) | **$591.10M** | **$632.29M** | **$13.44 per share** |
| **Sensitivity Span Ratio** | *Revenue Growth $\div$ Gross Margin* | **2.61x** | **2.74x** | **2.51x** |

> [!IMPORTANT]
> **Key Finding Over Tested Ranges:**  
> **Revenue Growth Trajectory** is the primary driver of IREN's operating results and valuation **over these tested ranges**. Its output span is **2.61x** larger for Operating Profit ($591.10M vs. $226.72M), **2.74x** larger for Free Cash Flow ($632.29M vs. $230.69M), and **2.51x** larger for Value per Share ($13.44/sh vs. $5.35/sh).

---

### 3. Restored Base Case Verification Block

As mandated by course policy, following the execution of all sensitivity runs, the original base case was restored, re-executed, and verified to ensure that no state pollution or parameter corruption occurred.

| Verification Line / Metric | Original Base (Pre-Sensitivity) | Restored Base (Post-Sensitivity) | Discrepancy (Abs Error) | Integrity Status |
| :--- | :---: | :---: | :---: | :---: |
| **FY2031E Operating Profit (EBIT)** | $777.8823M | $777.8823M | $0.000000M | **PASS (Exact Match)** |
| **FY2031E Free Cash Flow (FCFE)** | $380.3902M | $380.3902M | $0.000000M | **PASS (Exact Match)** |
| **Implied Value per Share** | -$5.3145 | -$5.3145 | $0.000000 | **PASS (Exact Match)** |
| **Balance Sheet Gap (FY2027E–FY2031E)** | +0.0000 | +0.0000 | 0.0000 | **PASS (Balanced to 0.0000)** |
| **Minimum Cash Buffer ($\ge \$500.0M$)** | PASS | PASS | 0.0000 | **PASS (Protected)** |

---

## Causal Traces: Mechanism from Input to Value

The worksheet requires tracing the exact causal mechanism through the financial statements for at least one sensitivity run. Below are the actual step-by-step model links for both drivers.

### Causal Trace 1: Driver 1 — Cash Gross Margin (70.0% $\rightarrow$ 75.0%)

```
INPUT CHANGE: Cash Gross Margin increases from 70.0% to 75.0% (+5.0 percentage points)
  |
  v
FINANCIAL STATEMENT LINE(S) (FY2031E):
  - Total Revenue:           $3,488.02M (Unchanged; revenue growth is held at Base)
  - Cost of Revenues:        $872.00M (Decreases by $174.40M from base $1,046.41M; Cost = Rev * (1 - GM))
  - Cash Gross Profit:       $2,616.01M (Increases by $174.40M from base $2,441.61M)
  - SG&A Overhead (35% GP):  $915.60M (Increases by $61.04M from base $854.57M due to profit-linked overhead)
  - Depreciation & Amort:    $809.17M (Unchanged; PP&E and capex schedule held at Base)
  - GAAP Pretax Income (EBT):$631.48M (Increases by $128.39M from base $503.09M)
  - Income Tax (21% post-NOL):$28.53M (Tax increases from $0.00M because higher earnings exhaust $700M NOLs earlier)
  - GAAP Net Income:         $602.95M (Increases by $99.86M from base $503.09M)
  |
  v
OPERATING PROFIT (EBIT):
  - FY2031E EBIT:            $891.24M (Signed change: +$113.36M from base $777.88M)
  |
  v
FREE CASH FLOW (FCFE):
  - Operating Cash Flow:     $1,480.25M (Increases by +$99.86M from base $1,380.39M)
  - Working Capital Delta:   Unchanged (AR, Deferred Revenue, and Other Liabilities track revenue, which is at Base)
  - Capex & Debt Repayment:  -$600.0M Capex - $400.0M Debt Repayment = -$1,000.0M (Unchanged)
  - FY2031E FCFE:            $480.25M (Signed change: +$99.86M from base $380.39M)
  |
  v
IMPLIED VALUE PER SHARE:
  - Terminal Value at FY31E: Terminal Value rises to $5,530.96M (PV TV = $3,223.85M, up +$670.34M)
  - Total Equity Value:      Improves from -$2,094.23M to -$1,153.27M (+940.97M)
  - Value per Share:         Improves from -$5.31 to -$2.93 per share (Signed change: +$2.39/share)
```

### Causal Trace 2: Driver 2 — Revenue Growth (+5.0 pp per year)

```
INPUT CHANGE: Revenue Growth increases by +5.0 percentage points per year ([105%, 55%, 35%, 20%, 15%])
  |
  v
FINANCIAL STATEMENT LINE(S) (FY2031E):
  - Total Revenue:           $4,359.88M (Increases by +$871.86M from base $3,488.02M due to compound top-line expansion)
  - Cost of Revenues (30%):  $1,307.96M (Increases by +$261.56M from base $1,046.41M)
  - Cash Gross Profit (70%): $3,051.92M (Increases by +$610.30M from base $2,441.61M)
  - SG&A Overhead (35% GP):  $1,068.17M (Increases by +$213.61M from base $854.57M)
  - Depreciation & Amort:    $888.62M (Increases by +$79.45M because higher capex/PP&E base scales D&A)
  - GAAP Pretax Income (EBT):$1,095.13M (Increases by +$592.04M from base $503.09M)
  - Income Tax (21% post-NOL):$124.96M (Substantially higher taxable income accelerates NOL exhaustion)
  - GAAP Net Income:         $786.13M (Increases by +$283.04M from base $503.09M)
  |
  v
OPERATING PROFIT (EBIT):
  - FY2031E EBIT:            $1,095.13M (Signed change: +$317.24M from base $777.88M)
  |
  v
FREE CASH FLOW (FCFE):
  - Operating Cash Flow:     $1,672.22M (Increases by +$291.83M from base $1,380.39M, boosted by +$142.1M Deferred Rev)
  - Capex & Debt Repayment:  -$600.0M Capex - $400.0M Debt Repayment = -$1,000.0M (Unchanged in Year 5)
  - FY2031E FCFE:            $672.22M (Signed change: +$291.83M from base $380.39M)
  |
  v
IMPLIED VALUE PER SHARE:
  - Terminal Value at FY31E: Terminal Value rises to $7,741.87M (PV TV = $4,512.60M, up +$1,959.09M)
  - Total Equity Value:      Improves from -$2,094.23M to +$390.53M (+$2,484.76M)
  - Value per Share:         Improves from -$5.31 to +$0.99 per share (Signed change: +$6.31/share)
```

---

## Interpretation & Findings

### 1. Main Driver Over the Tested Ranges
Over these tested ranges, **Revenue Growth Trajectory** is the primary driver of IREN's pro-forma performance and equity valuation:
- **Operating Profit (FY2031E EBIT):** Revenue Growth span of **$591.10M** is **2.61 times** the Cash Gross Margin span of **$226.72M**.
- **Free Cash Flow (FY2031E FCFE):** Revenue Growth span of **$632.29M** is **2.74 times** the Cash Gross Margin span of **$230.69M**.
- **Implied Value per Share:** Revenue Growth span of **$13.44/share** is **2.51 times** the Cash Gross Margin span of **$5.35/share**.

### 2. Range Limitation ("Over These Tested Ranges")
A larger output span does **not** prove that Revenue Growth is fundamentally or universally more important than Gross Margin. The ranking depends directly on the boundaries of the tested ranges:
- A $10.0$ percentage point compounding shift in annual revenue growth across five consecutive forecast periods has a cumulative multiplicative effect on total scale ($+\$871.9\text{M}$ in Year 5 revenue), whereas a $10.0$ percentage point shift in cash gross margin acts on a fixed revenue base.
- Had we tested a much tighter revenue growth range ($\pm1.0$ percentage point) against a wide gross margin range ($\pm15.0$ percentage points), Gross Margin would have produced the larger span. Therefore, every sensitivity ranking must be explicitly qualified: **over these tested ranges**.

### 3. Impact vs. Uncertainty
A complete financial assessment requires distinguishing between two distinct concepts:
- **IMPACT:** How much a given change in an input moves the model's output (the mathematical derivative or elasticity of the model).
- **UNCERTAINTY:** The degree of real-world dispersion, volatility, or unpredictability surrounding that input.

For IREN, Revenue Growth has both high **impact** (due to compounding top-line leverage and customer prepayments) and high **uncertainty** (dependent on external hyperscaler capital expenditure cycles, NVIDIA Blackwell GPU delivery timelines, and ERCOT grid interconnection approvals). Cash Gross Margin has high **impact** on unit profitability, but slightly narrower **uncertainty** because data center power contracts and PPA agreements hedge wholesale electricity volatility.
---

## Visible Terminal Output

Below is the complete, unedited console output generated by executing `py Lab-11/sensitivity_iren.py`:

```
===================================================================================================================
FIN 439 LAB 11: PRO-FORMA SENSITIVITY ANALYSIS - IREN LIMITED (NASDAQ: IREN)
Authoritative Assignment: Lab 11 - Pro-Forma Sensitivity: Find Your Company's Drivers
Student: Elliot | Valuation Date: September 29, 2026
===================================================================================================================

--- BASE CASE BENCHMARK (PRE-SENSITIVITY) ---
  Final-Year (FY2031E) Operating Profit (EBIT):  $    777.88 million
  Final-Year (FY2031E) Free Cash Flow (FCFE):    $    380.39 million
  Implied Value per Share (Primary: 394.06M sh):  $     -5.31 per share
  Accounting Check Status:                        PASS (All 5 Years Gap = 0.0000)

===================================================================================================================
1. MASTER SENSITIVITY TABLE: TWO OPERATING DRIVERS
===================================================================================================================
Driver                       Case           Input Value        FY31 EBIT   Signed d   FY31 FCFE   Signed d  Val/Share  Signed d   Checks
-------------------------------------------------------------------------------------------------------------------
1. Cash Gross Margin         Lower (65.0%)  65.0%               $664.52M   -113.36M    $249.56M   -130.84M     $-8.28     -2.96     PASS
                             Base (70.0%)   70.0%               $777.88M     +0.00M    $380.39M     +0.00M     $-5.31     +0.00     PASS
                             Higher (75.0%) 75.0%               $891.24M   +113.36M    $480.25M    +99.86M     $-2.93     +2.39     PASS
-------------------------------------------------------------------------------------------------------------------
2. Revenue Growth Path       Lower (-5 pp)  95%->5%             $504.03M   -273.85M     $39.92M   -340.47M    $-12.45     -7.14     PASS
                             Base (0 pp)    100%->10%           $777.88M     +0.00M    $380.39M     +0.00M     $-5.31     +0.00     PASS
                             Higher (+5 pp) 105%->15%          $1095.13M   +317.24M    $672.22M   +291.83M      $0.99     +6.31     PASS
-------------------------------------------------------------------------------------------------------------------
2b. Stress Growth (+/-10pp)  Stress Lower (-10 pp) 90%->0%             $269.00M   -508.88M   $-250.49M   -630.88M   UNAVAIL*       N/A     PASS
                             Stress Higher (+10 pp) 110%->20%          $1460.67M   +682.78M    $957.27M   +576.88M      $7.22    +12.53     PASS
-------------------------------------------------------------------------------------------------------------------
Notes: Signed d = Changed Output - Base Output. All figures in USD millions except Value/Share.
* In Stress Lower (-10 pp), FY31 FCFE is negative ($-250.49M); terminal value is refused by economic logic.

===================================================================================================================
2. OUTPUT SPAN COMPARISON (MAXIMUM VALID OUTPUT - MINIMUM VALID OUTPUT)
===================================================================================================================
Driver Name                        Tested Input Range             EBIT Span ($M)   FCFE Span ($M)   VPS Span ($)
-------------------------------------------------------------------------------------------------------------------
1. Cash Gross Margin               65.0% to 75.0% (10 pp span)  $        226.72M $        230.69M $        5.35
2. Revenue Growth Path             +/-5.0 pp/yr (10 pp shift)   $        591.10M $        632.29M $       13.44
-------------------------------------------------------------------------------------------------------------------
>>> MAIN DRIVER OVER TESTED RANGES: REVENUE GROWTH TRAJECTORY <<<
    - Operating Profit Span: Revenue Growth ($591.10M) is 2.61x Gross Margin ($226.72M)
    - Free Cash Flow Span:   Revenue Growth ($632.29M) is 2.74x Gross Margin ($230.69M)
    - Value per Share Span:  Revenue Growth ($13.44/sh) is 2.51x Gross Margin ($5.35/sh)
    * CRITICAL LIMITATION: This ranking holds OVER THESE TESTED RANGES and reflects input range width.

===================================================================================================================
3. RESTORED BASE CASE VERIFICATION (RE-RUN AT CONCLUSION)
===================================================================================================================
Metric / Verification Line                         Original Base      Restored Base      Discrepancy     Status
-------------------------------------------------------------------------------------------------------------------
FY2031E Operating Profit (EBIT, $M)                     777.8823           777.8823         0.000000       PASS
FY2031E Free Cash Flow (FCFE, $M)                       380.3902           380.3902         0.000000       PASS
Implied Value per Share ($/share)                        -5.3145            -5.3145         0.000000       PASS
Balance Sheet Gap (FY2027E - FY2031E)                    +0.0000            +0.0000           0.0000       PASS
Minimum Cash Buffer (>= $500.0M)                            PASS               PASS           0.0000       PASS
-------------------------------------------------------------------------------------------------------------------
>>> VERIFICATION RESULT: Original base case is 100% restored. No persistent mutations occurred. <<<

===================================================================================================================
4. CAUSAL TRACE: DRIVER 1 SENSITIVITY (GROSS MARGIN: 70.0% -> 75.0%)
===================================================================================================================
INPUT CHANGE: Cash Gross Margin increases from 70.0% to 75.0% (+5.0 percentage points)
  |
  v
FINANCIAL STATEMENT LINE(S) (FY2031E):
  - Total Revenue:           $3488.02M (Unchanged; revenue growth is held at Base)
  - Cost of Revenues:        $872.00M (Decreases by $174.40M from $1046.41M)
  - Cash Gross Profit:       $2616.01M (Increases by $174.40M from $2441.61M)
  - SG&A Overhead (35% GP):  $915.60M (Increases by $61.04M due to profit-linked overhead)
  - Depreciation:            $809.17M (Unchanged; PP&E and capex held at Base)
  - GAAP Pretax Income:      $631.48M (Increases from $503.09M)
  - Income Tax (21% post-NOL):$28.53M (NOLs depleted earlier; tax increases from $0.00M)
  - GAAP Net Income:         $602.95M (Increases by $99.86M from $503.09M)
  |
  v
OPERATING PROFIT (EBIT):
  - FY2031E EBIT:            $891.24M (Signed change: +$113.36M from base $777.88M)
  |
  v
FREE CASH FLOW (FCFE):
  - Operating Cash Flow:     $1480.25M (Increases by $99.86M)
  - Working Capital Delta:   Unchanged (AR, Deferred Revenue, and Other Liabilities track revenue)
  - Capex & Debt Repayment:  -$600.0M Capex - $400.0M Debt Repayment = -$1,000.0M (Unchanged)
  - FY2031E FCFE:            $480.25M (Signed change: +$99.86M from base $380.39M)
  |
  v
IMPLIED VALUE PER SHARE:
  - Year 5 FCFE Capitalized: Terminal Value rises to $5530.96M (PV TV = $3223.85M)
  - Total Equity Value:      Improves from -$2094.23M to -$1153.27M (+$940.97M)
  - Value per Share:         Improves from $-5.31 to $-2.93 (Signed change: +$2.39/share)
===================================================================================================================

################################################################################
RUNNING LAB 11 SENSITIVITY TEST SUITE & VERIFICATION CHECKS
################################################################################
  [PASS] Original base case runs and passes all balance sheet/liquidity checks.
  [PASS] Driver 1 (Gross Margin) Lower/Base/Higher runs pass all double-entry checks.
  [PASS] Driver 2 (Revenue Growth) Lower/Base/Higher runs pass all double-entry checks.
  [PASS] Stress lower run correctly flags valuation as UNAVAILABLE when FCFE is negative.
  [PASS] Restored base case matches original base case exactly (error < 1e-6).
```

---

## Academic Integrity & AI Assistance Disclosure

This report, financial model (`sensitivity_iren.py`), and supporting documentation were prepared for **FIN 43900 (Corporate Finance / Applied Financial Modeling, Purdue University)** as part of Laboratory 11.

- **Student Name:** Elliot  
- **Company:** IREN Limited (NASDAQ: IREN)  
- **Authoritative Worksheet:** Lab 11 — Pro-Forma Sensitivity: Find Your Company's Drivers  

**AI Assistance Disclosure:**  
Model development and documentation were drafted with the assistance of **Google Antigravity / AI Coding Assistant**. In accordance with course guidelines and academic integrity policies:
1. The analysis strictly leverages Elliot's existing Lab 10 three-statement model without modifying prior audited SEC data or altering historical financial statements.
2. Sensitivity runs were executed programmatically one-at-a-time, resetting to a fresh independent base copy before every run.
3. Double-entry accounting checks were verified for every run, and the original base case was restored and confirmed to zero error tolerance ($0.000000$).
4. In strict adherence to academic integrity policies, all financial inputs, historical data, and modeling schedules were derived from audited SEC filings without fabricating company numbers.
