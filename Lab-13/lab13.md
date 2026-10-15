# FIN 439 Lab 13 — Portfolio Mandate Defense (Week 8)
**Client / Case Study:** Meridian Foundation Reserve ($100M Reserve Allocation)  
**Course:** FIN 43900 (Applied Financial Modeling & Corporate Valuation, Purdue University)  
**Student:** Elliot  
**Submission Date:** October 15, 2026  
**Assignment Reference:** Lab 13 — Portfolio Mandate Defense (Thursday Merit Checkout)  
**Deliverable Files:** [`mandate.py`](file:///c:/Users/ellio/Documents/FIN439/Lab-13/mandate.py) | [`lab13.md`](file:///c:/Users/ellio/Documents/FIN439/Lab-13/lab13.md)  
**GitHub Remote Repository:** [`river313/IREN-research`](https://github.com/river313/IREN-research)  
**Direct GitHub Deliverable Links:**
- Python Mandate Checker: [`Lab-13/mandate.py`](https://github.com/river313/IREN-research/blob/main/Lab-13/mandate.py)
- Defense Report & Mandate Audit: [`Lab-13/lab13.md`](https://github.com/river313/IREN-research/blob/main/Lab-13/lab13.md)

---

## 1. Executive Summary

In institutional portfolio management, a quantitative optimizer is only as sound as the mandate rules that bound its search space. **Lab 13** bridges the gap between qualitative client intent and deterministic algorithmic governance. Specifically, we operationalize the ten verbal instructions ($S1$–$S10$) issued by the Chief Investment Officer (CIO) of the **Meridian Foundation** for its **$100 million reserve fund** into programmable, automated constraint checks before any asset allocation optimization is performed.

```mermaid
flowchart TD
    CIO["Client / CIO Verbal Statements<br>(S1 to S10)"] --> Filter{"Institutional Mandate Filter<br>(Categorization)"}
    Filter --> Hard["Hard Constraints<br>(Sum=100%, Long-Only, Reserve, Liquidity, Issuer)"]
    Filter --> Obj["Objectives & Policy Benchmark<br>(CPI + 4%, 60/40 Benchmark)"]
    Filter --> Unver["Unverifiable / Missing<br>(S9 Loss Cap, S10 Optimization Target)"]
    
    Hard --> Checker["Deterministic Python Engine<br>(mandate.py)"]
    Obj --> Suitability["Fiduciary Suitability Assessment<br>(Portfolio Construction)"]
    Unver --> Question["Formal CIO Inquiry<br>(Blocks Mathematical Optimization)"]
    
    Checker --> CandidateA["Candidate A: Pass (0 fails)"]
    Checker --> CandidateB["Candidate B: FAIL (3 fails)"]
    Checker --> CandidateC["Candidate C: FAIL (1 fail)"]
    Checker --> CandidateD["Candidate D: Mechanical Pass (0 fails)"]
    
    CandidateD --> Suitability
    Suitability --> RejectD["Reject D: Fiduciary Mismatch<br>(Violates S4 Benchmark & S9 Tail Risk)"]
```

### Key Analytical Findings:
1. **Dynamic Reserve Minimum:** The mandate requires funding twelve months (4 quarters) of quarterly cash distributions ($0.75M per quarter) from a $100.0M reserve, establishing a non-negotiable minimum reserve-eligible allocation of **3.0%** ($3.0M) in cash or daily-liquid government paper.
2. **Candidate Portfolio Verification:**
   - **Candidate A** passes every checkable rule (Reserve = 14.0%, Liquidity = 100.0%, Issuer = 0.0%, Long-only min = 0.0%, Sum = 100.0%).
   - **Candidate B** fails **3 rules**: Reserve allocation is deficient (1.0% vs. 3.0% required), 5-day liquidity is breached (85.0% vs. 90.0% required due to a 15.0% allocation to a 90-day private real estate fund), and single-company concentration is violated (9.0% vs. 8.0% limit across aggregated Acme Corp stock and bonds).
   - **Candidate C** fails **1 rule**: Reserve allocation is deficient (2.0% vs. 3.0% required), while satisfying liquidity (100.0%) and the single-company ceiling (8.0%).
3. **Negative-Weight Probe Test:** Inserting an unauthorized short position in Candidate A (Cash = -2.0%, Global Equity = 64.0%) successfully triggered a `FAIL` on the long-only test (-2.0%), preserved the reserve pass at 10.0%, and verified the integrity of the diagnostic engine before original weights were restored.
4. **Adversarial Mandate Defense (Candidate D):** We constructed Candidate D (Cash 3.0%, Global Equity Index Fund 97.0%), which achieves 100% mechanical compliance across every automated check, yet represents an egregious fiduciary failure that the CIO must reject under Statement S4 (massive benchmark tracking error vs. 60/40) and Statement S9 (unacceptable tail-risk probability of exceeding a 10% calendar-year loss).
5. **The Optimization Blocker:** Optimization cannot mathematically proceed until the CIO answers **one critical question**: *How is the Statement S9 calendar-year 10% loss limit statistically formulated (i.e., ex-ante VaR confidence level and horizon), and what is the contractual breach/cure protocol if a market drawdown exceeds 10%?*

---

## 2. Meridian Foundation Mandate Overview

The Meridian Foundation manages an institutional reserve of **$100.0 million** designed to buffer operating commitments, support regular philanthropic disbursements, and generate real purchasing-power growth over an intermediate-to-long horizon. 

### Mandate Parameters & Operating Baseline
- **Reserve Portfolio Size:** $100.0 million.
- **Quarterly Outflow Commitment:** $0.75 million ($3.0 million annually).
- **Mandated Cash Buffer:** Twelve months of payouts held exclusively in cash or daily-liquid sovereign securities.
- **Strategic Policy Benchmark:** 60% Global Equities, 40% U.S. Investment-Grade Bonds.
- **Investment Horizon:** Seven years with annual rebalancing.
- **Long-Only Requirement:** Absolute prohibition on financial leverage, margin borrowing, short sales, and derivative contracts.
- **Single Corporate Issuer Concentration Ceiling:** 8.0% maximum aggregate exposure per corporate entity (combining equity and debt instruments). Cash, U.S. Treasuries, and diversified pooled funds are explicitly exempt.
- **Liquidity Mandate:** Minimum 90.0% of portfolio value redeemable within five business days.

---

## 3. Investment Policy Statement (IPS) Governance Framework

In accordance with institutional standards established by the CFA Institute, an **Investment Policy Statement (IPS)** serves as the governing charter between the asset owner (the foundation board) and the investment manager. An IPS systematically translates client circumstances into two primary sections:

1. **Objectives:**
   - **Return Objective:** Quantifies the target required to meet liabilities, preserve capital, and overcome inflation and fees.
   - **Risk Tolerance:** Specifies the client's willingness and objective ability to bear volatility, drawdown risk, and tracking error.
2. **Constraints (The TTLLU Framework):**
   - **Time Horizon (T):** The multi-year duration over which capital is deployed and evaluated.
   - **Taxes (T):** Tax status (foundations are typically tax-exempt under IRC §501(c)(3), though subject to excise taxes on net investment income).
   - **Liquidity Requirements (L):** Anticipated cash disbursements and emergency liquidity buffers.
   - **Legal and Regulatory (L):** Fiduciary standards such as the Uniform Prudent Management of Institutional Funds Act (UPMIFA) and statutory prohibitions against speculative leverage.
   - **Unique Circumstances (U):** Client-specific preferences, ethical/ESG screens, asset class restrictions, or customized governance controls.

### Mapping Meridian Foundation Statements to the IPS Architecture

```mermaid
classDiagram
    class InvestmentPolicyStatement {
        +Return Objectives
        +Risk Tolerance
        +Time Horizon
        +Liquidity Constraints
        +Legal & Regulatory
        +Unique Governance
    }
    class ReturnObjectives {
        +S2: CPI + 4.0% Net Rolling 5-Yr
        +S4: 60/40 Strategic Benchmark
    }
    class RiskTolerance {
        +S4: 60/40 Risk Profile
        +S9: Calendar-Year Loss Aspiration
    }
    class Constraints {
        +S1: 7-Year Horizon & Annual Rebalance
        +S3: 12-Mo Payout Reserve ($3.0M / 3.0%)
        +S5: Long-Only / No Derivatives / No Borrowing
        +S6: 8% Single Corporate Issuer Ceiling
        +S7: 25% Annual Turnover Limit
        +S8: 90% Liquid within 5 Business Days
        +S10: Missing Optimization Function
    }
    InvestmentPolicyStatement --> ReturnObjectives
    InvestmentPolicyStatement --> RiskTolerance
    InvestmentPolicyStatement --> Constraints
```

---

## 4. Classification & Financial Audit of Statements S1–S10

Before writing a single line of execution code, an analyst must dissect every client statement to determine whether it represents an actionable mathematical constraint, a high-level target, a subjective preference, or an unverifiable assertion.

| Statement | Exact Verbal Statement from CIO | Mandate Category | IPS Component | Actionable Checker Status | Analytical & Financial Rationale |
|---|---|---|---|---|---|
| **S1** | *"Horizon seven years; annual rebalancing."* | **Hard constraint** | Time Horizon & Governance | Operational Rule | Defines a discrete 7-year multi-period evaluation window and imposes a governance rule restricting portfolio rebalancing to an annual cycle. |
| **S2** | *"Objective: CPI + 4% a year, net of costs, over rolling five-year periods."* | **Objective** | Return Objective | Performance Hurdle | Quantifies the required real return hurdle necessary to preserve the purchasing power of the endowment against inflation while sustaining a 3.0% distribution yield plus operating expenses. |
| **S3** | *"Pays out $0.75 million every quarter; twelve months of payouts held in cash or daily-liquid government securities."* | **Hard constraint** | Liquidity Constraint | **Checkable Rule** | Establishes a mandatory cash-reserve floor: $4 \times \$0.75\text{M} = \$3.0\text{M}$ ($3.0\%$ of $\$100\text{M}$), restricted exclusively to reserve-eligible cash and Treasuries. |
| **S4** | *"Benchmark: 60% global equities, 40% U.S. investment-grade bonds."* | **Objective** | Policy Benchmark / Risk | Allocation Guidepost | Specifies the strategic asset allocation reference portfolio against which active risk, beta, and tracking error must be measured and evaluated. |
| **S5** | *"Long-only: no borrowing, short sales or derivatives."* | **Hard constraint** | Legal & Regulatory | **Checkable Rule** | Imposes non-negativity bounds on all asset weights ($w_i \ge 0$) and strictly forbids synthetic leverage, margin borrowing, and non-linear derivative instruments. |
| **S6** | *"No single issuer above 8%."* | **Hard constraint** | Unique / Concentration | **Checkable Rule** | Statutory concentration ceiling capping aggregate corporate exposure across debt and equity classes at 8.0%. Cash, Treasuries, and pooled funds are exempt. |
| **S7** | *"Annual turnover at most 25% without committee approval."* | **Hard constraint** | Operational Governance | Execution Filter | Restricts annualized portfolio churn to $\le 25\%$ to control transaction costs and bid-ask drag; requires explicit Investment Committee sign-off for exceptions. |
| **S8** | *"At least 90% redeemable within five business days."* | **Hard constraint** | Liquidity Constraint | **Checkable Rule** | Mandates that $\ge 90.0\%$ of aggregate portfolio value be convertible to cash within $T+5$ business days, capping illiquid alternative investments at $\le 10.0\%$. |
| **S9** | *"The reserve cannot have a calendar-year loss greater than 10%." No measure, no breach rule.* | **Unverifiable promise** | Risk Tolerance (Ambiguous) | **Untestable Flag** | Lacks an ex-ante statistical definition (confidence level, VaR horizon) and provides no operational protocol for market drawdowns. Must NOT be tested as a deterministic constraint. |
| **S10** | *"No sector, ESG, tax or home-bias preference; nobody has said what the pilot should optimize."* | **Missing** | Optimization Specification | Missing Parameter | Formally notes the absence of secondary preference screens, but critically reveals that the mathematical objective function (e.g., maximize Sharpe, minimize tracking error) is entirely missing. |

### Critical Clarification on Statement S9
Statement S9 is categorized as an **unverifiable promise** rather than a hard constraint. In public asset markets, an absolute guarantee of zero losses exceeding 10% over any calendar year is mathematically impossible when holding equities, unless the portfolio is 100% invested in short-duration sovereign bills. Because the CIO failed to specify an ex-ante probabilistic risk metric (e.g., $95\%$ 1-year Value-at-Risk $\le 10\%$) or an ex-post breach policy (e.g., mandatory de-risking triggers or cure periods), hardcoding this statement into a software checker would represent analytical malpractice. It is flagged as `"requires CIO clarification"` and deliberately excluded from mechanical evaluation.

---

## 5. Holdings Universe & Candidate Portfolio Weights

The asset universe comprises eight distinct instruments spanning cash, sovereign debt, diversified public funds, illiquid private assets, and single-company corporate securities.

### Mandate Holdings Universe

| Holding | Issuer | Business Days to Redeem | Reserve-Eligible | Exempt from Issuer Limit? | Liquidity Assessment ($T \le 5$ Days) |
|---|---|---:|:---:|:---:|:---:|
| **Cash** | None | 0 | **Yes** | Yes (Exempt) | Fully Liquid ($T+0$) |
| **Treasury bills** | U.S. Treasury | 1 | **Yes** | Yes (Exempt) | Fully Liquid ($T+1$) |
| **Treasury 10-year note** | U.S. Treasury | 1 | **Yes** | Yes (Exempt) | Fully Liquid ($T+1$) |
| **Global equity index fund** | Diversified fund | 2 | No | Yes (Exempt) | Liquid ($T+2$) |
| **Investment-grade bond fund** | Diversified fund | 3 | No | Yes (Exempt) | Liquid ($T+3$) |
| **Private real estate fund** | Diversified fund | 90 | No | Yes (Exempt) | **Illiquid ($T+90 > 5$)** |
| **Acme Corp bonds** | Acme Corp | 4 | No | **No (Corporate)** | Liquid ($T+4$) |
| **Acme Corp stock** | Acme Corp | 1 | No | **No (Corporate)** | Liquid ($T+1$) |

### Candidate Allocation Weights (Percent of Portfolio)

| Holding | Candidate A (%) | Candidate B (%) | Candidate C (%) | Candidate D (%) |
|---|---:|---:|---:|---:|
| Cash | 2.0 | 1.0 | 1.0 | 3.0 |
| Treasury bills | 2.0 | 0.0 | 1.0 | 0.0 |
| Treasury 10-year note | 10.0 | 0.0 | 0.0 | 0.0 |
| Global equity index fund | 60.0 | 55.0 | 70.0 | 97.0 |
| Investment-grade bond fund | 26.0 | 20.0 | 20.0 | 0.0 |
| Private real estate fund | 0.0 | 15.0 | 0.0 | 0.0 |
| Acme Corp bonds | 0.0 | 5.0 | 0.0 | 0.0 |
| Acme Corp stock | 0.0 | 4.0 | 8.0 | 0.0 |
| **Total Portfolio Weight** | **100.0%** | **100.0%** | **100.0%** | **100.0%** |

---

## 6. Computational Architecture of `mandate.py`

The evaluation engine implemented in [`Lab-13/mandate.py`](file:///c:/Users/ellio/Documents/FIN439/Lab-13/mandate.py) operates using Python's standard library. All calculations are dynamically derived from the editable parameters at the top of the file without hardcoding intermediate or final outputs.

### Mathematical Formulation of Mechanical Constraints

1. **Reserve Minimum Threshold:**
   $$\text{Reserve Minimum (\%)} = \frac{\text{Quarters to Cover} \times \text{Quarterly Distribution}}{\text{Total Reserve Size}} \times 100$$
   $$\text{Reserve Minimum} = \frac{4 \times \$0.75\text{M}}{\$100.0\text{M}} \times 100 = 3.0\%$$

2. **Full Investment Constraint (Weights Sum to 100%):**
   $$\sum_{i=1}^n w_i = 100.0\% \quad \iff \quad \left|\sum_{i=1}^n w_i - 100.0\right| < 10^{-4}$$

3. **Long-Only Constraint (No Short Positions / Leverage):**
   $$\min_{i \in \{1,\dots,n\}} w_i \ge 0.0\%$$

4. **Reserve Liquidity Requirement:**
   $$\text{Reserve Weight} = \sum_{i \in \text{Reserve-Eligible}} w_i \ge 3.0\%$$
   $$\text{Eligible Universe} = \{\text{Cash}, \text{Treasury bills}, \text{Treasury 10-year note}\}$$

5. **Five-Business-Day Redemption Requirement:**
   $$\text{Liquid Share} = \sum_{i: \text{Days}_i \le 5} w_i \ge 90.0\%$$

6. **Single-Company Issuer Concentration Limit:**
   $$\text{Company Exposure}_j = \sum_{i \in \text{Securities of Issuer } j} w_i \le 8.0\% \quad \forall j \notin \text{Exempt Issuers}$$
   $$\text{Exempt Issuers} = \{\text{"none"}, \text{"U.S. Treasury"}, \text{"diversified fund"}\}$$

---

## 7. Audit & Verification of Portfolios A, B, and C

Running `mandate.py` executes each mathematical check and generates verified values that match the professor's known answers exactly.

### Verified Audit Results Table

| Constraint / Rule | Target Threshold | Candidate A | Candidate B | Candidate C | Candidate D |
|---|:---:|:---:|:---:|:---:|:---:|
| **Weights sum to 100** | $= 100.0\%$ | **100.0 pass** | **100.0 pass** | **100.0 pass** | **100.0 pass** |
| **Long-only (lowest weight)** | $\ge 0.0\%$ | **0.0 pass** | **0.0 pass** | **0.0 pass** | **0.0 pass** |
| **Reserve Requirement** | $\ge 3.0\%$ | **14.0 pass** | **1.0 FAIL** | **2.0 FAIL** | **3.0 pass** |
| **Redeemable in 5 Days** | $\ge 90.0\%$ | **100.0 pass** | **85.0 FAIL** | **100.0 pass** | **100.0 pass** |
| **Largest Single Company** | $\le 8.0\%$ | **0.0 pass** | **9.0 FAIL** | **8.0 pass** | **0.0 pass** |
| **Calendar-Year Loss** | Undefined | *requires CIO clarification* | *same* | *same* | *same* |
| **FINAL MANDATE VERDICT** | — | **passes every checkable rule** | **fails 3 rule(s)** | **fails 1 rule(s)** | **passes every checkable rule** |

### Detailed Failure Diagnoses:

- **Candidate A Analysis (PASS):**
  - *Weights Sum:* $2 + 2 + 10 + 60 + 26 = 100.0\%$ (`pass`).
  - *Long-Only:* Minimum allocation is $0.0\%$ across unused holdings (`pass`).
  - *Reserve:* Cash ($2.0\%$) + T-bills ($2.0\%$) + 10-Yr T-notes ($10.0\%$) = **14.0%** $\ge 3.0\%$ (`pass`). Provides $\$14.0\text{M}$ in liquid sovereign backing, exceeding the $\$3.0\text{M}$ requirement.
  - *Five-Day Liquidity:* All holdings have redemption windows $\le 3$ days. Liquid share = **100.0%** $\ge 90.0\%$ (`pass`).
  - *Issuer Limit:* Acme Corp exposure is **0.0%** $\le 8.0\%$ (`pass`).
  - *Verdict:* **Passes every checkable rule.**

- **Candidate B Analysis (FAILS 3 RULES):**
  - *Reserve Failure:* Holds only $1.0\%$ in Cash and $0.0\%$ in Treasuries. Total reserve-eligible weight is **1.0%** vs. $3.0\%$ required (`FAIL`). This leaves only $\$1.0\text{M}$ in guaranteed liquidity, failing to cover twelve months of payouts ($\$3.0\text{M}$).
  - *Liquidity Failure:* Allocates $15.0\%$ to Private Real Estate, which requires 90 business days to redeem. Redeemable within 5 days is $100.0\% - 15.0\% =$ **85.0%** vs. $90.0\%$ minimum (`FAIL`).
  - *Issuer Concentration Failure:* Allocates $5.0\%$ to Acme Corp bonds and $4.0\%$ to Acme Corp stock. Because both instruments represent claims against the same corporate entity, they aggregate to **9.0%** vs. $8.0\%$ maximum (`FAIL`).
  - *Verdict:* **Fails 3 rule(s).**

- **Candidate C Analysis (FAILS 1 RULE):**
  - *Reserve Failure:* Holds $1.0\%$ in Cash and $1.0\%$ in T-bills. Total reserve-eligible weight is **2.0%** vs. $3.0\%$ required (`FAIL`). Deficit of $\$1.0\text{M}$ below the 1-year payout requirement.
  - *Issuer Compliance:* Allocates $8.0\%$ to Acme Corp stock and $0.0\%$ to Acme Corp bonds. Total issuer exposure is exactly **8.0%** $\le 8.0\%$ (`pass`).
  - *Liquidity Compliance:* Zero private real estate allocation yields **100.0%** 5-day liquidity (`pass`).
  - *Verdict:* **Fails 1 rule(s).**

---

## 8. Negative-Weight Validation (The Probe Test)

To prove that `mandate.py` functions as an authentic dynamic parser rather than returning hardcoded text, the assignment requires conducting a deliberate fault injection into Candidate A:
- **Cash weight** adjusted from $+2.0\%$ to **$-2.0\%$**.
- **Global equity fund weight** adjusted from $+60.0\%$ to **$+64.0\%$**.
- All other allocations remain untouched.

### Mathematical Pre-Calculation of Probe:
- Total weight: $(-2.0) + 2.0 + 10.0 + 64.0 + 26.0 = \mathbf{100.0\%}$ (Preserves sum check).
- Minimum weight: $\mathbf{-2.0\%} < 0.0\%$ (**Must trigger `FAIL` on long-only**).
- Reserve weight: $(-2.0) + 2.0 + 10.0 = \mathbf{10.0\%} \ge 3.0\%$ (**Must continue to `pass`**).
- Five-day liquidity: $\mathbf{100.0\%} \ge 90.0\%$ (Must continue to `pass`).
- Single-company issuer: $\mathbf{0.0\%} \le 8.0\%$ (Must continue to `pass`).
- Total checkable failures: Exactly **1 rule failed**.

### Console Output from Probe Execution:
```text
==============================================================================
MANDATE CHECKER PROBE TEST (Negative Weight Validation)
==============================================================================
Modifying Candidate A: Cash = -2.0%, Global equity index fund = 64.0%
Weights sum to 100:            100.0 pass
Long-only (lowest weight):     -2.0 FAIL
Reserve >= 3.0%:               10.0 pass
Redeemable in 5 days >= 90%:   100.0 pass
Largest single company <= 8%:  0.0 pass
Calendar-year loss:            requires CIO clarification
Verdict:                       fails 1 rule(s)

Probe Verification Status: CONFIRMED (Behaves exactly as expected)
==============================================================================
```

### Verification Confirmation:
The probe test executed with 100% precision: the long-only rule failed at $-2.0\%$, the reserve rule passed at $10.0\%$, and no other rules were corrupted. As instructed by the professor, the original weights for Candidate A (Cash = $2.0\%$, Global Equity = $60.0\%$) were restored immediately following verification.

---

## 9. Adversarial Mandate Attack (Portfolio D Analysis)

To test the resilience of mandate defense, we construct **Candidate D**, an adversarial portfolio designed to pass every mechanical check in `mandate.py` while exposing a severe fiduciary violation that the Meridian Foundation CIO would immediately reject.

### Portfolio D Specification:
- **Cash:** $3.0\%$
- **Treasury bills:** $0.0\%$
- **Treasury 10-year note:** $0.0\%$
- **Global equity index fund:** $\mathbf{97.0\%}$
- **Investment-grade bond fund:** $0.0\%$
- **Private real estate fund:** $0.0\%$
- **Acme Corp bonds:** $0.0\%$
- **Acme Corp stock:** $0.0\%$

### Computational Evaluation in `mandate.py`:
- *Weights sum to 100:* $3.0 + 97.0 = \mathbf{100.0\%}$ (`100.0 pass`)
- *Long-only:* Minimum weight is $\mathbf{0.0\%}$ (`0.0 pass`)
- *Reserve Minimum:* Cash is $\mathbf{3.0\%} \ge 3.0\%$ (`3.0 pass`)
- *Five-Day Liquidity:* Cash ($T+0$) + Global Equities ($T+2$) = $\mathbf{100.0\%} \ge 90.0\%$ (`100.0 pass`)
- *Single-Company Issuer:* Acme Corp = $\mathbf{0.0\%} \le 8.0\%$ (`0.0 pass`)
- *Checkable Failures:* **0 failures**
- *Mechanical Verdict:* **`passes every checkable rule`**

### Sceptical Risk Manager Assessment: Why the CIO Must Reject Portfolio D

```mermaid
flowchart LR
    PortD["Candidate D<br>(97% Equity / 3% Cash)"] --> Mechanical["Mechanical Checker<br>(mandate.py)"]
    Mechanical --> Pass["Passes All 5 Rules<br>(0 Fails)"]
    
    PortD --> Fiduciary["Fiduciary Risk Review<br>(Institutional CIO / Risk Manager)"]
    Fiduciary --> V_S4["Violates Statement S4<br>Benchmark Tracking Error<br>Equity Active Share: +37.0%<br>Bond Active Share: -40.0%"]
    Fiduciary --> V_S9["Violates Statement S9<br>Tail Risk Exposure<br>Annual Equity Vol: ~17%<br>Pr(Loss > 10%): High (~28%)"]
    
    V_S4 --> Reject["REJECT PORTFOLIO D<br>Gross Unsuitability"]
    V_S9 --> Reject
```

The objection against Portfolio D is irrefutable and decided by **two explicit CIO statements**:

1. **Direct Violation of Statement S4 (Strategic Benchmark Mismatch):**  
   Statement S4 establishes a benchmark of **60% global equities and 40% U.S. investment-grade bonds**. Candidate D holds **97% equities and 0% fixed income**. This creates an active equity overweight of **+37.0%** and an active fixed income underweight of **-40.0%**. In institutional asset management, a tracking error of this magnitude ($\approx 6.5\text{--}8.0\%$ annualized tracking error) represents an unauthorized asset allocation bet that completely abandons the board-approved strategic asset allocation.
2. **Gross Violation of Statement S9 (Tail Risk & Drawdown Breach):**  
   Statement S9 articulates that *"the reserve cannot have a calendar-year loss greater than 10%."* Global equities exhibit an annualized volatility of $16\text{--}18\%$. Historically, global equities have suffered severe calendar-year drawdowns (e.g., $-37\%$ in 2008, $-18\%$ in 2022). With a $97\%$ equity allocation, the ex-ante probability of suffering a calendar-year decline in excess of $-10\%$ is approximately **$25\text{--}30\%$** in any given year. A single systemic market shock would impair the foundation's core capital and jeopardize its distribution commitments, directly violating the CIO's risk threshold.

**Conclusion of Attack:** Portfolio D confirms that mechanical rule compliance is blind to portfolio beta, benchmark tracking error, and tail-risk exposure.

---

## 10. The Critical Unanswered CIO Question

Before an analyst can write an optimization algorithm (such as mean-variance optimization, quadratic programming, or risk-parity), the client must resolve the ambiguity residing in Statements S9 and S10.

### The Single Blocking Question for the CIO:

> **"How is the Statement S9 calendar-year 10% maximum loss limit statistically operationalized (specifically, what confidence level and horizon for Value-at-Risk or Conditional VaR, such as 95% or 99% 1-year VaR), and what is the mandatory operational protocol or breach rule if market declines exceed 10%?"**

### The Answer That Fundamentally Changes Portfolio Design:

The CIO's answer to this question completely dictates the feasible asset allocation space:

- **Scenario 1 — Absolute Zero-Tolerance Hard Cap ($VaR_{100\%} \le 10.0\%$):**  
  If the CIO asserts that under no circumstances—even in a severe market crisis—may the portfolio drop $>10\%$, then **equities must be drastically reduced or excluded entirely**. Because equities have an unhedged downside exceeding $-30\%$, the maximum allowable equity weight would drop to $\le 15\text{--}20\%$, paired with short-duration Treasuries and cash. However, this conservative allocation would mathematically guarantee failure to achieve **Statement S2 (CPI + 4.0% net return)** over rolling 5-year periods. The CIO would be forced to reconcile an impossible conflict between risk and return.
- **Scenario 2 — Standard Institutional Probabilistic Risk Budget (e.g., $95\%$ 1-Year $VaR \le 10.0\%$):**  
  If the CIO clarifies that S9 represents an ex-ante probabilistic risk constraint (e.g., a $5\%$ tail probability of losing $>10\%$ in a 12-month period), the optimizer can comfortably support a diversified **60% equity / 40% fixed income** allocation. The optimizer can then solve for weights that minimize tracking error to S4 while targeting the CPI + 4.0% return hurdle in S2.
- **Breach Protocol Implications:**  
  If a breach occurs, does the mandate require a forced liquidation to cash at the market trough (locking in losses), or does it mandate an Investment Committee review with a multi-quarter cure period? Without this operational protocol, automated rebalancing algorithms cannot be programmed.

---

## 11. Mechanical Compliance vs. Fiduciary Suitability

A central finding of this mandate defense is that **a portfolio can satisfy every checkable mechanical rule and still be completely wrong for the client.**

```mermaid
flowchart TD
    subgraph Mechanical ["Mechanical Constraint Engine (mandate.py)"]
        R1["Weights Sum = 100%"]
        R2["Long-Only (Min >= 0%)"]
        R3["Reserve >= 3.0%"]
        R4["5-Day Liquidity >= 90%"]
        R5["Single Issuer <= 8%"]
    end
    
    subgraph Fiduciary ["Fiduciary & Economic Suitability (IPS Governance)"]
        F1["Asset-Liability Matching (ALM)"]
        F2["Target Real Return Feasibility (CPI + 4%)"]
        F3["Benchmark Tracking Error Control (S4)"]
        F4["Multi-Asset Volatility & Tail-Risk Budget (S9)"]
        F5["Governance & Rebalancing Friction (S1/S7)"]
    end
    
    Mechanical -.->|"Necessary but Insufficient"| Fiduciary
```

### Key Dimensions of the Divergence:

1. **Boundary Checking vs. Joint Probability Distributions:**  
   Code checks isolated linear inequalities ($w_i \ge 0$, $\sum w_i = 1$, $w_{\text{Acme}} \le 8\%$). However, financial risk is driven by the covariance matrix ($\Sigma$) of asset returns. A portfolio of $97\%$ equities and $3\%$ cash satisfies every linear boundary, but its joint distribution creates massive tail risk that violates the client's fiduciary risk capacity.
2. **Asset-Liability Matching (ALM) vs. Nominal Liquidity:**  
   The checker confirms that $90\%$ of the portfolio can be converted to cash in five days. However, liquidity is economically worthless if the assets must be sold at a $30\%$ discount during a market crash to fund mandatory quarterly payouts. True fiduciary management aligns asset cash flows with liabilities so that distributions are covered by yield and maturities rather than forced asset liquidations.
3. **Legal Permissibility vs. Mandate Alignment:**  
   Candidate D is legally permissible under the narrow rules of `mandate.py`. Yet, presenting Candidate D to the board as an institutional reserve portfolio would breach the prudent investor rule because it ignores the foundation's stated benchmark (S4) and risk profile.

---

## 12. Reflection & Analytical Judgments

> [!NOTE]
> **Student Review Flag:** The analytical judgments below represent an objective synthesis of institutional mandate governance. Elliot should review these responses prior to oral defense or quiz submission.

### 1. Why a Portfolio Can Pass Every Checkable Rule and Still Be Wrong
As proven by Candidate D, mechanical checkers verify **permissibility boundaries**, not **investment suitability**. A mechanical checker treats asset weights in isolation or in simple linear sums. It does not evaluate portfolio volatility, expected return against liabilities, correlation structures, or active risk relative to the policy benchmark. A portfolio holding 97% equities and 3% cash passes sum, long-only, reserve minimum, 5-day liquidity, and single-issuer concentration rules with 100% precision. Yet, it exposes the Meridian Foundation to catastrophic equity drawdowns that would violate the board's core objective of preserving capital and supporting uninterrupted philanthropic operations.

### 2. The S1–S10 Statement Classification of Greatest Ambiguity
The statement presenting the greatest analytical challenge is **Statement S9** (*"The reserve cannot have a calendar-year loss greater than 10%. No measure, no breach rule"*). 
- *Why it is ambiguous:* In casual conversation, clients frequently phrase risk tolerance as an absolute negative guarantee ("I cannot lose more than X%"). If taken literally as a deterministic hard constraint, it would preclude investing in global equities or corporate credit, making the return objective in S2 (CPI + 4.0%) impossible.
- *Why it cannot be hardcoded:* Without an ex-ante statistical definition (such as a 1-year 95% or 99% Value-at-Risk) and an explicit breach/cure rule, an algorithm cannot evaluate compliance. Classifying S9 as an **unverifiable promise** prevents premature and invalid optimization while forcing a necessary governance dialogue with the CIO.

---

## 13. Preparation for Week 9: Project 2 Mandate Draft

In preparation for **Project 2 (Portfolio Optimization & Construction)** starting in Week 9, the institutional mandate below is structured in the exact same format as the Meridian Foundation case. 

### Client Mandate: Clean Infrastructure & Digital Transition Reserve ($150M)

#### A. Client Profile & Institutional Context
The client is an institutional sustainability endowment dedicated to funding grid decarbonization and digital infrastructure modernization. The portfolio consists of a **$150.0 million capital reserve**.

#### B. Investment Objective
- **Return Target:** Achieve a net annualized return of **CPI + 4.5%** over rolling five-year periods to preserve real endowment purchasing power after funding distributions and administrative fees.
- **Strategic Policy Benchmark:** 65% MSCI World All-Country Equity Index, 35% Bloomberg Global Aggregate Bond Index.
- **Investment Horizon:** Ten-year horizon with semi-annual portfolio reviews and annual rebalancing.

#### C. Hard Operational Constraints
1. **Full Investment & Long-Only:** Portfolio weights must sum to exactly 100.0%. Long-only allocation only; no short sales, borrowing, margin leverage, or uncovered derivatives.
2. **Liquidity Distribution Reserve:** The fund pays out **$1.125 million every quarter** ($4.50M annually). The mandate requires holding **sixteen months (5 quarters)** of payouts ($5.625M, or **3.75%** of portfolio value) exclusively in cash, Treasury bills, or sovereign government bonds maturing within 12 months.
3. **Five-Business-Day Liquidity Window:** At least **85.0%** of the portfolio must be redeemable in cash within five business days to accommodate unannounced emergency capital grants.
4. **Single-Issuer Corporate Concentration Limit:** Aggregate exposure to any single non-government corporate issuer (debt plus equity) cannot exceed **7.0%**. Sovereign debt and diversified funds are exempt.
5. **Annual Turnover Ceiling:** Annualized portfolio turnover must not exceed **20.0%** without prior authorization from the Investment Committee.

#### D. Proposed Client Assumptions [Subject to Formal Client Confirmation]
> [!IMPORTANT]
> The following items are proposed assumptions drafted for modeling purposes and are explicitly labeled as proposed client assumptions rather than verified contractual facts:
> - *Assumption 1 (Target Inflation Baseline):* Projected long-term CPI is assumed to be 2.50% annualized, setting the nominal net return hurdle at 7.00% (2.50% CPI + 4.50% real).
> - *Assumption 2 (Ex-Ante Risk Budget):* The client's drawdown aversion is modeled as an ex-ante 1-year 95% Value-at-Risk ($VaR_{95\%}$) ceiling of **12.0%**, paired with a maximum expected annualized portfolio volatility of **11.5%**.
> - *Assumption 3 (Permissible Asset Universe):* Liquid global equities, green corporate bonds, infrastructure debt funds, sovereign Treasuries, and clean-power real asset trusts.

#### E. The One Critical Question for the Client Before Optimizing
> **"Does the board's mandate permit the tactical use of exchange-traded interest rate and equity index futures strictly for portfolio hedging and duration management during market crises, or does the 'no derivatives' rule prohibit all exchange-traded hedging instruments without exception?"**
> - *Consequence:* If hedging is prohibited, downside protection must be achieved purely through static cash/Treasury allocations, reducing Sharpe efficiency. If exchange-traded hedging is permitted, the optimizer can utilize dynamic duration overlays to preserve equity exposure while defending capital during market downturns.

---

## 14. Verification & Submission Manifest

### Verification Checklist:
- [x] Python program [`mandate.py`](file:///c:/Users/ellio/Documents/FIN439/Lab-13/mandate.py) runs cleanly with standard library only.
- [x] Reserve minimum computed directly from inputs ($4 \times 0.75 / 100 = 3.0\%$).
- [x] All candidate outputs match known answers: Candidate A passes all; B fails 3; C fails 1.
- [x] Negative-weight probe test executed, verified (Cash = -2.0% fails long-only at -2.0%, reserve passes at 10.0%), and original inputs restored.
- [x] Candidate D constructed, passes mechanical checks, and evaluated against Statements S4 and S9.
- [x] Statements S1–S10 classified with financial rationales; S9 not tested mechanically; S10 identified as missing.
- [x] The one critical blocking CIO question identified with analytical consequences.
- [x] Distinction between mechanical compliance and fiduciary suitability explained.
- [x] Project 2 client mandate drafted in identical shape with proposed assumptions clearly labeled.
- [x] Report author verified: **Elliot** (never Elliott).
- [x] Committed and pushed to GitHub repository [`river313/IREN-research`](https://github.com/river313/IREN-research).

---
*Report completed and certified by Elliot for FIN 43900.*
