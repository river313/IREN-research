# FIN 439 Lab 18 — Legend Investor as Skill

**Course:** FIN 43900 (Applied Financial Modeling & Corporate Valuation, Purdue University)  
**Student:** Elliot  
**Repository:** `river313/IREN-research`  
**Files:** [`buffett_sec.py`](buffett_sec.py) | [`app.py`](app.py) | [`costco_buffett_memo.md`](costco_buffett_memo.md) | [`run_tests.py`](run_tests.py) | [`requirements.txt`](requirements.txt) | [`skills/warren-buffett/SKILL.md`](skills/warren-buffett/SKILL.md)  
**Status:** Complete — Verified against Costco reference data and SEC EDGAR filings

---

## 1. Objective & Architectural Philosophy

The objective of FIN 439 Lab 18 is to construct a reusable AI skill that embodies Warren Buffett's investment philosophy to evaluate corporate business quality using audited financial data from the **SEC EDGAR API**.

The guiding principle of this laboratory is:
> **Python computes every financial number from SEC filings. AI interprets those numbers using Buffett's investment philosophy.**
> Do not invent, estimate, or fabricate financial figures, validation results, test outcomes, or student actions.

In corporate valuation and financial research, large language models often hallucinate financial figures, misapply accounting definitions, or mix fiscal year dates. This system solves that problem by decoupling **numerical calculation** (enforced in Python from official SEC XBRL filings) from **qualitative interpretation** (AI analysis of economic moats, competitive durability, and owner earnings compounding).

---

## 2. SEC EDGAR Data Architecture

All financial data is pulled dynamically from the official SEC EDGAR public endpoints:
* **Company Ticker Lookup:** `https://www.sec.gov/files/company_tickers.json`
* **XBRL Company Facts:** `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json` (where `##########` is the zero-padded, ten-digit CIK).

### Request Standards & Privacy
* Requests pass an SEC-compliant `User-Agent` identifying Elliot: `User-Agent: Elliot river313@purdue.edu`.
* Contact details can be configured via the `SEC_EDGAR_EMAIL` environment variable or the Streamlit sidebar without committing personal credentials to public source control.

### Strict Accounting Filters
1. **10-K Filings Only:** Ingests only annual 10-K filings (`form == '10-K'`); ignores quarterly 10-Q forms and 8-K disclosures.
2. **One-Year Duration Constraints:** Income statement and cash flow items enforce duration boundaries `350 <= (end - start).days <= 375` to accommodate 52/53-week fiscal retail calendars while rejecting multi-year or quarterly periods.
3. **Latest Filing Precedence:** When subsequent 10-Ks report earlier fiscal periods, the engine selects the filing with the latest `filed` date.
4. **Five Fiscal Years Grouping:** Aligns data strictly by the actual fiscal-year-end date (`end`), taking the five most recent fiscal years.
5. **No Synthetic Proxies:** If an XBRL tag is absent, the metric displays `"not found"`; checks depending on it output `"NOT KNOWN"`.

### XBRL Taxonomy Mapping
Metric | Primary XBRL Tag | Fallback XBRL Tag | Type
:--- | :--- | :--- | :---
**Revenue** | `RevenueFromContractWithCustomerExcludingAssessedTax` | `Revenues` | Duration (1 Year)
**Net Income** | `NetIncomeLoss` | — | Duration (1 Year)
**Operating Cash Flow** | `NetCashProvidedByUsedInOperatingActivities` | — | Duration (1 Year)
**CapEx (Capital Spending)** | `PaymentsToAcquirePropertyPlantAndEquipment` | `PaymentsToAcquireProductiveAssets` | Duration (1 Year)
**Stockholders' Equity** | `StockholdersEquity` | — | Instant (Fiscal Year-End)

### Core Formulas
$$\text{Return on Equity (ROE)} = \frac{\text{Net Income}}{\text{Year-End Stockholders' Equity}}$$
*(If Equity $\le 0$, ROE is defined as `"not known"`)*

$$\text{Owner Earnings} = \text{Operating Cash Flow} - \text{Capital Spending}$$
*(If CapEx or OCF is absent, Owner Earnings is defined as `"not found"`)*

---

## 3. Buffett's Three Fundamental Checks

Check | Hurdle Rate | Costco (COST) | JPMorgan (JPM)
:--- | :--- | :---: | :---:
**Check 1: ROE** | $\ge 15.0\%$ in each of the 5 fiscal years | **`PASS`** (25.1% – 31.2%) | **`FAIL`** (12.9% in 2022)
**Check 2: Owner Earnings** | Positive ($> 0$) in each of the 5 fiscal years | **`PASS`** ($3,501M – $9,382M) | **`NOT KNOWN`** (CapEx not found)
**Check 3: Owner Earnings Growth** | Final year Owner Earnings $>$ Initial year | **`PASS`** (+$5,881M, +168.0%) | **`NOT KNOWN`** (No initial/final OE)

---

## 4. Costco (COST) Reference Reconciliation

The retrieved SEC numbers were tested against the professor's reference table. All 35 financial figures matched with zero variance.

| Fiscal Year End | Revenue ($M) | Net Income ($M) | Operating Cash Flow ($M) | CapEx ($M) | Equity ($M) | ROE | Owner Earnings ($M) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **2022-08-28** | 226,954 | 5,844 | 7,392 | 3,891 | 20,642 | 28.3% | 3,501 |
| **2023-09-03** | 242,290 | 6,292 | 11,068 | 4,323 | 25,058 | 25.1% | 6,745 |
| **2024-09-01** | 254,453 | 7,367 | 11,339 | 4,710 | 23,622 | 31.2% | 6,629 |
| **2025-08-31** | 275,235 | 8,099 | 13,335 | 5,498 | 29,164 | 27.8% | 7,837 |
| **2026-08-30** | 303,154 | 9,226 | 15,817 | 6,435 | 35,803 | 25.8% | 9,382 |

All figures represent audited SEC facts:
* Revenue tag: `RevenueFromContractWithCustomerExcludingAssessedTax`
* Net Income tag: `NetIncomeLoss`
* Operating Cash Flow tag: `NetCashProvidedByUsedInOperatingActivities`
* CapEx tag: `PaymentsToAcquirePropertyPlantAndEquipment`
* Equity tag: `StockholdersEquity`

---

## 5. Required Tests & Findings

### Test A: JPMorgan Chase (JPM) Missing-Data Test
* Commercial banks do not report conventional capital expenditures under `PaymentsToAcquirePropertyPlantAndEquipment` or `PaymentsToAcquireProductiveAssets`.
* CapEx is reported as `"not found"`, causing Owner Earnings to display `"not found"`.
* Check 1 (ROE $\ge 15\%$): `FAIL` (2022 ROE was 12.9%).
* Checks 2 and 3: `NOT KNOWN`.
* The investment memo generator acknowledges that owner earnings cannot be evaluated with the available inputs.

### Test B: Unsupported / Fabricated Number Detection
* The script indexes all numbers printed during retrieval (currencies, percentages, integers).
* When scanning a clean investment memo, the detector reports `0` flags.
* When tested with an unverified claim (`"Costco's ROE was 40.0% in 2024"`), the detector flags `40.0%` with the exact line number and surrounding context.

### Test C: Independent Comparison Protocol (For Student Execution)
To complete the comparison required by the professor:
1. Submit this prompt to an unaugmented AI chat (ChatGPT, Claude, or Gemini Web):
   > *"Act as legendary investor Warren Buffett and evaluate Costco Wholesale Corporation (COST) as a long-term investment. What are Costco's Return on Equity and Owner Earnings over the last five fiscal years, what are your three quality checks, and what is your investment recommendation?"*
2. Compare whether the unaugmented AI invents numbers, miscalculates owner earnings, uses calendar years instead of Costco's August/September fiscal ends, or violates the quality-only mandate by citing stock price.

---

## 6. Streamlit Dashboard Features

The dashboard (`app.py`) provides an investment research interface:
* **Attribution:** `"Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice."`
* **Ticker Input:** Supports looking up any publicly traded US stock symbol via SEC CIK mapping.
* **Buffett Check Cards:** Visual badges showing `PASS`, `FAIL`, or `NOT KNOWN` alongside underlying details.
* **Five-Year Financial Chart:** Plotly chart comparing GAAP Net Income to Buffett Owner Earnings.
* **Audited Financial Table:** Displays all seven metrics with an expander showing the source XBRL tags.
* **Investment Memo & Active Detector:** Includes an interactive memo editor and real-time scanner that flags unsupported financial numbers.

---

## 7. Execution Commands

```powershell
# 1. Run Buffett SEC analysis from command line (Costco)
& "C:\Users\ellio\Documents\FIN439\Python-3.13.15\python.exe" Lab-18/buffett_sec.py --ticker COST

# 2. Run missing-data analysis (JPMorgan Chase)
& "C:\Users\ellio\Documents\FIN439\Python-3.13.15\python.exe" Lab-18/buffett_sec.py --ticker JPM

# 3. Execute automated test suite
& "C:\Users\ellio\Documents\FIN439\Python-3.13.15\python.exe" Lab-18/run_tests.py

# 4. Launch the Streamlit application
& "C:\Users\ellio\Documents\FIN439\Python-3.13.15\python.exe" -m streamlit run Lab-18/app.py
```
