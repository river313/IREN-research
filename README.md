# IREN Limited (NASDAQ: IREN) — Corporate Finance Valuation & Decision System

**Course:** FIN 43900 (Corporate Finance / Applied Financial Modeling, Purdue University)  
**Student:** Elliot  
**Valuation Date:** October 8, 2026 (Audit As-of Date)  
**Primary SEC Source:** FY2026 Form 10-K (ended June 30, 2026; filed August 27, 2026)  
**Repository URL:** https://github.com/river313/IREN-research  

---

## 1. Finance Decision and Intended User

- **Intended User:** Buy-Side Investment Committee (Technology & Infrastructure Fund / Corporate Finance AI Task Force).
- **Security:** Ordinary Shares of IREN Limited (NASDAQ: IREN).
- **Committee Decision:** **WATCH / DEFER** (Do not initiate a buy position; zero allocation).
- **Primary Valuation Architecture:** Five-Year Three-Statement Integrated Pro-Forma FCFF Enterprise DCF with Enterprise-to-Equity Bridge.
  - **Base Implied Intrinsic Equity Value:** **$12.12 per share** (Enterprise Value: **$6,715.33M**; Implied Equity Value: **$4,774.18M** across 394.059M basic ordinary shares).
  - **Modeled Valuation Range:** **$4.06 to $19.25 per share** (Capacity Energization Path sensitivity span: **$15.19/sh**).
- **Secondary Methodological Benchmark:** Direct Equity FCFE DCF of **-$5.31 per share** (sensitivity span: **-$8.28 to +$0.99 per share**).
  - *Methodological Reconciliation:* Direct FCFE produces -$5.31 because explicit multi-billion capex in FY27E–FY28E causes negative cash flows before cash flows recover; however, because that capex is pre-funded from the $5,895.6M cash already sitting on the balance sheet, the FCFF Enterprise DCF properly captures the asset value and yields $12.12/share. Both methods confirm that the current market price of **$45.73** (as of September 24, 2026; ~280% premium over fundamental FCFF value) and **$41.65** (as of September 3, 2026) is substantially overvalued.
- **Core Thesis:** The market currently prices IREN as an unencumbered hyperscale AI cloud winner ($18.0B market capitalization) following its $9.7B Microsoft contract and Horizon 1 delivery. However, our audited five-year three-statement pro-forma DCF demonstrates that IREN faces an acute intermediate **capex and financing inflection**: actual FY2026 GAAP results generated a $(702.6)M net loss, $(1,046.7)M operating loss, and cash capex of $4,333.1M ($2,998.0M PP&E additions + $1,335.1M computer hardware payments, uncounted by third-party aggregators). With $7.84B in carrying debt/convertible notes and heavy near-term capital expenditure ($4.0B over FY27E–FY28E), fundamental equity value is $12.12 per share. The committee should not initiate an equity position until Horizons 2–4 achieve verified customer acceptance and recognized GAAP cash flow from operations inflects positively.

---

## 2. Visible Result

The primary valuation output is frozen in [`visible_output.json`](visible_output.json) and can be reviewed directly without code execution:

```json
{
  "target_company": "IREN Limited",
  "ticker": "NASDAQ: IREN",
  "decision": "WATCH / DEFER",
  "committee_action": "Do not initiate a buy position. The market prices IREN at $45.73 (~$18.0B market cap), representing a ~280% premium to fundamental operating FCFF DCF value ($12.12/share). Defer position pending customer acceptance of Horizons 2-4 and recognized GAAP operating cash flow inflection.",
  "as_of": "2026-10-08",
  "valuation_date": "2026-09-24",
  "filing_source": "FY2026 Form 10-K (ended June 30, 2026; filed August 27, 2026)",
  "intended_user": "Buy-side Investment Committee (AI Task Force embedded in corporate finance team)",
  "currency": "USD",
  "share_counts": {
    "primary_10k_cover_page": 394.059,
    "balance_sheet_ending": 380.194,
    "weighted_average_diluted": 316.123
  },
  "modeled_valuation": {
    "primary_required_architecture": {
      "methodology": "Five-Year Pro-Forma Operating FCFF DCF with WACC & Enterprise-to-Equity Bridge",
      "wacc": 0.1,
      "terminal_growth_rate": 0.025,
      "pv_explicit_fcff_usd_m": -2238.85,
      "terminal_value_fcff_usd_m": 14420.8,
      "pv_terminal_value_usd_m": 8954.18,
      "enterprise_value_usd_m": 6715.33,
      "bridge_cash_usd_m": 5895.59,
      "bridge_debt_usd_m": 7836.74,
      "net_debt_usd_m": 1941.15,
      "implied_equity_value_usd_m": 4774.18,
      "value_per_share_primary": 12.12,
      "valuation_range_primary": "$4.06 to $19.25"
    },
    "secondary_fcfe_comparison": {
      "methodology": "Direct Equity FCFE DCF (Unadjusted for Cash Balance)",
      "cost_of_equity": 0.114,
      "terminal_growth_rate": 0.025,
      "value_per_share_primary": -5.31,
      "reconciliation_explanation": "Direct FCFE yields -$5.31 because explicit capex of $4.0B in FY27E-FY28E causes negative FCFE before cash flows recover; however, because that capex is funded from the $5,895.6M cash already sitting on the balance sheet, the FCFF Enterprise DCF properly captures the asset value and yields $12.12/share. Both methods confirm that the current market price of $45.73 is substantially overvalued."
    },
    "market_comparison_prices": {
      "2026-09-03": 41.65,
      "2026-09-24": 45.73,
      "market_premium_over_fcff": 277.3
    }
  },
  "proforma_fy2031e_summary_usd_m": {
    "total_revenue": 3488.02,
    "operating_income_ebit": 777.88,
    "depreciation_amortization": 809.17,
    "gaap_net_income": 503.09,
    "operating_cash_flow": 1380.39,
    "capital_expenditures": 600.0,
    "free_cash_flow_to_equity_fcfe": 380.39,
    "free_cash_flow_to_firm_fcff": 1055.18
  },
  "accounting_checks": {
    "balance_sheet_gap_max": 0.0,
    "all_5_years_balanced": true,
    "cash_buffer_pass": true,
    "minimum_cash_buffer_usd_m": 500.0
  },
  "sensitivities": {
    "fcff_power_cost_margin_span": {
      "tested_range": "65.0% to 75.0%",
      "vps_range": "$8.96 to $14.61",
      "vps_span": 5.65
    },
    "fcff_revenue_path_shift_span": {
      "tested_range": "-5.0 pp/yr to +5.0 pp/yr across 5 years",
      "vps_range": "$4.06 to $19.25",
      "vps_span": 15.19
    },
    "dominant_driver": "Capacity Energization Path (Revenue Scale) over the tested ranges"
  },
  "reversal_trigger": "Change recommendation from WATCH-DEFER to INITIATE-BUY if: (1) market price corrects toward the fundamental valuation range ($12-$18), OR (2) IREN demonstrates verified customer acceptance and recognized billing for Horizons 2-4 scaling GAAP quarterly revenue above $375M, positive operating cash flow generation before customer prepayments, and capital additions funded without equity dilution exceeding 10%.",
  "kill_conditions": "Reject valuation model if pro-forma balance sheet does not articulate (Gap > $0.01M), if cash falls below $500.0M liquidity reserve, or if power purchase agreements fail to maintain gross power margin above 50%."
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
*Expected terminal output: Prints summary of IREN pro-forma DCF valuation ($12.12/sh primary FCFF, -$5.31/sh secondary FCFE), checks balance sheet articulation (Gap = 0.0000), and writes fresh `visible_output.json`.*

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
├── app.py                                     # Streamlit interactive valuation workbench application
├── compile_pdfs.py                            # ReportLab PDF compiler for course deliverables
├── run_analysis.py                            # Master analysis runner; executes model and outputs visible_output.json
├── visible_output.json                        # Frozen visible executed output and accounting check contracts
├── project_audit.py                           # Course mechanical audit script for submission manifest
├── project-submission-manifest-template.csv   # Completed 12-row working copy of the submission manifest
├── validation_record.md                       # Comprehensive project validation record and AI use register
├── sources.md                                 # Source tracking and SEC filing citations
├── Decision-Memo.pdf                          # Compiled formal 2-page Investment Committee Decision Memo
├── Research-Evolution.pdf                     # Compiled formal 1-page Research Evolution Brief
├── Validation-and-AI-Use.pdf                  # Compiled formal 2-page Validation and AI Use Record
├── IREN_10-K.pdf                              # Audited Form 10-K filing (period ended June 30, 2026)
├── IREN_2026-09-03_report.md                  # Edition A baseline research report (frozen at commit 2710819)
├── docs/
│   ├── Decision-Memo.md                       # Source Markdown of 2-page Investment Committee Decision Memo
│   ├── Research-Evolution.md                  # Source Markdown of Edition A to Edition B trajectory brief
│   └── Validation-and-AI-Use.md               # Source Markdown of data ledger, cold run logs, and tests
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

- **Modeling Boundary & Valuation Methodology:** The primary required valuation architecture is a Five-Year Three-Statement Pro-Forma FCFF Enterprise DCF with an Enterprise-to-Equity Bridge, fully coupled with the integrated dynamic statements in `run_analysis.py` (0.0000 balance sheet gap). A secondary direct FCFE benchmark (-$5.31/sh) is maintained for comparison. A known modeling boundary is that IREN's $6.30B in convertible senior notes are carried at contract principal debt value on the bridge ($7,836.7M total carrying debt) rather than dynamically bifurcated into straight debt and conversion call-option components under Black-Scholes or lattice models.
- **Observable Monitoring Triggers:**
  1. *Horizon Energization & Customer Acceptance:* Formal SEC filing or press release confirming commercial energization and customer acceptance of Childress Horizons 2, 3, and 4 (targeting Q4 2026 / H1 2027).
  2. *Operating Cash Flow Inflection:* Recognized quarterly Cash Flow from Operations (before customer advances) turning sustainably positive (> $100M/quarter).
  3. *Gross Power Margin Stability:* Quarterly cost of revenue confirming that gross power margins remain at or above 65–70%.
- **Reversal Condition:** Revisit the **WATCH / DEFER** recommendation and consider an upgrade to **INITIATE BUY** if: (1) market trading price corrects toward our fundamental valuation band ($12 to $18 per share), OR (2) IREN demonstrates verified customer acceptance and recognized billing for Horizons 2–4 scaling GAAP quarterly revenue above $375M ($1.5B ARR), positive operating cash flow generation before customer prepayments, and capital additions funded without dilutive share issuances exceeding 10%.
- **Model Refusal / Kill Conditions:** Valuation outputs are automatically refused if the pro-forma balance sheet fails double-entry articulation (Gap > $0.01M), if ending cash violates the $500.0M mandatory liquidity buffer, or if Gordon Growth capitalization is applied to a negative terminal cash flow.
