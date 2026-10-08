# Research Evolution Brief — IREN Limited (NASDAQ: IREN)

**Student Name:** Elliot  
**Course:** FIN 43900 (Corporate Finance / Applied Financial Modeling, Purdue University)  
**Valuation Date:** October 8, 2026  

---

## 1. Edition A — Unchanged Baseline

- **Baseline Document of Record:** `IREN_2026-09-03_report.md` (FIN 439 Lab 04 Initial Research Report)
- **Immutable Commit Hash:** `27108195fbd49f6c7d1fb5d0fa7ddd61fec45ecd`
- **Commit Date:** September 3, 2026 18:17:39 EDT
- **Original Edition A Recommendation:** **WATCH / DEFER**
- **Original Core Claim:** While IREN achieved strong revenue growth ($707.0M in FY26) and delivered Horizon 1 to Microsoft, the company reported a $(702.6)M net loss, $13.81B in contractual capital commitments, and heavy dilution from $4.74B in equity issuance and $6.30B in convertible notes. The analyst deferred initiation until AI cloud growth proves sustainable profitability and cash generation.
- **Edition A Integrity Status:** Unchanged and preserved intact in the repository root.

---

## 2. Dated Correction Addendum

- **Addendum Date:** September 24, 2026 (Discovered during Lab 10 pro-forma construction)
- **Item 1: SEC Filing Form Transition (Form 20-F to Form 10-K):**
  - *Correction:* In FY2024, IREN reported as an Australian Foreign Private Issuer under IFRS on Form 20-F. When it transitioned to US domestic issuer status in FY2025, it retroactively restated FY2024 financials under US GAAP. Comparative figures used across Labs 10–12 reflect audited US GAAP restatements from the FY2026 Form 10-K, ensuring accounting consistency.
- **Item 2: Capital Expenditure Data Aggregator Distortion:**
  - *Correction:* Data aggregators (Yahoo Finance, CapIQ) reported FY2026 Capex as $2,998.0M, capturing only "Additions to property, plant and equipment." Inspection of the audited Consolidated Statement of Cash Flows (p. F-9) revealed an additional $1,335.1M in "Payments for computer hardware" (GPU clusters). Actual cash capex was $4,333.1M, understating capital burn by 30.8% in external databases.
- **Item 3: Multi-Basis Share Count Reconciliation:**
  - *Correction:* Reconciled three conflicting share counts reported in the FY2026 10-K: 394.059M basic ordinary shares on the cover page (August 14, 2026); 380.194M on the June 30, 2026 Balance Sheet; and 316.123M diluted weighted-average shares on the Statement of Operations. The primary valuation adopts 394.059M to reflect actual current equity claims.

---

## 3. Edition B — After Project-Specific Research and Disclosed AI Assistance

### Current Decision and Intended User
- **Recommendation:** **WATCH / DEFER** (Affirmed and rigorously quantified).
- **Intended User:** Buy-Side Investment Committee.
- **Modeled Valuation Range:** Intrinsic equity value of **-$8.28 to +$0.99 per share** (Base Modeled Value: **-$5.31 per share** across 394.06M shares) vs. Current Market Price of **$45.73** (as of September 24, 2026) and **$41.65** (as of September 3, 2026).

### A-to-B Evidence Table

| Item | Edition A (2026-09-03) | Edition B (2026-10-08) | Primary Driver of Change | Evidence / Test Justifying Changed or Unchanged Position |
| :--- | :--- | :--- | :--- | :--- |
| **Thesis & Recommendation** | WATCH / DEFER based on qualitative trade-off: rapid AI growth vs. massive capital commitments and net loss. | WATCH / DEFER rigorously affirmed: fully modeled 5-year pro-forma DCF produces **-$5.31/sh**, revealing a multi-billion capex gap before positive FCFE. | **Own Analysis & Model Evolution** | Pro-forma DCF proves FCFE remains negative through FY29E (-$4.1B in FY27E, -$1.2B in FY28E, -$402M in FY29E). FCFE turns positive only in FY30E ($131M) and FY31E ($380M). |
| **Valuation Architecture** | Qualitative multiples and high-level DCF outline; no dynamic statement modeling. | Dynamic Five-Year Three-Statement Integrated Pro-Forma FCFE DCF with double-entry balance sheet articulation checks. | **Course Instruction & Own Implementation** | Built company-specific driver architecture (Lab 10): zero-inventory digital infrastructure, customer prepayments ($1.84B) driving working capital liquidity, and scheduled debt repayments. |
| **Data & Source Choice** | Initial review of FY26 Form 10-K headline figures. | Audited three-year historical grid (FY24–FY26), audited capex ($4,333.1M), and reconciliation of three distinct share counts. | **Own Research & Independent Auditing** | Overruled third-party aggregator data ($2,998M capex) by tracing cash paid for PP&E + computer hardware on Form 10-K p. F-9. |
| **Assumption & Driver Hierarchy** | Focused broadly on GPU procurement, power capacity, and contract size. | Quantified one-at-a-time sensitivities: Capacity Energization Path (VPS span: $13.44) dominant over Gross Power Margin (VPS span: $5.35). | **Course Instruction & Peer Challenge** | Lab 11 & Lab 12 sensitivity engines isolated causal links: revenue scale from substation energization drives 2.51x the value impact of a 10 pp power margin shift over tested ranges. |
| **Validation & Failure Controls** | No formal code testing or accounting check gates. | Triple validation suite: Lab 09 ABG known-answer check ($291.75), balance sheet double-entry refusal gate (Gap == 0.0000), stress test refusal on negative FCFE terminal value. | **Course Instruction & Validation Design** | Verified model refusal behavior by injecting +$500M artificial cash error (script halted with error). Verified cold-run reproducibility via `py` launcher. |

---

## 4. What Changed from Edition A to Edition B, and Why?

The central recommendation did **not** change: both editions conclude that the fund must **WATCH / DEFER** rather than initiate a buy position in IREN Limited. However, the nature and authority of the evidence supporting this conclusion evolved fundamentally:

1. **From Qualitative Hesitation to Exact Quantitative Proof:**  
   In Edition A, WATCH-DEFER was driven by skepticism over IREN's reported $(702.6)M net loss, $13.81B in contractual obligations, and reliance on $11.0B in external financing. In Edition B, this hesitation is replaced by an audited three-statement pro-forma financial model. The model proves mathematically that even if IREN scales recognized GAAP revenue at 100% in FY27 and 50% in FY28, reaching $3.5B by FY31, the required cash capex ($2.5B in FY27, $1.5B in FY28, $1.0B in FY29) consumes all operating liquidity. Modeled equity value under base operating assumptions is **-$5.31 per share**.

2. **Resolution of Data and Working Capital Mechanics:**  
   In Edition A, working capital dynamics were unmodeled. In Edition B, we recognized that IREN carries **zero inventory** ($0.0M) and that customer prepayments ($1.84B in FY26, primarily Microsoft) represent the company's primary non-dilutive liquidity source. This was hard-coded into the balance sheet and cash flow statement, replacing generic corporate working capital formulas.

3. **Identification of Load-Bearing Operating Drivers:**  
   Through one-at-a-time sensitivity testing in Labs 11 and 12, we proved that the **Capacity Energization Path** (revenue scaling from new MW energization) is the single most load-bearing driver, generating an implied share price span of $13.44 (from -$12.45 to +$0.99), compared to $5.35 for Cash Gross Margin (power cost efficiency). This establishes that IREN's valuation is driven by execution on energization and infrastructure delivery, not mere power pricing fluctuations.
