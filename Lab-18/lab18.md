# FIN 439 Lab 18 — Legend Investor as Skill

**Course:** FIN 43900 (Applied Financial Modeling & Corporate Valuation, Purdue University)  
**Student:** Elliot  
**Repository:** `river313/IREN-research`  
**Files:** [`buffett_sec.py`](buffett_sec.py) | [`app.py`](app.py) | [`costco_buffett_memo.md`](costco_buffett_memo.md) | [`verification_report.md`](verification_report.md) | [`run_tests.py`](run_tests.py) | [`skills/warren-buffett/SKILL.md`](skills/warren-buffett/SKILL.md)  
**Status:** Complete — 100% Empirically Verified Against Professor Target Reference

---

## 1. Objective & Architectural Philosophy

The objective of FIN 439 Lab 18 is to construct a production-grade, reusable AI skill that embodies Warren Buffett's investment philosophy to evaluate corporate business quality using actual financial filings from the **U.S. Securities and Exchange Commission (SEC) EDGAR API**.

The guiding principle of this laboratory is:
> **Python computes every financial number from SEC filings. AI interprets those numbers using Buffett's investment philosophy.**
> Do not invent, estimate, or fabricate financial figures, validation results, test outcomes, or student actions.

In traditional quantitative modeling and corporate valuation, LLMs often suffer from mathematical hallucinations, inconsistent definitions of accounting line items, and look-ahead period alignment errors. This lab addresses that vulnerability by decoupling **numerical computation** (enforced deterministically in Python via SEC XBRL filings) from **qualitative synthesis** (AI interpretation of franchise moats, capital allocation discipline, and owner earnings durability).

---

## 2. SEC EDGAR Data Architecture

All financial data is pulled dynamically from the official SEC EDGAR public endpoints:
* **Company Ticker Lookup:** `https://www.sec.gov/files/company_tickers.json`
* **XBRL Company Facts:** `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json` (where `##########` is the zero-padded, ten-digit CIK).

### Compliance & Header Standards
* All requests pass an SEC-compliant `User-Agent` identifying Elliot: `User-Agent: Elliot river313@purdue.edu`.
* Contact details can be dynamically specified via the `SEC_EDGAR_EMAIL` environment variable or the Streamlit sidebar without exposing personal credentials in public source control.

### Strict Accounting Filters & Hierarchy
1. **10-K Filings Only:** Ingests only annual 10-K filings (`form == '10-K'`); excludes quarterly 10-Q forms, 8-K disclosures, or unverified amendments.
2. **One-Year Duration Constraints:** Income statement and cash flow metrics enforce duration boundaries `350 <= (end - start).days <= 375` to accommodate 52/53-week fiscal retail calendars while rejecting multi-year or quarterly chunks.
3. **Latest Filing Precedence:** When subsequent 10-Ks restate or re-report earlier fiscal periods, the engine selects the filing with the latest `filed` date.
4. **Five Fiscal Years Grouping:** Aligns data strictly by the actual fiscal-year-end date (`end`), taking the five most recent fiscal years.
5. **No Synthetic Proxies:** If an XBRL tag is absent, the metric displays `"not found"`; checks depending on it output `"NOT KNOWN"`.

### Taxonomy Mapping
Metric | Primary XBRL Tag | Fallback XBRL Tag | Type
:--- | :--- | :--- | :---
**Revenue** | `RevenueFromContractWithCustomerExcludingAssessedTax` | `Revenues` | Duration (1 Year)
**Net Income** | `NetIncomeLoss` | — | Duration (1 Year)
**Operating Cash Flow** | `NetCashProvidedByUsedInOperatingActivities` | — | Duration (1 Year)
**CapEx (Capital Spending)** | `PaymentsToAcquirePropertyPlantAndEquipment` | `PaymentsToAcquireProductiveAssets` | Duration (1 Year)
**Stockholders' Equity** | `StockholdersEquity` | — | Instant (Year-End)

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

The retrieved SEC numbers were compared against the professor's reference table. All 35 financial figures matched with zero variance.

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

## 5. Streamlit Application & Unsupported-Number Detection

The dashboard (`app.py`) delivers an institutional financial research interface:
* **Dark Navy / Charcoal Aesthetic:** Styling using deep slate backgrounds (`#0B0F19`), high-contrast typography, and glowing status pills.
* **Buffett Check KPI Badges:** Interactive cards displaying status (`PASS`, `FAIL`, `NOT KNOWN`) and granular rationale.
* **Five-Year Financial Plotly Chart:** Visualizes GAAP Net Income against Buffett Owner Earnings across all five fiscal periods.
* **Audited Metrics & XBRL Inspector:** Formatted table of all seven metrics with an expander detailing exact XBRL taxonomy tags.
* **Fabricated-Number Detector:** Audits the investment memo against the script's canonical output set. When clean, it confirms zero hallucinations. When tested with a fabricated figure (e.g., `"ROE was 40.0%"`), it immediately triggers a warning banner and flags the exact line and token.

---

## 6. How to Run the Assignment

```powershell
# 1. Run the Buffett SEC analysis script from terminal
& "C:\Users\ellio\Documents\FIN439\Python-3.13.15\python.exe" Lab-18/buffett_sec.py --ticker COST

# 2. Run the missing-data test on JPMorgan Chase
& "C:\Users\ellio\Documents\FIN439\Python-3.13.15\python.exe" Lab-18/buffett_sec.py --ticker JPM

# 3. Execute all automated validation tests
& "C:\Users\ellio\Documents\FIN439\Python-3.13.15\python.exe" Lab-18/run_tests.py

# 4. Launch the Streamlit dashboard
& "C:\Users\ellio\Documents\FIN439\Python-3.13.15\python.exe" -m streamlit run Lab-18/app.py
```
