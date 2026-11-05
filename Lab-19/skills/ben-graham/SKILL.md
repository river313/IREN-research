---
name: ben-graham
description: >-
  Analyzes publicly traded companies using Benjamin Graham's classic value investing
  and margin-of-safety philosophy. Evaluates audited SEC EDGAR 10-K financial statements,
  enforces balance sheet conservatism through working capital and earnings stability checks
  (Current Ratio >= 2.0, multi-year positive GAAP net income, and five-year net income growth),
  and generates disciplined investment memos. Use when analyzing defensive value criteria,
  working capital cushions, solvency, or applying Benjamin Graham's screening principles to any equity ticker.
---

# Benjamin Graham Value Investing Skill

This skill operationalizes Benjamin Graham's classic security analysis and defensive investment philosophy using audited financial data retrieved directly from the **SEC EDGAR API**.

The guiding principle of this skill is:
> **Python computes every financial number from SEC filings. AI interprets those numbers using Graham's investment philosophy.**
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
To run the automated Graham analysis for any publicly traded ticker:

```powershell
# Default analysis for Costco (COST)
python legend_sec.py --ticker COST

# Analysis with Graham threshold probe (e.g., threshold lowered to 1.0)
python legend_sec.py --ticker COST --graham-threshold 1.0

# Print all investor memos including Graham
python legend_sec.py --ticker COST --memos
```

---

## 3. Financial Extraction & Calculation Rules

The engine extracts audited 10-K facts directly from the SEC EDGAR API:
* **Ticker Lookup:** `https://www.sec.gov/files/company_tickers.json`
* **Company Facts:** `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json`

### Required XBRL Tags for Graham Analysis
Metric | Primary XBRL Tag | Fallback XBRL Tag | Type
:--- | :--- | :--- | :---
**Net Income** | `NetIncomeLoss` | — | Duration (1 Year)
**Current Assets** | `AssetsCurrent` | — | Instant (Fiscal Year-End)
**Current Liabilities** | `LiabilitiesCurrent` | — | Instant (Fiscal Year-End)

### Accounting Rules
1. **10-K Filings Only:** Strictly filter for annual reports (`form == '10-K'`).
2. **Current Ratio Calculation:**
   $$\text{Current Ratio} = \frac{\text{Current Assets}}{\text{Current Liabilities}}$$
   *Rule:* If Current Assets or Current Liabilities is missing or non-positive, Current Ratio is `"not found"`.
3. **Five Fiscal Years:** Track the last five fiscal years chronologically by fiscal-year-end date (`end`).
4. **Honest Gaps:** If an SEC tag is missing, mark it `"not found"`. Never interpolate or invent numbers.

---

## 4. Graham's Three Fundamental Value Checks

Graham's defensive investor rules demand strict liquidity buffers and consistent earnings:

Check | Hurdle Rate | Purpose / Rationale
:--- | :--- | :---
**Check 1: Working Capital Cushion** | Current Ratio $\ge 2.0$ in the **latest fiscal year** | Assures adequate margin of safety to absorb short-term commercial shocks without insolvency.
**Check 2: Earnings Stability** | Net Income $> 0$ in **each** of the five fiscal years | Verifies business resiliency across cyclical downturns (no deficit years).
**Check 3: Earnings Growth** | Net Income in FY5 $>$ Net Income in FY1 | Confirms positive real purchasing-power expansion over the 5-year observation window.

*Missing Input Rule:* If required inputs are missing or `"not found"`, the check status must be `"NOT KNOWN"`.

### Threshold Sensitivity Probe
In security analysis, financial screening thresholds represent deliberate design choices. When evaluating lean-working-capital retailers (such as Costco) that operate with negative or neutral working capital cycles, the traditional 2.0 industrial threshold may fail. Lowering the threshold to 1.0 tests sensitivity:
* Threshold = 2.0 $\rightarrow$ COST Current Ratio 1.06 fails (`FAIL`).
* Threshold = 1.0 $\rightarrow$ COST Current Ratio 1.06 passes (`PASS`).

---

## 5. Investment Memo Synthesis Guidelines

When generating a Benjamin Graham investment memo:
1. **Strict Provenance:** Only reference financial metrics printed by `legend_sec.py`.
2. **Unsupported Number Scanning:** Run `detect_unsupported_numbers()` across the text to guarantee no hallucinated figures exist.
3. **Transparent Verdict:**
   - 3/3 Checks Passed: **DEFENSIVE BUY**
   - 2/3 Checks Passed: **ENTERPRISING / WATCH**
   - $\le 1/3$ Checks Passed: **REJECT / DEFICIENT**
4. **Threshold Disclosure:** Explicitly document whether the standard 2.0 threshold or a probed alternative was evaluated.
