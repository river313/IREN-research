---
name: warren-buffett
description: >-
  Analyzes publicly traded companies using Warren Buffett's investment philosophy
  and official SEC EDGAR 10-K filings. Retrieves annual financial facts, computes ROE
  and owner earnings across five fiscal years, enforces Buffett's three fundamental quality
  checks, and generates disciplined investment memos evaluating business quality.
  Use when analyzing company fundamentals, owner earnings, corporate quality moats,
  or applying Buffett's criteria to any equity ticker.
---

# Warren Buffett Financial Quality Skill

This skill operationalizes Warren Buffett's value investing and franchise quality philosophy using audited financial data retrieved directly from the **SEC EDGAR API**.

The guiding principle of this skill is:
> **Python computes every financial number from SEC filings. AI interprets those numbers using Buffett's investment philosophy.**
> Do not invent, estimate, or fabricate financial figures, validation results, or test outcomes.

---

## 1. Prerequisites & Environment

* **Python Interpreter:** Python 3.10+ with standard library (`urllib.request`, `json`, `datetime`, `re`, `argparse`).
* **SEC Compliance:** All SEC EDGAR API requests must pass a legitimate `User-Agent` header formatted as:
  `User-Agent: Elliot <email@example.com>` (defaults to `SEC_EDGAR_EMAIL` or `river313@purdue.edu`).
* **Cached Ingestion:** The bundled script automatically caches SEC facts locally to prevent redundant network traffic and allow offline execution.

---

## 2. Bundled Python Execution Script

The core retrieval and calculation engine is bundled at [`scripts/buffett_sec.py`](./scripts/buffett_sec.py).

### Usage Syntax
To run the automated Buffett analysis for any publicly traded ticker:

```powershell
# Default analysis for Costco (COST)
python scripts/buffett_sec.py --ticker COST

# Analysis for any custom company (e.g., JPMorgan Chase)
python scripts/buffett_sec.py --ticker JPM

# Generate the full Markdown investment memo
python scripts/buffett_sec.py --ticker COST --memo
```

---

## 3. Financial Extraction & Calculation Rules

The bundled script retrieves data directly from:
* **Ticker Lookup:** `https://www.sec.gov/files/company_tickers.json`
* **Company Facts:** `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json`

### Required XBRL Tags
Metric | Primary XBRL Tag | Fallback XBRL Tag | Type
:--- | :--- | :--- | :---
**Revenue** | `RevenueFromContractWithCustomerExcludingAssessedTax` | `Revenues` | Duration (1 Year)
**Net Income** | `NetIncomeLoss` | — | Duration (1 Year)
**Operating Cash Flow** | `NetCashProvidedByUsedInOperatingActivities` | — | Duration (1 Year)
**CapEx (Capital Spending)** | `PaymentsToAcquirePropertyPlantAndEquipment` | `PaymentsToAcquireProductiveAssets` | Duration (1 Year)
**Stockholders' Equity** | `StockholdersEquity` | — | Instant (Fiscal Year-End)

### Strict Accounting Filters
1. **10-K Only:** Extract only filings where `form == '10-K'`.
2. **One-Year Periods:** For duration tags, enforce `350 <= (end - start).days <= 375`.
3. **Latest Filing Selection:** When multiple 10-K filings report the same period end, always select the latest `filed` date.
4. **Five Fiscal Years:** Group by actual fiscal-year-end dates (`end`), sorting chronologically, and selecting the last five years.
5. **No Invented Numbers:** If a metric is absent from SEC filings, display `"not found"`. Never invent or estimate figures.
6. **Return on Equity (ROE):**
   $$\text{ROE} = \frac{\text{Net Income}}{\text{Year-End Stockholders' Equity}}$$
   *Rule:* If equity is zero or negative, ROE must be `"not known"`.
7. **Owner Earnings:**
   $$\text{Owner Earnings} = \text{Operating Cash Flow} - \text{Capital Spending}$$
   *Rule:* If CapEx or Operating Cash Flow is missing, Owner Earnings must be `"not found"`.

---

## 4. Buffett's Three Fundamental Quality Checks

All checks must be calculated in Python; the AI must not independently alter or fabricate results:

Check | Hurdle Rate | Possible Outputs
:--- | :--- | :---
**Check 1: ROE** | ROE $\ge 15.0\%$ in **each** of the five fiscal years | `PASS`, `FAIL`, `NOT KNOWN`
**Check 2: Owner Earnings** | Owner earnings $> 0$ in **each** of the five fiscal years | `PASS`, `FAIL`, `NOT KNOWN`
**Check 3: Owner Earnings Growth** | Owner earnings in FY5 $>$ Owner earnings in FY1 | `PASS`, `FAIL`, `NOT KNOWN`

*Missing Input Rule:* If required inputs are missing or `"not found"`, the check must output `"NOT KNOWN"`.

---

## 5. Investment Memo Synthesis Guidelines

When generating an investment memo using this skill:
1. **Solely Reference Computed Data:** Every single financial number, percentage, and dollar amount mentioned in the memo must originate from the numbers printed by `buffett_sec.py`.
2. **Unsupported Number Detection:** All memo drafts must be audited using `detect_unsupported_numbers()` to ensure zero hallucinations.
3. **Explain the Three Checks:** Provide the exact status (`PASS`, `FAIL`, `NOT KNOWN`) and the underlying numbers for each check.
4. **Identify Economic Moats:** Analyze competitive barriers (low-cost scale, switching costs, network effects, brand power).
5. **Acknowledge Limitations:** Detail capital intensity, margin pressure, or geographic headwinds without inventing facts.
6. **Quality Verdict Only:** Choose exactly one conclusion:
   * `OWN THE BUSINESS`
   * `WATCH`
   * `PASS`
7. **Exclude Valuation & Market Price:** Do not include stock price, P/E ratio, market capitalization, or valuation multiples. Evaluate the *business*, not the market ticker.
8. **Student Reflection Placeholder:** Leave a clearly marked space for the student's personal one-sentence verdict. Never fabricate student opinions.

---

## 6. Philosophical Reference

Consult [`references/buffett_philosophy.md`](./references/buffett_philosophy.md) for detailed background on Buffett's mental models, moat typology, circle of competence, and Berkshire Hathaway shareholder letter principles.
