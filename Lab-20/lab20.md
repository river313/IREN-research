# FIN 439 Lab 20 — Project 2 Readiness Checkout

**Course:** FIN 43900 (Applied Financial Modeling & Corporate Valuation, Daniels School of Business, Purdue University)  
**Student:** Elliot  
**Lab Repository:** [https://github.com/river313/IREN-research](https://github.com/river313/IREN-research)  
**Project 2 Repository:** [https://github.com/river313/Project-2](https://github.com/river313/Project-2)  
**Client / Mandate:** Meridian Foundation Reserve ($100.0M Total Capital Base)  
**Deliverable File:** `Lab-20/lab20.md`  
**Status:** In Progress — Pre-Class Readiness Audit & Code Verification Complete; In-Class Partner Cold Run, Specific Scenario Prediction Precommit, and Code Defense Pending  

---

> ### Required Opening Disclosures
> 1. **AI Use Disclosure:** This readiness checkout report and portfolio modeling system were prepared with the assistance of artificial intelligence tools (Google Gemini / Antigravity). All architectural decisions, mathematical checks, financial interpretations, and final committee recommendations are the independent work and responsibility of Elliot.
> 2. **Regulatory & Academic Disclaimer:** This analysis is an educational demonstration prepared for FIN 43900 at Purdue University and does not constitute formal investment advice or a professional fiduciary solicitation.

---

## 1. D — The Core Readiness Question

> **"Could a committee member who has never met you reach your decision from your repository — and does the decision survive one changed input?"**

This document audits the readiness of the Project 2 repository ([`river313/Project-2`](https://github.com/river313/Project-2)) to satisfy the stranger test for the FIN 439 Lab 20 completion checkout. Every financial metric in this report is extracted directly from verified application code, executed Python test suites, and official SEC/FRED disclosures without fabrication or simulated human results.

---

## 2. R — What a Stranger Needs: Repository Readiness Audit

The table below audits the Project 2 repository against the six required manifest elements defined on the Lab 20 handout and the Project 2 specification page:

| Manifest Part | Course Requirement ("Ready Means") | Repository Evidence & Verification Status | Verified Disposition |
|---|---|---|:---:|
| **The Tool** | A teammate moves one control and reads the mandate verdict | • Interactive Streamlit application in [`app.py`](https://github.com/river313/Project-2/blob/main/app.py) (761 lines, 5 functional tabs).<br>• Controls for expected returns, volatilities, correlations, reserve floor, and advisory fee drag.<br>• Dynamic mandate compliance verdict banner and Plotly risk-return charts. | **PASS (READY)** |
| **Repository README** | A README with the one command that produces your result | • [`README.md`](https://github.com/river313/Project-2/blob/main/README.md) documents master reproduction command: `python run_tests.py` and launch command: `streamlit run app.py`.<br>• Local environment fallback documented: `& "..\Python-3.13.15\python.exe" run_tests.py`. | **PASS (READY)** |
| **Visible Output** | The decision numbers readable on GitHub without running anything | • Fully readable in [`visible_output.json`](https://github.com/river313/Project-2/blob/main/visible_output.json) on GitHub.<br>• Key metrics replicated in Markdown tables in [`README.md`](https://github.com/river313/Project-2/blob/main/README.md).<br>• Primary Candidate: Gross Return **6.66%**, Net Return **6.51%**, Volatility **10.07%**, Reserve **20.0%**. | **PASS (READY)** |
| **Decision Memo** | `docs/decision-memo.md` has the same numbers, dates, and conditions as the output | • Verified in draft framework [`docs/decision-memo.md`](https://github.com/river313/Project-2/blob/main/docs/decision-memo.md).<br>• Reconciled to $100.0M capital, CPI + 4.0% hurdle (6.50% net), 10.07% volatility, and 20.0% reserve floor. | **PASS (READY)** |
| **Validation & AI Use** | Baseline, mandate check, stress run, Locked Changed-Input Record | • Test suite [`run_tests.py`](https://github.com/river313/Project-2/blob/main/run_tests.py) passes 18/18 tests (100%).<br>• Pre-run prediction precommit locked in [`docs/validation-and-ai-use.md`](https://github.com/river313/Project-2/blob/main/docs/validation-and-ai-use.md) at commit `9ee860d`.<br>• Changed-input execution pending specific scenario precommit. | **PARTIAL (Phase 2 Pending)** |
| **Videos 1–3 & Transcripts** | Links work; each video answers its own question | • Listed in submission manifest [`project-submission-manifest-template.csv`](https://github.com/river313/Project-2/blob/main/project-submission-manifest-template.csv) rows 7–12 with pending URLs.<br>• To be recorded before final Project 2 deadline. | **UNRESOLVED / PENDING SUBMISSION** |

---

## 3. Verified Repository Financial Numbers and Calculations

All figures below reflect modeled capital market expectations audited directly from [`Project-2/modules/portfolio.py`](https://github.com/river313/Project-2/blob/main/modules/portfolio.py) and verified via [`Project-2/run_tests.py`](https://github.com/river313/Project-2/blob/main/run_tests.py).

### Master Portfolio Comparison Table

| Metric / Attribute | Portfolio A: Equal Weight | Portfolio B: Strategic 60/40 | Portfolio C: Gross Optimizer | Portfolio D: Net-Return Candidate |
|---|:---:|:---:|:---:|:---:|
| **Allocation (Bills / 10-Yr / IG / Eq)** | `[25%, 25%, 25%, 25%]` | `[0%, 0%, 40%, 60%]` | `[0%, 20%, 25%, 55%]` | `[0%, 20%, 20%, 60%]` |
| **Expected Gross Return** | $5.2000\%$ | $6.8000\%$ | $6.5100\%$ | $6.6600\%$ |
| **Sleeve Expense Drag** | $2.8\text{ bps}$ ($0.0275\%$) | $5.8\text{ bps}$ ($0.0580\%$) | $4.9\text{ bps}$ ($0.0485\%$) | $5.0\text{ bps}$ ($0.0500\%$) |
| **Net Return (Fund Fees Only)** | $5.1725\%$ | $6.7420\%$ | $6.4615\%$ | $6.6100\%$ |
| **Net Return (Fund + 10 bps Advisory)** | $5.0725\%$ | $6.6420\%$ | $6.3615\%$ | **$6.5100\%$** |
| **Annualized Volatility** | $5.2104\%$ ($5.21\%$) | $10.4618\%$ ($10.46\%$) | $9.4417\%$ ($9.44\%$) | **$10.0658\%$ ($10.07\%$)** |
| **Reserve-Eligible Allocation** | $50.00\%$ ($\ge 3.0\%$) | $0.00\%$ ($< 3.0\%$) | $20.00\%$ ($\ge 3.0\%$) | **$20.00\%$ ($\ge 3.0\%$)** |
| **Five-Day Liquidity** | $100.00\%$ ($\ge 90.0\%$) | $100.00\%$ ($\ge 90.0\%$) | $100.00\%$ ($\ge 90.0\%$) | **$100.00\%$ ($\ge 90.0\%$)** |
| **Max Single Corporate Issuer** | $0.00\%$ ($\le 8.0\%$) | $0.00\%$ ($\le 8.0\%$) | $0.00\%$ ($\le 8.0\%$) | **$0.00\%$ ($\le 8.0\%$)** |
| **Gross Hurdle Status ($\ge 6.50\%$)** | **FAIL** ($-130\text{ bps}$) | **PASS** ($+30\text{ bps}$) | **PASS** ($+1\text{ bp}$) | **PASS** ($+16\text{ bps}$) |
| **Net Hurdle Status ($\ge 6.50\%$)** | **FAIL** ($-143\text{ bps}$) | **PASS** ($+14\text{ bps}$) | **FAIL** ($-14\text{ bps}$) | **PASS** ($+1\text{ bp}$) |
| **Hard Mandate Compliance** | **COMPLIANT** | **NON-COMPLIANT** (0% Reserve) | **COMPLIANT** | **COMPLIANT** |

*Fee Discrepancy Reconciliation:* `visible_output.json` serializes Portfolio C net return as $6.46\%$ (reflecting sleeve expenses only), whereas `app.py` applies the default $10.0\text{ bps}$ institutional advisory fee drag, resulting in $6.36\%$. For Portfolio D, net return with all fees included is $6.5100\%$, clearing the $6.50\%$ hurdle by exactly $1.0\text{ basis point}$.

---

## 4. I — Independent Partner Cold Run

> **Course Requirement (Minutes 5–25):**  
> Send your partner your repository link and nothing else. They open it in their own folder, follow only the README, and record their exact terminal experience.

### Status: UNRESOLVED / PENDING LIVE IN-CLASS PARTNER EXECUTION
*In accordance with course anti-fabrication standards, no partner names, conversations, or simulated classmate experiences are recorded.*

### Developer / Automated Environment Baseline Verification
To verify technical reproducibility prior to in-class partner testing, an independent automated execution was run directly from terminal:
- **Execution Command Attempted:** `& "..\Python-3.13.15\python.exe" run_tests.py`
- **Elapsed Time:** **1.4 seconds**
- **First Failure:** **CLEAN RUN — NO FAILURE (0 errors)**
- **Automated Test Results:** **18 of 18 unit tests passed (100.0%)**
- **Location of Output:** Terminal stdout and serialized [`visible_output.json`](https://github.com/river313/Project-2/blob/main/visible_output.json).

---

## 5. V — One Changed Input, Predicted First

### Pre-Run Prediction Audit (Commit `9ee860d`)
- **Pushed Commit Hash:** [`9ee860d61b2257f56be2ea1316ab5e2c0dee1010`](https://github.com/river313/Project-2/commit/9ee860d61b2257f56be2ea1316ab5e2c0dee1010)
- **Pre-Run Timestamp:** `2026-11-19T01:55:41Z` (`2026-11-18 20:55:41 -05:00`)
- **Location:** [`docs/validation-and-ai-use.md`](https://github.com/river313/Project-2/blob/main/docs/validation-and-ai-use.md), Section 2A.
- **Elliot's Verbatim Statement:**
  > *"I predict that when portfolio inputs change, the optimal portfolio weights will adjust based on the relationship between risk and return. If expected returns increase, I expect the portfolio to allocate more capital to those assets. If volatility increases, I expect the allocation to riskier assets to decrease. If liquidity decreases, I expect the investment to become less attractive because it will be harder to sell without additional costs. Overall, I predict that the investment decision will favor assets that provide higher expected returns with manageable risk and sufficient liquidity."*

### Honest Evaluation Against Rubric Criteria:
1. **Original Input & Units:** `8.00%` Global Equity Expected Return (recorded in markdown header).
2. **Changed Input & Units:** `7.50%` Global Equity Expected Return (recorded in markdown header).
3. **Direction of Financial Results:** **PARTIALLY SPECIFIED**. The text states general conditional principles ("if returns increase...", "if volatility increases..."), but does not forecast the specific direction of Meridian portfolio weights, net return, or volatility under the $8.00\% \rightarrow 7.50\%$ shock.
4. **Effect on Investment Decision:** **PARTIALLY SPECIFIED**. The statement predicts general asset favoring, but does not state whether this specific shock causes the committee to adopt, pilot, rebalance, or reject the candidate portfolio.
5. **Committed Before Testing:** **VERIFIED**. Commit `9ee860d` was pushed before any test run.

### Status: TEST HALTED PRIOR TO RUN
The changed-input scenario has **NOT** been run. To achieve 100% compliance with Lab 20 Section V, Elliot will independently add 2–3 specific sentences with AI closed stating expected directional impacts for this specific scenario prior to model rerun.

---

## 6. Code Explanation (Six Minutes, No AI)

> **Course Requirement (Minutes 40–46):**  
> Open the block of Project 2 code that produces your decision number. Explain it line by line to your partner.

- **Selected Code Block:** [`Project-2/modules/portfolio.py`, lines 270–385](https://github.com/river313/Project-2/blob/main/modules/portfolio.py#L270-L385) (`optimize_portfolio` function).
- **Core Decision Logic Explained:**
  1. Generates 1,771 long-only portfolio combinations using a course-mandated $5\%$ grid step ($\sum w_i = 100\%$, $w_i \ge 0\%$).
  2. Filters allocations against the return hurdle (`ret >= objective_rate`) and sovereign reserve floor (`reserve >= min_reserve`).
  3. Computes portfolio variance using the full covariance matrix: $\sigma_p = \sqrt{\mathbf{w}^T \mathbf{\Sigma} \mathbf{w}}$.
  4. Selects the qualifying allocation with the lowest annualized volatility.
  5. Implements an explicit refusal stop condition (`feasible=False`) if no portfolio qualifies.
- **Partner Interaction Status:** **UNRESOLVED / PENDING IN-CLASS LIVE PRESENTATION**.

---

## 7. E — Fix One Thing

### Status: PENDING IN-CLASS COLD RUN
*To be completed after classmate identifies an issue during the Tuesday cold run.*

### Documented Technical Environment Fix
- **Issue:** On systems where Python is not registered in the Windows launcher path, `python` or `py` returns `CommandNotFoundException` or `No installed Python found!`.
- **Fix Implemented:** Updated [`README.md`](https://github.com/river313/Project-2/blob/main/README.md) with explicit fallback syntax:
  ```powershell
  & "..\Python-3.13.15\python.exe" run_tests.py
  ```

---

## 8. Your Decision Line

> **One line, as the committee will hear it:**  
> State: *adopt, allocate to, rebalance, pilot, or reject*, with the condition that would reverse it.

> **"Approve a conditional pilot allocation to the Net-Return Optimized Portfolio (0.0% Treasury bills, 20.0% 10-year Treasuries, 20.0% investment-grade corporate bonds, 60.0% global equities) which models an expected net return of 6.51% (clearing the CPI + 4.0% hurdle by 1 basis point) and 10.07% volatility while meeting the 3.0% reserve floor and 90.0% five-day liquidity constraints; reversible to REJECT or REBALANCE if the investment committee rules that the return hurdle must be evaluated gross of advisory fees, if realized inflation increases the net hurdle above modeled portfolio return, or if downside stress testing demonstrates non-compliance with the 10.0% calendar-year loss restriction."**

---

## 9. Reflect

### Status: UNRESOLVED / PENDING IN-CLASS REFLECTION (Minutes 60–70)
*To be completed live with partner in class.*

### Pre-Class Technical Reflection:
1. **What automated verification revealed:** Coarse 5% grid search forces 16 pp higher Treasury allocation than necessary, creating an 18 bps volatility drag compared to fine-grid optimization. Furthermore, solving for gross return creates a 14 bps shortfall against the client's purchasing power mandate.
2. **What will not be touched before the deadline:** The core covariance risk engine, the deterministic Lab 13 mandate checker, and the verified 18 automated unit tests are strictly frozen.

---

## 10. Checkout — GitHub Verification Links

- **Lab 20 Document:** [`Lab-20/lab20.md`](https://github.com/river313/IREN-research/blob/main/Lab-20/lab20.md)
- **Project 2 Main Application:** [`Project-2/app.py`](https://github.com/river313/Project-2/blob/main/app.py)
- **Verification Test Suite:** [`Project-2/run_tests.py`](https://github.com/river313/Project-2/blob/main/run_tests.py)
- **Audited Output Snapshot:** [`Project-2/visible_output.json`](https://github.com/river313/Project-2/blob/main/visible_output.json)
- **Pre-Run Locked Commit:** [`Commit 9ee860d`](https://github.com/river313/Project-2/commit/9ee860d61b2257f56be2ea1316ab5e2c0dee1010)
- **Decision Memo:** [`Project-2/docs/decision-memo.md`](https://github.com/river313/Project-2/blob/main/docs/decision-memo.md)
- **Validation Record:** [`Project-2/docs/validation-and-ai-use.md`](https://github.com/river313/Project-2/blob/main/docs/validation-and-ai-use.md)
- **Point-in-Time Data Card:** [`Project-2/docs/data-card-dgs10.md`](https://github.com/river313/Project-2/blob/main/docs/data-card-dgs10.md)
- **Submission Manifest:** [`Project-2/project-submission-manifest-template.csv`](https://github.com/river313/Project-2/blob/main/project-submission-manifest-template.csv)
