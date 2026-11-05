---
name: michael-burry
description: >-
  Analyzes publicly traded companies using Dr. Michael Burry's forensic value investing
  and cash flow quality philosophy. Scrutinizes audited SEC EDGAR 10-K financial disclosures,
  enforces cash flow conversion integrity (Operating Cash Flow >= Net Income across all five years)
  and balance sheet leverage limits (Total Liabilities <= 2 * Stockholders' Equity in latest year),
  and generates disciplined investment memos. Use when analyzing earnings quality, accrual risks,
  debt leverage, bankruptcy protection, or applying Michael Burry's forensic criteria to any equity ticker.
---

# Michael Burry Forensic Cash Flow & Leverage Skill

This skill operationalizes Dr. Michael Burry's deep-value and forensic accounting philosophy using audited financial data retrieved directly from the **SEC EDGAR API**.

The guiding principle of this skill is:
> **Python computes every financial number from SEC filings. AI interprets those numbers using Burry's investment philosophy.**
> Do not invent, estimate, or fabricate financial figures, validation results, or test outcomes.

---

## 1. Prerequisites & Environment

* **Python Interpreter:** Python 3.10+ with standard library (`urllib.request`, `json`, `datetime`, `re`, `argparse`).
* **SEC Compliance:** All SEC EDGAR API requests must pass a legitimate `User-Agent` header formatted as:
  `User-Agent: Elliot <email@example.com>` (defaults to `SEC_EDGAR_EMAIL` or `river313@purdue.edu`).
* **Cached Ingestion:** The bundled script caches SEC facts locally to avoid redundant network queries and ensure offline reproducibility.

---

## 2. Bundled Python Execution Script

The core retrieval and multi-investor calculation engine is bundled at [`../../legend_sec.py`](../../legend_sec.py) (or [`legend_sec.py`](./legend_sec.py)).

### Usage Syntax
To run the automated Burry analysis for any publicly traded ticker:

```powershell
# Default analysis for Costco (COST)
python legend_sec.py --ticker COST

# Analysis for custom ticker
python legend_sec.py --ticker JPM

# Print all investor memos including Burry
python legend_sec.py --ticker COST --memos
```

---

## 3. Financial Extraction & Calculation Rules

The engine extracts audited 10-K facts directly from the SEC EDGAR API:
* **Ticker Lookup:** `https://www.sec.gov/files/company_tickers.json`
* **Company Facts:** `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json`

### Required XBRL Tags for Burry Analysis
Metric | Primary XBRL Tag | Fallback XBRL Tag | Type
:--- | :--- | :--- | :---
**Net Income** | `NetIncomeLoss` | — | Duration (1 Year)
**Operating Cash Flow** | `NetCashProvidedByUsedInOperatingActivities` | — | Duration (1 Year)
**Total Liabilities** | `Liabilities` | — | Instant (Fiscal Year-End)
**Stockholders' Equity** | `StockholdersEquity` | — | Instant (Fiscal Year-End)

### Accounting Rules
1. **10-K Filings Only:** Strictly filter for annual reports (`form == '10-K'`).
2. **Liabilities to Equity Ratio:**
   $$\text{Liabilities to Equity} = \frac{\text{Total Liabilities}}{\text{Stockholders' Equity}}$$
   *Rule:* If Liabilities or Equity is missing or Equity $\le 0$, ratio is `"not found"`.
3. **Five Fiscal Years:** Track the last five fiscal years chronologically by fiscal-year-end date (`end`).
4. **Honest Gaps:** If an SEC tag is missing, mark it `"not found"`. Never interpolate or invent numbers.

---

## 4. Burry's Two Fundamental Forensic Checks

Burry's checks target forensic accounting vulnerabilities and capital structure risk:

Check | Hurdle Rate | Purpose / Rationale
:--- | :--- | :---
**Check 1: Cash Flow Quality** | Operating Cash Flow $\ge$ Net Income in **each** of the five fiscal years | Audits earnings conversion. Ensures GAAP reported net income is backed by real operational cash inflows rather than aggressive accruals or deferred revenues.
**Check 2: Solvency & Debt Manageability** | Total Liabilities $\le 2 \times$ Stockholders' Equity in the **latest fiscal year** | Enforces balance sheet protection against debt overhang, solvency distress, and creditor intervention during economic downturns.

*Missing Input Rule:* If required inputs are missing or `"not found"`, the check status must be `"NOT KNOWN"`.

---

## 5. Investment Memo Synthesis Guidelines

When generating a Michael Burry investment memo:
1. **Strict Provenance:** Only reference financial metrics printed by `legend_sec.py`.
2. **Unsupported Number Scanning:** Run `detect_unsupported_numbers()` across the text to guarantee no hallucinated figures exist.
3. **Transparent Verdict:**
   - 2/2 Checks Passed: **VALUE LONG**
   - 1/2 Checks Passed: **HIGH RISK / SKEPTICAL**
   - 0/2 Checks Passed: **SHORT CANDIDATE / AVOID**
