# IREN Limited (NASDAQ: IREN) — Corporate Finance Valuation & Decision System

**Course:** FIN 43900 (Corporate Finance / Applied Financial Modeling, Purdue University)  
**Student:** Elliot  
**Valuation Date:** October 8, 2026 (Audit As-of Date)  
**Primary SEC Source:** FY2026 Form 10-K (ended June 30, 2026; filed August 27, 2026)  
**Repository URL:** https://github.com/river313/IREN-research  

---

## 1. Finance Decision and Intended User

- **Intended User:** Buy-Side Investment Committee (Technology & Infrastructure Fund).
- **Security:** Ordinary Shares of IREN Limited (NASDAQ: IREN).
- **Committee Decision:** **WATCH / DEFER**.
- **Valuation Summary:** Intrinsic equity value of **-$5.31 per share** (primary 394.06M shares; sensitivity span **-$8.28 to +$0.99 per share**) vs. Market Trading Price of **$45.73** (as of September 24, 2026) and **$41.65** (as of September 3, 2026).
- **Core Thesis:** The market currently prices IREN as a pure-play hyperscale AI cloud winner ($18.0B market capitalization) following its $9.7B Microsoft contract and Horizon 1 delivery. However, our audited five-year three-statement pro-forma DCF demonstrates that IREN faces an acute intermediate **capex and financing inflection**: actual FY2026 GAAP results generated a $(702.6)M net loss, $(1,046.7)M operating loss, and cash capex of $4,333.1M. With $7.84B in carrying debt/convertible notes and deep negative FCFE through FY2029E, intrinsic equity value is negative under fundamental operating forecasts. The committee should not initiate a position until Horizons 2–4 achieve verified customer acceptance and recognized GAAP cash flow from operations inflects positively.

---

## 2. Visible Result

The primary valuation output is frozen in [`visible_output.json`](visible_output.json) and can be reviewed directly without code execution:

```json
{
  "target_company": "IREN Limited",
  "ticker": "NASDAQ: IREN",
  "decision": "WATCH / DEFER",
  "as_of": "2026-10-08",
  "modeled_valuation": {
    "methodology": "Five-Year Integrated Three-Statement Pro-Forma FCFE DCF",
    "cost_of_equity": 0.114,
    "terminal_growth_rate": 0.025,
    "value_per_share_primary": -5.31,
    "value_per_share_bs_ending": -5.51,
    "value_per_share_weighted": -6.62,
    "present_value_explicit_fcfe_usd_m": -4647.74,
    "terminal_value_usd_m": 4380.90,
    "total_implied_equity_value_usd_m": -2094.23
  },
  "accounting_checks": {
    "balance_sheet_gap_max": 0.0,
    "all_5_years_balanced": true,
    "cash_buffer_pass": true
  },
  "sensitivities": {
    "dominant_driver": "Capacity Energization Path (Revenue Scale) over the tested ranges",
    "power_cost_gross_margin_span": "$5.35/sh ($-8.28 to $-2.93)",
    "revenue_growth_path_span": "$13.44/sh ($-12.45 to $0.99)"
  }
}
```

---

## 3. Setup and Run Instructions (Windows PowerShell)

All commands are designed for direct copy-and-paste in Windows PowerShell.

> [!NOTE]
> On Windows machines, invoke Python using the `py` launcher (Python Launcher for Windows) to bypass default Windows Store app execution aliases.

### 1. Install Dependencies
```powershell
py -m pip install -r requirements.txt
```

### 2. Execute Master Valuation Engine & Generate Visible Output
```powershell
py run_analysis.py
```
*Expected terminal output: Prints summary of IREN pro-forma DCF valuation (-$5.31/sh), checks balance sheet articulation (Gap = 0.0000), and writes fresh `visible_output.json`.*

### 3. Run Week 7 Submission Manifest Audit Checker
```powershell
py project_audit.py project-submission-manifest-template.csv
```
*Expected terminal output: Audits the 12-row project submission manifest against actual repository deliverables. Reports mechanical gaps for deliverables scheduled for final Week 8 compilation (videos, transcripts, final PDFs).*

### 4. Launch Interactive Valuation Workbench (Streamlit Application)
```powershell
py -m streamlit run app.py
```
*Expected output: Launches the semi-adjustable Pro-Forma Workbench in your web browser with bounded driver sliders, live accounting check banners, dynamic statement tabs, and sensitivity explorer.*

### 5. Execute Core Pro-Forma & Sensitivity Labs
```powershell
# Run Lab 10 Full Three-Statement Pro-Forma Model & Articulation Gates
py Lab-10/proforma_iren.py

# Run Lab 11 One-At-A-Time Operating Driver Sensitivities & Trace
py Lab-11/sensitivity_iren.py

# Run Lab 12 Audited Revenue Growth Sensitivity Engine (Compounded vs. Single-Year)
py Lab-12/lab12_sensitivity.py
```

---

## 4. Repository Map

```text
IREN-research/
├── README.md                                  # Central project documentation, cold-run protocol, and setup
├── requirements.txt                           # Frozen Python dependencies (numpy, pandas, yfinance, etc.)
├── .gitignore                                 # Git configuration excluding caches, environments, and secrets
├── run_analysis.py                            # Master analysis runner; executes model and outputs visible_output.json
├── visible_output.json                        # Frozen visible executed output and accounting check contracts
├── project_audit.py                           # Course mechanical audit script for submission manifest
├── project-submission-manifest-template.csv   # Completed 12-row working copy of the submission manifest
├── validation_record.md                       # Comprehensive project validation record and AI use register
├── sources.md                                 # Source tracking and SEC filing citations
├── IREN_10-K.pdf                              # Audited Form 10-K filing (period ended June 30, 2026)
├── IREN_2026-09-03_report.md                  # Edition A baseline research report (frozen at commit 2710819)
├── docs/
│   ├── Decision-Memo.md                       # Working draft of 2-page Investment Committee Decision Memo
│   ├── Research-Evolution.md                  # Working draft of Edition A to Edition B trajectory brief
│   └── Validation-and-AI-Use.md               # Sourced data ledger, cold run logs, and locked changed-input tests
├── Lab-07/                                    # Lab 07: Comparable-company P/E valuation and peer multiples
├── Lab-08/                                    # Lab 08: Precedent transaction screening and valuation triangulation
├── Lab-09/                                    # Lab 09: Reference ABG pro-forma engine (known-answer benchmark)
├── Lab-10/                                    # Lab 10: IREN five-year three-statement integrated pro-forma engine
├── Lab-11/                                    # Lab 11: One-at-a-time pro-forma sensitivities (Gross Margin & Revenue)
├── Lab-12/                                    # Lab 12: Audited revenue growth sensitivity suite & verification checks
└── Project-1/                                 # Project 1 workspace and historical Week 3 models
    ├── dcf.py                                 # Preserved Week 3 DCF script (documents negative FCFF compounding failure)
    └── analysis/
        ├── beta.py                            # Pairwise stock/market beta regression calculator
        └── calculate_iren_beta.py             # Historical beta script using Nasdaq API (beta = 1.60)
```

---

## 5. Data Sources and Point-in-Time Boundary

All material historical inputs originate from SEC EDGAR filings:
1. **FY2026 Form 10-K:** Filed August 27, 2026 (Accession `0001878848-26-000051`, period ended June 30, 2026). Item 7 (MD&A), Item 8 (Financial Statements: pp. F-6 to F-9; Notes 4, 10, 14, 22, 23, 27, 28).
2. **FY2025 Form 10-K:** Filed August 28, 2025. Sourced for historical comparison and restated FY24 US GAAP figures.
3. **Form 20-F:** Filed August 28, 2024. Australian Foreign Private Issuer baseline under IFRS.
4. **SEC Form 8-K / Press Release (August 13, 2026):** Customer acceptance of Horizon 1 (50 MW) by Microsoft under 5-year, $9.7B agreement.

---

## 6. Financial Conventions and Assumptions

- **Revenue Modeling:** Explicitly models recognized GAAP revenue starting from $707.0M in FY2026, scaling at 100%, 50%, 30%, 15%, and 10% across the five forecast years. Contracted ARR ($4.0B) is excluded from immediate revenue recognition.
- **Operating Working Capital:** Inventory is explicitly modeled as **$0.0M** (IREN provides digital cloud compute and holds zero physical inventory). Working capital financing is driven by **Customer Prepayments / Deferred Revenue** ($1.84B in FY26), which amortizes as capacity is delivered.
- **Capital Expenditures:** Sourced from actual cash paid for PP&E + computer hardware ($4,333.1M in FY2026), correcting for aggregator undercounting. Forecast capex declines from $2,500M (FY27E) to $600M (FY31E).
- **Cost of Capital:** Cost of equity $r_e = 11.4\%$ based on CAPM ($r_f = 4.2\%$, $\beta = 1.60$, ERP = 4.5%). Perpetual growth rate $g = 2.5\%$.
- **Share Count Basis:** Primary valuation uses **394.059 million** basic ordinary shares from the 10-K cover page (August 14, 2026), reconciled against 380.194M on the June 30 balance sheet and 316.123M weighted-average diluted shares.

---

## 7. Validation, Tests, and Refusal Gates

The repository contains four distinct layers of automated verification:
1. **Synthetic Known-Answer Test:** Verified against Asbury Automotive Group (`Lab-09/proforma.py`), achieving exactly $291.75/share to the nearest cent.
2. **Double-Entry Balance Sheet Articulation:** Every forecast year enforces $\text{Assets} - \text{Liabilities} - \text{Equity} = 0.0000$ and minimum cash $\ge \$500.0\text{M}$.
3. **Refusal Gate Check:** Injected errors (e.g., +$500M artificial cash break) halt the engine immediately with loud error messages (`MODEL REFUSAL: Gap = $+500.0M`).
4. **Locked Changed-Input Record:** Human-authored precommit predictions recorded in `validation_record.md` before execution; directional monotonicity verified.

---

## 8. Known Limitations, Monitoring, and Reversal Triggers

- **Limitation:** Project 1 valuation relies on direct equity FCFE modeling due to negative operating cash flows and complex convertible note structures. The WACC-to-FCFF bridge from Week 3 remains partially uncoupled from the pro-forma statements.
- **Monitoring Trigger:** Monitor customer acceptance milestones for Childress Horizons 2–4 and quarterly operating cash flow before customer prepayments.
- **Reversal Condition:** Revisit WATCH-DEFER if recognized GAAP quarterly revenue scales above $375M ($1.5B ARR) with two consecutive quarters of positive operating cash flow, and further expansion is financed without dilutive share issuances exceeding 10%.
