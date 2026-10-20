# Validation and AI Use Record — Project 1 (IREN Limited)

**Student Name:** Elliot  
**Course:** FIN 43900 (Corporate Finance / Applied Financial Modeling, Daniels School of Business, Purdue University)  
**Target Company:** IREN Limited (NASDAQ: IREN)  
**Valuation / Audit As-of Date:** October 8, 2026  
**Baseline Filing Date:** August 27, 2026 (FY2026 Form 10-K, period ended June 30, 2026)  
**Prior Baseline Date:** September 3, 2026 (Edition A Research Report, commit `2710819`)  
**Current Committee Decision:** WATCH / DEFER at **$12.12 Implied Equity Value per Share** (Primary FCFF Enterprise DCF; Range: **$4.06 to $19.25**; Secondary FCFE Comparison: **-$5.31**)  

---

## 1. Decision, Version, and As-of Boundary

- **Target / Security:** IREN Limited (Ordinary Shares, NASDAQ: IREN).
- **Intended User:** Buy-Side Investment Committee (AI Task Force embedded in corporate finance/analyst team).
- **Recommendation:** **WATCH / DEFER**. Do not initiate a buy position at current market prices ($41.65 on 2026-09-03; $45.73 on 2026-09-24). The company is undergoing a multi-billion-dollar infrastructure transition from Bitcoin mining to AI Cloud data centers. While top-line contracted ARR has reached $4.0B ($1.0B operating ARR) and Horizon 1 (50 MW) was accepted by Microsoft, actual FY2026 GAAP results generated a $(702.6)M net loss, $(1,046.7)M operating loss, and cash capex of $4,333.1M. Modeled 5-year pro-forma FCFF DCF produces an intrinsic equity value of **$12.12 per share** (primary 394.059M basic ordinary shares; range: **$4.06 to $19.25**), while direct FCFE produces **-$5.31 per share** prior to crediting the starting cash reserve. We defer initiation until recognized GAAP operating cash flows turn positive and Horizons 2–4 customer acceptance is achieved.
- **Repository Commit / Tag:** Main branch, commit `a1acf078dce766509dc296cecc0f48b3eb5c5623` (and subsequent audit updates).
- **Audit Run Timestamp:** 2026-10-08 16:15 EDT (re-audited 2026-10-19).
- **Source Cutoffs:** Form 10-K filed August 27, 2026; Press Release dated August 13, 2026 (Microsoft Horizon 1 acceptance); Market prices as of September 3, 2026 ($41.65) and September 24, 2026 ($45.73).
- **Environment:** Windows 11, Python 3.13.15 (accessed via `py` launcher), pandas 3.0.6, numpy 2.5.3, streamlit 1.65.0, reportlab 5.0.1.

---

## 2. Data and Convention Ledger

| Material Input | Sourced Value | SEC Filing Source & Locator | Definition / Units | Transformation / Exclusion | Risk & Handling |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FY2026 Total Revenue** | $707,007 thousand | FY2026 10-K, Item 8, Cons. Stmt. of Operations, p. F-7 | GAAP recognized revenue ($M) | Direct filing input. Excludes unearned ARR. | Low. Reconciles to Note 4 segment revenue. |
| **FY2026 AI Cloud Revenue** | $128,795 thousand | FY2026 10-K, Item 8, Note 4, p. F-15 | AI compute revenue ($M) | Direct filing input ($16.4M in FY25, $3.1M in FY24). | Low. Shows rapid 686% YoY ramp. |
| **FY2026 Bitcoin Revenue** | $578,212 thousand | FY2026 10-K, Item 8, Note 4, p. F-15 | Mining revenue ($M) | Direct filing input. Daily fiat liquidation. | Medium. Exposed to BTC spot price swings. |
| **Cash Cost of Revenue (Power)** | $219,706 thousand | FY2026 10-K, Item 8, Cons. Stmt. of Operations, p. F-7 | Operating costs excl. D&A ($M) | Reconciles to 68.92% cash gross margin. | Medium. Exposed to ERCOT/PJM wholesale power spikes. |
| **Depreciation & Amortization** | $417,729 thousand | FY2026 10-K, Item 8, Cons. Stmt. of Cash Flows, p. F-9 | Non-cash D&A ($M) | Straight-line D&A on PP&E (5-yr GPUs, 20-25 yr sites). | High. Massive near-term drag on GAAP earnings. |
| **Asset Impairments** | $638,805 thousand | FY2026 10-K, Item 8, Cons. Stmt. of Operations, p. F-7 | Non-cash write-downs ($M) | Normalized to $0 in pro-forma forecast (one-time). | High. Written-down Bitcoin ASICs during AI transition. |
| **Operating Loss (EBIT)** | $(1,046,714) thousand | FY2026 10-K, Item 8, Cons. Stmt. of Operations, p. F-7 | GAAP operating loss ($M) | Direct filing input. | High. Shows current operational burn before AI scale. |
| **GAAP Net Loss** | $(702,621) thousand | FY2026 10-K, Item 8, Cons. Stmt. of Operations, p. F-7 | GAAP net loss ($M) | Direct filing input. Checked against Note 27. | High. Reflects impairment + D&A + SG&A scaling. |
| **Cash & Cash Equivalents** | $5,895,591 thousand | FY2026 10-K, Item 8, Cons. Balance Sheet, p. F-6 | Balance sheet cash ($M) | Direct filing input. Checked against Note 10. | Low. Substantial balance from equity + note proceeds. |
| **Customer Prepayments (Def. Rev)** | $1,842,546 thousand | FY2026 10-K, Item 8, Cons. Balance Sheet, p. F-6 | Deferred revenue liabilities ($M) | $46.5M current + $1,796.1M non-current (Microsoft prepay). | Critical. Non-dilutive working capital liquidity engine. |
| **Total Debt & Convertible Notes** | $7,836,740 thousand | FY2026 10-K, Item 8, Note 22 & 23, pp. F-43–F-47 | Carrying debt & notes ($M) | Includes $6.30B convertible notes + term debt. | High. Future interest burden ($59.3M in FY26) + dilution. |
| **Actual Cash Capex (PP&E + GPUs)** | $4,333,143 thousand | FY2026 10-K, Item 8, Cons. Stmt. of Cash Flows, p. F-9 | Total cash investment ($M) | $2,998.0M PP&E additions + $1,335.1M computer hardware. | Critical. Data aggregators report only $2,998M, understating capex by 31%! |
| **Share Count (Cover Page)** | 394.059 million | FY2026 10-K Cover Page (August 14, 2026) | Basic ordinary shares (M) | Primary share basis for per-share valuation. | High. Reconciles 3 distinct counts in SEC filings. |
| **Share Count (Balance Sheet)** | 380.194 million | FY2026 10-K Cons. Balance Sheet (June 30, 2026) | Ending balance sheet count (M) | Secondary sensitivity basis. | High. Differs by 13.86M shares due to July/Aug equity issuance. |
| **Share Count (Diluted Wtd Avg)** | 316.123 million | FY2026 10-K Cons. Stmt. of Operations, p. F-7 | Diluted weighted-average (M) | Used in Week 3 dcf.py; understates current share dilution. | High. Weighted average over entire FY26 misses rapid expansion. |

---

## 3. Validation Register

| Claim / Output | Failure Mode | Test and Expected Result / Direction | Actual Result | Disposition | Evidence Location |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cold-Run Setup & Environment** | Windows Store execution alias intercepts `python` | Cold terminal execution of `python project_audit.py` fails if python alias is not resolved. | `python` returned exit code 1 ("Python was not found..."). `py` launcher succeeded immediately. | **RESOLVED**: Updated README with explicit `py` and direct python execution instructions. | Cold-run log below; `README.md` |
| **Synthetic Known-Answer Check** | Model logic corruption on reference case | Run Lab 09 ABG benchmark engine; expect implied value per share of exactly $291.75 and Gap = 0.0. | Implied VPS = $291.75; Gap = 0.0000 across all 5 years. | **PASS (ACCEPT)**: Reconciled to professor benchmark to the exact cent. | `Lab-09/proforma.py` |
| **Double-Entry Articulation** | Balance sheet out of balance / circular cash break | Assets = Liabilities + Equity (Gap == 0.0000) for every forecast year. | FY27E to FY31E all balance with Gap = 0.0000; cash ties exactly to balance sheet ending cash. | **PASS (ACCEPT)**: Five-year statements fully articulate. | `Lab-10/proforma_iren.py`; `visible_output.json` |
| **Refusal Gate Check** | Silent calculation of corrupt inputs | Intentionally add $500.0M artificial discrepancy to FY28E cash; expect script refusal and loud error. | Script halted execution immediately: `MODEL REFUSAL: Balance sheet check failed in FY2028E! Gap = $+500.0000M`. | **PASS (ACCEPT)**: Model refuses invalid accounting state. | `Lab-10/proforma_iren.py` [Test 2] |
| **Stress Lower Refusal Check** | Gordon Growth applied to negative perpetual terminal cash flow | Run -10 pp stress on revenue growth; FY31E FCFE turns negative (-$250.49M). | Terminal value refused: `UNAVAIL*` flagged. Economic logic strictly preserved. | **PASS (ACCEPT)**: Prevents economic absurdity of capitalizing negative cash flow. | `Lab-11/sensitivity_iren.py` [Test 2b] |
| **Independent Capex Source Check** | Aggregator capex undercounting | Compare Yahoo/Bloomberg Capex ($2,998M) against Form 10-K Cash Flow Statement. | Form 10-K reveals additional $1,335.1M in "Payments for computer hardware". Total capex is $4,333.1M. | **PASS (ACCEPT)**: Overruled aggregator data; used audited cash flow statement. | `Lab-10/lab10.md` Section R.2 |
| **DCF Compounding Bug in Week 3 Engine** | Compounding negative starting FCFF | Applying positive growth rates `[50%, 35%, 20%]` to `STARTING_FCFF = -2191.19M` expands deficit to -$6.3B in Year 5. | Modeled share price collapsed to -$196.34/share; reverse DCF bisection broke. | **DIAGNOSED & QUALIFIED**: Preserved original failure in `Project-1/dcf.py`; superseded by 3-statement pro-forma. | `Project-1/dcf.py`; Section 4 below |
| **FCFF Valuation & Bridge** | Disconnected DCF vs. pro-forma statements | Operating FCFF derived dynamically from pro-forma income statement, D&A, and capex with Enterprise-to-Equity Bridge. | Base FCFF DCF yields **$12.12/sh** (EV $6,715.33M + Cash $5,895.59M - Debt $7,836.74M = Equity $4,774.18M). | **PASS (ACCEPT)**: Reconciled with FCFE (-$5.31/sh); both affirm WATCH-DEFER. | `run_analysis.py`; `visible_output.json` |
| **One-at-a-time Sensitivity Monotonicity** | Non-monotonic directional output | Increasing Gross Margin from 65% to 75% must strictly increase EBIT, cash flows, and Value per Share. | FCFF VPS moves monotonically from $8.96 to $12.12 to $14.61 (span: $5.65/sh). FCFE VPS moves from -$8.28 to -$5.31 to -$2.93. | **PASS (ACCEPT)**: Strict monotonic behavior verified across both valuation metrics. | `run_analysis.py`; `Lab-11/sensitivity_iren.py` |

---

## 4. Documented Changed-Input Sensitivity Experiments & Directional Verification

> **Historical Documentation Status:**  
> The repository commit history preserves the actual Python sensitivity scripts, model executions, and output logs (`3125ff9`, `0644c82`). An isolated, timestamped precommit record created with AI disabled prior to execution was not independently maintained during initial lab work. The table below documents the sensitivity experiments actually performed during the lab sequence, the directional hypotheses tested during model development, and the preserved execution outputs verified against git history.

### Documented Hypotheses and Sensitivity Experiments

| Tested Parameter / Commit | Material Input | Old → New Value / Units | Hypothesized Directional Effect | Hypothesized Committee Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Lab 11 (`3125ff9`)** | Cash Gross Margin (`gross_margin`) | 70.0% → 75.0% (+5.0 percentage points) | FY31E EBIT, cash flows, and Implied VPS must increase monotonically; valuation deficit must shrink. | Margin expansion improves operating economics, but multi-billion capex burden keeps equity value constrained; recommendation remains WATCH-DEFER. |
| **Lab 11 (`3125ff9`)** | Revenue Growth Path (`revenue_growth`) | Base path `[100%, 50%, 30%, 15%, 10%]` → Higher path `[105%, 55%, 35%, 25%, 15%]` (+5 pp/yr) | FY31E Revenue, EBIT, and cash flows must scale sharply; VPS must increase substantially. | Top-line revenue reaching ~$4.2B expands FCFF toward ~$19/sh and FCFE crosses slightly positive; however, execution risk warrants maintaining WATCH-DEFER. |
| **Lab 12 (`0644c82`)** | Single-Year FY31E Revenue Growth | 10.0% → 11.0% (+1.0 percentage point in FY31 only) | FY31E Revenue moves +$31.71M; FY31E EBIT moves +$14.43M; VPS moves +$0.39/sh. | Minimal impact on overall 5-year present value; demonstrates that single-year terminal growth sensitivity is secondary to explicit capex timing. |

### Preserved Execution Results

| Tested Sensitivity & Model Output | Actual Committee Decision | Directional Outcome & Verification | Financial Rationale for Maintaining Recommendation | Evidence Path |
| :--- | :--- | :--- | :--- | :--- |
| **Gross Margin Test (70% → 75%):**<br>FCFE VPS: -$5.31 → -$2.93 (+$2.39/sh)<br>FCFF VPS: $12.12 → $14.61 (+$2.49/sh) | Recommendation unchanged: **WATCH-DEFER**. | **Monotonic Increase Verified**; valuation improved directionally across both metrics. | Decision did not change because a 5 pp power cost savings cannot offset $5.8B of cumulative debt service and $6.3B in capital commitments. | `Lab-11/sensitivity_iren.py`<br>`run_analysis.py`<br>`visible_output.json` |
| **Revenue Growth Path Test (+5 pp/yr):**<br>FCFE VPS: -$5.31 → +$0.99 (+$6.31/sh)<br>FCFF VPS: $12.12 → $19.25 (+$7.13/sh) | Recommendation unchanged: **WATCH-DEFER**. | **Monotonic Scaling Verified**; FCFE crossed above zero and FCFF reached $19.25. | Decision did not change because even $19.25 is still ~58% below market price ($45.73), and aggressive +5 pp compounding assumes flawless multi-gigawatt energization without supply chain disruption. | `Lab-11/sensitivity_iren.py`<br>`run_analysis.py`<br>`visible_output.json` |
| **FY31 Single-Year Test (10% → 11%):**<br>FCFE Base VPS: -$5.3145<br>FCFE New VPS: -$4.9213<br>(+$0.3933/sh signed change) | Recommendation unchanged: **WATCH-DEFER**. | **Arithmetic Impact Verified** to four decimal places. | Confirmed that single-year terminal revenue sensitivity is secondary to explicit capex cycle. Action remains WATCH-DEFER. | `Lab-12/lab12_sensitivity.py`<br>`Lab-12/lab12.md` Section 3.2 |

---

## 5. Named AI-Use Register

| Tool / Assistant Surface | Date / Phase | Material Development Task | Output / Suggestion Considered | Independent Human Check | Action Taken (Accept / Modify / Reject) | Effect on Valuation & Decision |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Generative AI Chat Assistant** | 2026-09-03 (Lab 04) | Initial research report structure and SEC disclosure summary. | Suggested including $4.0B contracted ARR in revenue forecast. | Manually verified Item 7 MD&A; confirmed ARR is non-GAAP and unearned commercial backlog. | **QUALIFIED & MODIFIED**: Excluded ARR from GAAP revenue; retained only recognized $707.0M. | Grounded baseline in audited reality; supported initial WATCH-DEFER. |
| **Antigravity Coding Assistant** | 2026-09-24 (Lab 10) | Scaffolding 3-statement pro-forma balance sheet logic in Python. | Proposed standard working capital formula referencing physical inventory. | Traced Form 10-K Balance Sheet (p. F-6); verified IREN carries **$0 inventory**. | **REJECTED**: Locked inventory at $0.0M; replaced with Customer Prepayments / Deferred Revenue. | Model accurately captures IREN's unique digital compute working capital mechanics. |
| **Antigravity Coding Assistant** | 2026-09-29 (Lab 11) | One-at-a-time sensitivity loop architecture. | Proposed running parameter sweeps on simplified unarticulated FCFE cash flow schedule. | Verified against course rubric requiring full 3-statement balance sheet articulation across every test. | **MODIFIED**: Rewrote loop to execute complete 3-statement rebalancing for every parameter step. | Ensured double-entry accounting integrity holds in every sensitivity test (Gap = 0.0000). |
| **Antigravity Coding Assistant** | 2026-10-08 (Week 7) | Automated course audit checker and environment diagnostic. | Flagged Windows execution alias failure and CSV quoting syntax error in manifest. | Verified `py` launcher execution and pandas CSV parser behavior in terminal. | **ACCEPTED**: Added `README.md` setup commands and regenerated valid 12-row manifest. | Passed mechanical audit; established verified cold-run reproducibility. |

---

## 6. Cold-Run Test Log (Fresh Environment README Protocol)

- **Test Date & Time:** 2026-10-08 16:12 EDT (re-verified 2026-10-19).
- **Protocol:** Executed in a fresh PowerShell terminal following only repository setup instructions.
- **Commands Executed:**
  ```powershell
  py -m pip install -r requirements.txt
  py run_analysis.py
  py project_audit.py project-submission-manifest-template.csv
  ```
- **First Failure Recorded:**
  - *Trigger:* Running `python project_audit.py project-submission-manifest-template.csv` directly in standard PowerShell.
  - *Error Output:* `Python was not found; run without arguments to install from the Microsoft Store, or disable this shortcut from Settings > Apps > Advanced app settings > App execution aliases.`
  - *Elapsed Time to Failure:* **4.2 seconds**.
  - *Root Cause:* Windows 11 default `python.exe` alias intercepts commands when Python is installed in a custom directory.
  - *Resolution:* Specified `py` (Python Launcher for Windows) in `README.md` and verification scripts.
- **Second Failure Recorded:**
  - *Trigger:* Running `project_audit.py` on draft manifest CSV.
  - *Error Output:* `pandas.errors.ParserError: Error tokenizing data. C error: Expected 9 fields in line 4, saw 11`
  - *Elapsed Time to Failure:* **2.1 seconds**.
  - *Root Cause:* Unquoted commas in the `notes` column of line 4.
  - *Resolution:* Regenerated `project-submission-manifest-template.csv` using Python `csv` writer with standard quoting.
- **Final Cold-Run Result:**
  - `py run_analysis.py` executed in **1.8 seconds**, fully balanced all 5 years (Gap = 0.0000), and successfully wrote `visible_output.json`.
  - `py project_audit.py project-submission-manifest-template.csv` executed in **1.2 seconds**, identifying exactly the 6 pending video/transcript rows without crash.
  - **Expected Output Reproduced:** **YES**.

---

## 7. Limitations, Monitoring, and Kill / Escalation Rules

### Observable Monitoring Triggers
1. **Horizon Delivery & Customer Acceptance:** Monitor SEC filings and press releases for formal delivery and acceptance of Horizons 2, 3, and 4 (targeting Q4 2026).
2. **Gross Power Margin Stability:** Monitor quarterly Cost of Revenue to confirm that power costs remain at or below 30–35% of revenue (cash gross margin ≥ 65%).
3. **Operating Cash Flow Inflection:** Re-evaluate recommendation if quarterly Cash from Operations before changes in customer prepayments turns sustainably positive (> $100M/quarter).

### Kill / Refusal Conditions
1. **Balance Sheet Disarticulation:** Reject the valuation model immediately if total assets do not equal total liabilities plus equity (Gap > $0.01M) in any forecast year.
2. **Liquidity Insolvency:** Refuse model outputs if ending cash drops below the mandatory $500.0M liquidity buffer without an authorized credit facility draw.
3. **Negative Terminal Cash Flow Gordon Capitalization:** Refuse terminal value calculation if Year 5 FCFE is negative, preventing economically meaningless capitalization.
