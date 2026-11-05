# FIN 439 Lab 19 — Legend Panel

**Course:** FIN 43900 (Applied Financial Modeling & Corporate Valuation, Purdue University)  
**Student:** Elliot (one "t")  
**Repository:** `river313/IREN-research`  
**Folder:** `Lab-19/`  
**Files:** [`legend_sec.py`](legend_sec.py) | [`app.py`](app.py) | [`run_tests.py`](run_tests.py) | [`requirements.txt`](requirements.txt) | [`memos/`](memos/) | [`skills/`](skills/)  
**Status:** Complete — All 5 Test Suites Passed, Empirically Reconciled Against SEC EDGAR 10-K Filings

---

## 1. Objective & Architectural Philosophy

The objective of FIN 439 Lab 19 is to extend the Warren Buffett skill from Lab 18 into a multi-persona **Legend Investor Panel** incorporating **Benjamin Graham** and **Dr. Michael Burry**. All three investor skills evaluate the exact same audited SEC EDGAR 10-K financial disclosures, using Python for deterministic financial computations and AI for qualitative investment interpretation.

The central rule of this laboratory is:
> **Python computes every financial number from SEC filings. AI interprets those numbers using each legend investor's philosophy.**  
> Do not invent, estimate, or fabricate financial figures, validation results, partner dialogues, or student opinions.

### The Three Investor Frameworks
1. **Warren Buffett (Franchise Quality & Compounding Moat):** Evaluates companies as an owner purchasing an entire business. Enforces high return on capital ($\text{ROE} \ge 15.0\%$), positive owner earnings ($\text{OCF} - \text{CapEx} > 0$), and multi-year owner cash flow expansion ($\text{OE}_{\text{FY5}} > \text{OE}_{\text{FY1}}$).
2. **Benjamin Graham (Balance Sheet Margin of Safety & Solvency):** Enforces classical defensive value conservatism: adequate working capital cushion ($\text{Current Ratio} \ge 2.0$ in latest year), uninterrupted earnings stability ($\text{Net Income} > 0$ every year), and purchasing-power earnings growth ($\text{Net Income}_{\text{FY5}} > \text{Net Income}_{\text{FY1}}$).
3. **Dr. Michael Burry (Forensic Cash Quality & Debt Leverage Limits):** Scrutinizes cash flow accounting integrity, rejecting paper profits unbacked by cash receipts ($\text{OCF} \ge \text{Net Income}$ across all 5 years) and capping financial leverage to prevent insolvency distress during credit contractions ($\text{Total Liabilities} \le 2.0 \times \text{Stockholders' Equity}$ in latest year).

---

## 2. SEC EDGAR Data Architecture & XBRL Mapping

All data is retrieved dynamically via the official SEC EDGAR API using an SEC-compliant User-Agent identifying Elliot:
* **Company Directory:** `https://www.sec.gov/files/company_tickers.json`
* **Company Facts:** `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json`
* **User-Agent:** `Elliot river313@purdue.edu` (configurable via `SEC_EDGAR_EMAIL` or application sidebar)

### XBRL Taxonomy Mapping
Metric | Primary XBRL Tag | Fallback Tag | Type
:--- | :--- | :--- | :---
**Revenue** | `RevenueFromContractWithCustomerExcludingAssessedTax` | `Revenues` | Duration (1 Year)
**Net Income** | `NetIncomeLoss` | — | Duration (1 Year)
**Operating Cash Flow** | `NetCashProvidedByUsedInOperatingActivities` | — | Duration (1 Year)
**CapEx (Capital Spending)** | `PaymentsToAcquirePropertyPlantAndEquipment` | `PaymentsToAcquireProductiveAssets` | Duration (1 Year)
**Stockholders' Equity** | `StockholdersEquity` | — | Instant (Year-End)
**Total Liabilities** | `Liabilities` | — | Instant (Year-End)
**Current Assets** | `AssetsCurrent` | — | Instant (Year-End)
**Current Liabilities** | `LiabilitiesCurrent` | — | Instant (Year-End)

### Strict Accounting Filters
* **10-K Filings Only:** Form 10-Q and 8-K disclosures are excluded (`form == '10-K'`).
* **Annual Duration Constraints:** `350 <= (end - start).days <= 375` ensures full fiscal years while accommodating 52/53-week retail calendars.
* **Latest Filing Precedence:** If a metric for a given period end is reported across multiple filings, the filing with the latest `filed` date takes precedence.
* **Five Fiscal Years:** Historical observations are sorted chronologically by fiscal-year-end date (`end`), selecting the 5 most recent years.
* **Honest Gaps:** Missing tags display `"not found"`. Missing inputs cause dependent checks to evaluate as `"NOT KNOWN"`. Never estimate or interpolate.

---

## 3. Costco Wholesale (COST) Known Answer Reconciliation

### Audited Ratios vs. Professor's Reference Table
The two new ratios (Current Ratio and Liabilities $\div$ Equity) and the five base metrics were computed for Costco Wholesale (COST) across fiscal years 2022–2026:

| FY End | 2022-08-28 | 2023-09-03 | 2024-09-01 | 2025-08-31 | 2026-08-30 | Status |
| :--- | ---: | ---: | ---: | ---: | ---: | :---: |
| **Current Ratio** | **1.02** | **1.07** | **0.97** | **1.03** | **1.06** | **MATCH** |
| **Liabilities $\div$ Equity** | **2.11** | **1.75** | **1.96** | **1.64** | **1.49** | **MATCH** |
| **ROE** | 28.3% | 25.1% | 31.2% | 27.8% | 25.8% | **MATCH** |
| **Owner Earnings ($M)** | $3,501 | $6,745 | $6,629 | $7,837 | $9,382 | **MATCH** |

### The Panel on COST
| Investor | Check Description | Hurdle | COST Value | Result |
| :--- | :--- | :--- | :--- | :---: |
| **Buffett** | Check 1: ROE $\ge 15\%$ every year | $\ge 15.0\%$ all 5 yrs | 25.1% – 31.2% | **`PASS`** |
| **Buffett** | Check 2: Owner earnings positive every year | $> 0$ all 5 yrs | $3,501M – $9,382M | **`PASS`** |
| **Buffett** | Check 3: Owner earnings grew (FY5 $>$ FY1) | $\text{OE}_{\text{FY5}} > \text{OE}_{\text{FY1}}$ | +$5,881M (+168.0%) | **`PASS`** |
| **Graham** | Check 1: Current ratio $\ge 2.0$ (latest year) | $\ge 2.0$ | **1.06** | **`FAIL`** |
| **Graham** | Check 2: Net income positive every year | $> 0$ all 5 yrs | $5,844M – $9,226M | **`PASS`** |
| **Graham** | Check 3: Net income grew (FY5 $>$ FY1) | $\text{NI}_{\text{FY5}} > \text{NI}_{\text{FY1}}$ | +$3,382M (+57.9%) | **`PASS`** |
| **Burry** | Check 1: Operating cash flow $\ge$ Net income every year | $\text{OCF} \ge \text{NI}$ all 5 yrs | OCF exceeded NI in all 5 yrs | **`PASS`** |
| **Burry** | Check 2: Liabilities $\le 2 \times$ Equity (latest year) | $\le 2.0$ | **1.49** | **`PASS`** |

* **Panel Verdicts on COST:**
  - **Buffett:** **OWN THE BUSINESS** (3 of 3 checks passed)
  - **Graham:** **ENTERPRISING / WATCH** (2 of 3 checks passed — Current ratio fails at 1.06)
  - **Burry:** **VALUE LONG** (2 of 2 checks passed — Cash conversion high, leverage 1.49 $\le 2.0$)

---

## 4. Graham Threshold Probe: A Design Choice

In quantitative screening, financial thresholds are deliberate human design choices rather than universal economic laws. Benjamin Graham formulated his $2.0$ current ratio rule in 1934 for asset-heavy manufacturing and rail companies holding large raw materials and trade receivables.

When applied to a high-turnover modern retailer like Costco Wholesale:
* **Standard Threshold ($2.0$):** Latest current ratio is $1.06 \rightarrow$ **FAIL** (Check 1 fails, overall score 2/3).
* **Probed Threshold ($1.0$):** Latest current ratio is $1.06 \ge 1.0 \rightarrow$ **PASS** (Check 1 passes, overall score 3/3, verdict shifts to **DEFENSIVE BUY**).

### Elliot's Recorded Threshold Decision:
> **"I kept Graham's original 2.0 threshold because lowering it to 1.0 makes Costco pass but weakens the liquidity standard, showing how a screening decision depends on the threshold chosen."**

---

## 5. Project 2 Company Analysis: Apple Inc. (AAPL)

### Fund Identification & Universe Lineage
In Labs 13–15, Elliot constructed an institutional portfolio universe governed by the Meridian Foundation training case and the draft Project 2 mandate (Lab 13, Section 13):
* **Strategic Policy Benchmark:** 65% MSCI World All-Country Equity Index, 35% Bloomberg Global Aggregate Bond Index.
* **Eligible Fund Sleeve:** The equity sleeve is the **Global Equity Index Fund**, indexed to the MSCI All-Country World Index and tracked in public markets by the **iShares MSCI ACWI ETF (`ACWI`)** and the **SPDR S&P 500 ETF Trust (`SPY`)**.
* **Largest Holding:** The verified #1 largest equity holding inside this global fund universe is **Apple Inc. (ticker: `AAPL`, CIK: `0000320193`)**.
* *Note on Non-Selection:* We do not invent an existing portfolio allocation or claim Elliot previously selected a fund; rather, Apple Inc. is evaluated as the verified largest constituent holding of the benchmark global equity sleeve established in Labs 13–15.

### Audited Financial Foundation (USD Millions) — Apple Inc. (AAPL)
| Fiscal Year End | Revenue ($M) | Net Income ($M) | Operating CF ($M) | CapEx ($M) | Equity ($M) | Current Ratio | Liab / Eq | ROE | Owner Earnings ($M) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **2022-09-24** | 394,328 | 99,803 | 122,151 | 10,708 | 50,672 | 0.88 | 5.96 | 197.0% | 111,443 |
| **2023-09-30** | 383,285 | 96,995 | 110,543 | 10,959 | 62,146 | 0.99 | 4.67 | 156.1% | 99,584 |
| **2024-09-28** | 391,035 | 93,736 | 118,254 | 9,447 | 56,950 | 0.87 | 5.41 | 164.6% | 108,807 |
| **2025-09-27** | 416,161 | 112,010 | 111,482 | 12,715 | 73,733 | 0.89 | 3.87 | 151.9% | 98,767 |
| **2026-09-26** | 478,834 | 132,175 | 145,097 | 9,041 | 112,093 | 1.02 | 2.61 | 117.9% | 136,056 |

### Panel Results on AAPL
| Investor | Check Description | Requirement | AAPL Evidence | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Buffett** | 1. ROE $\ge 15.0\%$ every year | $\ge 15.0\%$ all 5 yrs | 117.9% to 197.0% | **`PASS`** |
| **Buffett** | 2. Owner earnings positive every year | $> 0$ all 5 yrs | $98,767M to $136,056M | **`PASS`** |
| **Buffett** | 3. Owner earnings grew (FY5 $>$ FY1) | $\text{OE}_{\text{FY5}} > \text{OE}_{\text{FY1}}$ | +$24,613M (+22.1%) | **`PASS`** |
| **Graham** | 1. Current ratio $\ge 2.0$ (latest year) | $\ge 2.0$ | **1.02** | **`FAIL`** |
| **Graham** | 2. Net income positive every year | $> 0$ all 5 yrs | $93,736M to $132,175M | **`PASS`** |
| **Graham** | 3. Net income grew (FY5 $>$ FY1) | $\text{NI}_{\text{FY5}} > \text{NI}_{\text{FY1}}$ | +$32,372M (+32.4%) | **`PASS`** |
| **Burry** | 1. OCF $\ge$ Net Income every year | $\text{OCF} \ge \text{NI}$ all 5 yrs | Failed in FY25 ($111,482M < $112,010M) | **`FAIL`** |
| **Burry** | 2. Liabilities $\le 2 \times$ Equity (latest year) | $\le 2.0$ | **2.61** | **`FAIL`** |

* **Panel Verdicts on AAPL:**
  - **Warren Buffett:** **OWN THE BUSINESS** (3/3 Passed)
  - **Benjamin Graham:** **ENTERPRISING / WATCH** (2/3 Passed — Current ratio 1.02 fails 2.0 hurdle)
  - **Michael Burry:** **PASS / SHORT CANDIDATE** (0/2 Passed — Cash conversion slippage in FY25 and balance sheet leverage 2.61 exceeds 2.0 limit)

---

## 6. Bull and Bear Synthesis (Two Sentences Each)

### Bull Case (From the Panel Evidence):
1. Apple demonstrates an extraordinary economic franchise with 5-year return on equity averaging over 150% and compounding owner earnings expanding from $111,443M in FY22 to $136,056M in FY26 (+22.1%), satisfying all three of Warren Buffett's business quality checks.
2. The company generated over $145B in operating cash flow in FY26 while growing GAAP net income across five consecutive profitable years, proving unmatched commercial pricing power and consumer franchise durability.

### Bear Case (From the Panel Evidence):
1. From a balance-sheet conservatism perspective, Apple fails Benjamin Graham's defensive liquidity test with a latest-year current ratio of only 1.02, reflecting minimal working capital cushion to absorb unexpected operating shocks.
2. Dr. Michael Burry's forensic screen rejects the stock completely (0/2 checks passed) because total liabilities of $292.8B exceed stockholders' equity by 2.61x, and FY25 operating cash flow ($111,482M) trailed GAAP net income ($112,010M), indicating potential working capital drain and aggressive capital structure leverage driven by debt-funded share repurchases.

---

## 7. Explain the Code & Honest Gaps

### Line-by-Line Logic: `evaluate_graham_checks`
```python
def evaluate_graham_checks(rows: List[Dict[str, Any]], current_ratio_threshold: float = 2.0) -> Dict[str, Any]:
    latest = rows[-1]
    cr_latest = latest.get("current_ratio")
    
    # Check 1: Working Capital Cushion
    if cr_latest is None or cr_latest == "not found":
        c1_status = "NOT KNOWN"
    elif cr_latest >= current_ratio_threshold:
        c1_status = "PASS"
    else:
        c1_status = "FAIL"
```
* **Missing Input Handling:** If `current_ratio` is missing or labeled `"not found"`, the function immediately outputs `"NOT KNOWN"`. It never guesses or substitutes industry averages.
* **Checks 2 & 3:** Enforce strict positivity across all five elements in `rows` for Net Income, and evaluate whether `rows[-1]["net_income"] > rows[0]["net_income"]`. If any year is missing, the dependent checks output `"NOT KNOWN"`.

### Missing-Data Verification: JPMorgan Chase (JPM)
* As verified in Lab 18, bank holding companies do not disclose traditional industrial CapEx.
* CapEx is tagged as `"not found"`, causing Owner Earnings to output `"not found"`.
* Buffett Checks 2 and 3 output `"NOT KNOWN"` with zero hallucinations or filled guesses.

---

## 8. Unsupported / Fabricated Number Detection

To satisfy the merit criteria, `legend_sec.py` implements an active audit function `detect_unsupported_numbers()`:
1. **Canonical Token Vault:** Accumulates every currency amount ($M, $B), percentage (1 decimal, 2 decimals, integer rounded), and decimal ratio computed by Python.
2. **Regex Text Scanner:** Scans every line of the investment memos for currency (`$`), percentage (`%`), or floating-point patterns.
3. **Audit Outcomes:**
   - **Costco Memos (All 3):** 0 unsupported numbers detected.
   - **Apple Memos (All 3):** 0 unsupported numbers detected.
   - **Fabrication Probe Test:** Injected hallucinations (`42.7%` and `$999.5B`) were successfully flagged by line, token, and context.

---

## 9. Elliot's Project 2 Decision & Reflections

### Personal Screening Decision:
> **"I would use the three-investor panel as an initial screening tool for Project 2, but I would verify the financial data and consider valuation before making an investment decision."**

### Reflection on Panel Disagreement:
* **Why Personas Disagree on the Same Facts:** Warren Buffett, Benjamin Graham, and Michael Burry prioritize different economic dimensions of corporate performance. Buffett focuses on operating franchise moats and reinvestment compounding, Graham focuses on liquidation downside and balance-sheet buffers, and Burry focuses on accounting accrual quality and solvency risk.
* **Threshold Sensitivity:** The Graham probe demonstrates that quantitative screens are highly sensitive to parameter choices. A strict 2.0 current ratio excludes modern cash-efficient franchises that operate with near-zero working capital float, highlighting why quantitative screens must serve as initial filters rather than final investment decisions.

---

## 10. Direct Verification Links

* **Lab 19 Root Folder:** [`Lab-19/`](.)
* **Main Writeup:** [`Lab-19/lab19.md`](lab19.md)
* **SEC Retrieval & Multi-Investor Engine:** [`Lab-19/legend_sec.py`](legend_sec.py)
* **Streamlit Application:** [`Lab-19/app.py`](app.py)
* **Automated Test Suite:** [`Lab-19/run_tests.py`](run_tests.py)
* **Package Dependencies:** [`Lab-19/requirements.txt`](requirements.txt)
* **Costco Investment Memos:**
  - Buffett: [`Lab-19/memos/costco_buffett_memo.md`](memos/costco_buffett_memo.md)
  - Graham: [`Lab-19/memos/costco_graham_memo.md`](memos/costco_graham_memo.md)
  - Burry: [`Lab-19/memos/costco_burry_memo.md`](memos/costco_burry_memo.md)
* **Apple Inc. (Project 2) Investment Memos:**
  - Buffett: [`Lab-19/memos/aapl_buffett_memo.md`](memos/aapl_buffett_memo.md)
  - Graham: [`Lab-19/memos/aapl_graham_memo.md`](memos/aapl_graham_memo.md)
  - Burry: [`Lab-19/memos/aapl_burry_memo.md`](memos/aapl_burry_memo.md)
* **Skills:**
  - Buffett: [`Lab-19/skills/warren-buffett/SKILL.md`](skills/warren-buffett/SKILL.md)
  - Graham: [`Lab-19/skills/ben-graham/SKILL.md`](skills/ben-graham/SKILL.md)
  - Burry: [`Lab-19/skills/michael-burry/SKILL.md`](skills/michael-burry/SKILL.md)
