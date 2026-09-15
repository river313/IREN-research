# FIN 439 Lab 07 — Comparable-Company Policy and Implied Range
**Case Study:** Asbury Automotive Group (ABG) and Candidate Peers (AutoNation, Group 1 Automotive)  
**Student:** Elliott  
**Course:** FIN 439  
**Date:** September 2026  

---

## 1. Executive Summary & Case Overview

This laboratory analyzes the application of **Comparable-Company Analysis (Comps)** using the Price-to-Earnings (P/E) multiple for **Asbury Automotive Group (ABG)** as of December 31, 2024, evaluated against two candidate franchised automotive retail peers: **AutoNation (AN)** and **Group 1 Automotive (GPI)**.

### Supplied Case Inputs

| Company / Role | Ticker | Dec 31, 2024 Closing Price | FY2024 GAAP Diluted EPS | Case Status / Qualification |
| :--- | :---: | :---: | :---: | :--- |
| **Asbury Automotive Group** | **ABG** | **$243.03** | **$21.50** | **Target Company** |
| AutoNation | AN | $169.84 | $16.92 | Candidate Peer (Pure-play US) |
| Group 1 Automotive | GPI | $421.48 | $36.81 | Qualified Candidate Peer (US + UK) |

*Data Source: Supplied FIN 439 Lab 07 case inputs (retrospective comparison pairing Dec 31, 2024 closing prices with subsequently reported FY2024 full-year GAAP diluted earnings).*

---

## 2. Quantitative Valuation & Benchmark Verification

The valuation engine (`pe_calculator.py`) was executed using the local Python environment (`.\Python-3.13.15\python.exe Lab-07\pe_calculator.py`). Full precision was maintained internally across all steps, with multiples displayed to six decimal places and per-share prices displayed to the nearest cent.

### Summary of Peer Multiples and Target Implied Prices

$$\text{P/E Multiple} = \frac{\text{Market Price per Share}}{\text{FY2024 GAAP Diluted EPS}}$$

1. **AutoNation (AN) P/E:**
   $$\frac{\$169.84}{\$16.92} = 10.037825\times$$

2. **Group 1 Automotive (GPI) P/E:**
   $$\frac{\$421.48}{\$36.81} = 11.450149\times$$

3. **Two-Peer Median P/E:**
   $$\text{Median}(10.037825\times, 11.450149\times) = \frac{10.03782506 + 11.45014942}{2} = 10.743987\times$$

4. **Asbury (ABG) Target Implied Valuation:**
   - **Minimum Implied Price (at AN multiple):**
     $$10.03782506\times \times \$21.50 = \$215.8132 \rightarrow \mathbf{\$215.81}$$
   - **Maximum Implied Price (at GPI multiple):**
     $$11.45014942\times \times \$21.50 = \$246.1782 \rightarrow \mathbf{\$246.18}$$
   - **Implied Range:** **\$215.81 to \$246.18**
   - **Target at Peer Median P/E:**
     $$10.74398724\times \times \$21.50 = \$230.9957 \rightarrow \mathbf{\$231.00}$$
   - **Target Actual Closing Price:** **\$243.03** (Actual trades at $11.303721\times$, which is $+5.21\%$ or $+\$12.03$ above the peer median implied price of $\$231.00$).

### Leave-One-Out Sensitivity Analysis

When peer sets are small, individual peer multiples exert substantial leverage on the median benchmark.

| Excluded Peer | Remaining Peer Set | Remaining Median P/E | Remaining Implied ABG Price | Dollar Change vs Full-Peer Median ($231.00) |
| :--- | :---: | :---: | :---: | :---: |
| **Remove GPI** (higher multiple) | AN | $10.037825\times$ | **$215.81** | **-$15.18** |
| **Remove AN** (lower multiple) | GPI | $11.450149\times$ | **$246.18** | **+$15.18** |

### Benchmark Verification Audit Table

All automated checks in `pe_calculator.py` matched the course benchmarks exactly:

| Course Validation Check | Required Benchmark | Program Calculated Output | Status |
| :--- | :---: | :---: | :---: |
| AutoNation P/E | $10.037825\times$ | $10.037825\times$ | **PASS** |
| Group 1 Automotive P/E | $11.450149\times$ | $11.450149\times$ | **PASS** |
| Peer Median P/E | $10.743987\times$ | $10.743987\times$ | **PASS** |
| Asbury Peer-Implied Minimum | $\$215.81$ | $\$215.81$ | **PASS** |
| Asbury Peer-Implied Maximum | $\$246.18$ | $\$246.18$ | **PASS** |
| Asbury at Peer Median | $\$231.00$ | $\$231.00$ | **PASS** |
| Remove GPI: Remaining AN Estimate | $\$215.81$ | $\$215.81$ | **PASS** |
| Remove GPI: Change from Midpoint | $-\$15.18$ | $-\$15.18$ | **PASS** |
| Remove AN: Remaining GPI Estimate | $\$246.18$ | $\$246.18$ | **PASS** |
| Remove AN: Change from Midpoint | $+\$15.18$ | $+\$15.18$ | **PASS** |

---

## 3. Core Valuation Principles & Theoretical Framework

### 1. What Price-to-Earnings (P/E) Is
The Price-to-Earnings (P/E) ratio is a relative equity valuation multiple that expresses the market price of a company's equity relative to its net accounting profits:

$$\text{P/E} = \frac{P_0}{\text{EPS}} = \frac{\text{Market Capitalization}}{\text{GAAP Net Income Attributable to Common Stockholders}}$$

P/E is strictly an **equity multiple**. The numerator represents the market price per share of common equity, and the denominator represents the bottom-line earnings available exclusively to common shareholders after all operating costs, depreciation, interest payments to debtholders, and taxes have been deducted.

### 2. What Price Per Share Measures
Price per share ($P_0$) is the current clearing price of a single fractional unit of common equity in an active, liquid public market. Economically, it reflects the marginal investor's forward-looking consensus valuation of the present value of all expected future cash flows, dividends, and residual earnings accruing to that share of stock, discounted at the company's cost of equity ($r_e$). It incorporates collective market judgments regarding competitive advantages, growth trajectory, reinvestment opportunities, operating risks, and macroeconomic conditions.

### 3. What EPS Measures
Earnings Per Share (specifically GAAP diluted EPS) measures the dollar amount of net accounting income generated by the business during a specified period (here, FY2024) attributable to each share of common stock. The diluted calculation assumes the full conversion and exercise of all potentially dilutive securities—such as convertible notes, stock options, and restricted stock units (RSUs). EPS reflects historical accrual accounting performance under GAAP rather than cash generation, incorporating non-cash depreciation, amortization, and one-off accounting items.

### 4. What a P/E Multiple Tells Us
A P/E multiple indicates **how many dollars market participants are currently willing to pay for each dollar of annual net earnings**. 
- A multiple of $10.0\times$ means investors pay $\$10.00$ per $\$1.00$ of trailing earnings (an earnings yield of $10\%$).
- Differences in multiples across firms reflect market expectations about three structural variables:
  1. **Expected growth in earnings ($g$):** Faster-growing firms command higher multiples.
  2. **Perceived operational and financial risk (cost of equity, $r_e$):** Higher-risk firms command lower multiples.
  3. **Reinvestment efficiency / Return on Equity (ROE):** Firms that generate high returns on incremental capital reinvestment command higher multiples.

### 5. Why Comparing P/E Helps Compare Differently Sized Companies
Raw stock prices are arbitrary and incomparable because share count is an arbitrary managerial choice influenced by stock splits, reverse splits, and historical equity issuance. For instance, AutoNation's price of $\$169.84$ versus Group 1's price of $\$421.48$ tells us nothing about which company is more expensive or larger.

Similarly, comparing aggregate net income or market capitalization fails to adjust for the sheer operational scale of each enterprise. By dividing price by EPS, the P/E ratio produces a **scale-invariant, dimensionless metric** (dollars of equity value per dollar of earnings). This normalizes for corporate size and share count, enabling an apples-to-apples comparison of how public markets price one unit of earning power across different firms.

### 6. What Comparable-Company Valuation Adds to a Discounted Cash Flow (DCF)
A Discounted Cash Flow (DCF) model is an **intrinsic valuation** methodology built on bottom-up fundamental forecasts of operational cash flows (FCFF), long-term growth rates ($g$), and a weighted average cost of capital ($\text{WACC}$). While theoretically rigorous, DCFs are inherently sensitive to small changes in terminal growth and discount rate assumptions and can produce valuations completely disconnected from current market reality.

Comparable-company valuation provides an indispensable **extrinsic, market-based reality check**:
- **Anchors to current market clearing prices:** It reflects what actual buyers and sellers are paying for similar assets in today's interest rate, inflation, and credit environment.
- **Triangulation:** If a DCF indicates an intrinsic value of $\$300$ for Asbury while all peers trade between $10\times$ and $11.5\times$ P/E (implying $\$215$–$\$246$), the analyst must explain whether the DCF relies on overly optimistic assumptions or if the target possesses identifiable fundamental advantages that the market has not yet priced into peers.
- **Pragmatic transaction benchmark:** Public equity markets and acquisition negotiations routinely use peer multiples as standard pricing anchors.

### 7. Why a Lower P/E Does NOT Automatically Mean a Better Investment
A common misconception in retail finance is that a low P/E stock is an undervalued "bargain" while a high P/E stock is "expensive." This ignores the fundamental mathematics of equity valuation. 

Under the Gordon Growth equity formulation:

$$\frac{P_0}{E_1} = \frac{\text{Payout Ratio}}{r_e - g}$$

A low P/E ratio is often a rational market reaction to poor fundamentals—a phenomenon known as a **value trap**:
1. **Low or declining growth prospects ($g$):** A company facing structural obsolescence, customer defection, or margin compression will trade at a low multiple because its future earnings stream is stagnating or shrinking.
2. **Elevated risk and cost of equity ($r_e$):** A company burdened by excessive financial leverage (heavy debt loads) or high operational volatility requires a higher discount rate, mathematically depressing its P/E multiple.
3. **Low return on capital / high reinvestment burden:** If a company must reinvest nearly all of its cash flow merely to keep earnings flat, each dollar of reported accounting earnings produces little distributable cash flow for shareholders.
4. **The Cyclical P/E Trap:** For cyclical businesses (such as automotive retail), earnings peak at the top of the economic cycle. Investors anticipate an imminent decline in earnings, so the stock price falls while trailing earnings remain high, producing an artificially low trailing P/E multiple right before earnings collapse. Buying a cyclical firm at its lowest historical P/E often results in severe losses.

---

## 4. Practical Application & Peer Policy Nuance

### 8. When P/E Is Useful or Misleading

| Condition | Practical Impact on P/E | Appropriate Valuation Policy |
| :--- | :--- | :--- |
| **Negative Earnings (EPS $\le 0$)** | The multiple becomes negative or mathematically undefined. Multiplying a negative target EPS by a positive peer multiple yields a negative target price; multiplying positive target EPS by a negative peer multiple yields nonsense. | **Exclude P/E entirely.** Use revenue multiples (EV/Sales), asset-based valuation, or explicit DCF cash flow modeling until positive earnings stabilize. |
| **Unusual / Nonrepresentative Earnings** | One-time items (asset impairments, restructuring charges, litigation settlements, gain on facility sales, tax valuation reversals) distort GAAP net income. | **Normalize EPS** by adjusting out non-recurring, non-operating gains and losses before calculating P/E. |
| **Divergent Growth Profiles** | Applying a low-growth peer group's multiple to a high-growth target severely undervalues the target's future cash generation. | Adjust for growth differentials using forward P/E, PEG ratios ($\text{P/E} / g$), or multi-stage DCF models. |
| **Differences in Capital Structure** | P/E is an equity multiple influenced by debt. A company with high financial leverage has lower net income (due to interest expense) and higher equity risk, altering its P/E multiple relative to an un-levered peer. | Compare **Enterprise Value multiples (EV/EBITDA, EV/EBIT)** which are capital-structure neutral, or evaluate interest coverage ratios. |

### 9. Why Franchised Vehicle Retail and Parts/Service Economics Matter
Superficial industry taxonomy (e.g., GICS "Automotive Retail" or "Consumer Cyclicals") frequently lumps together businesses with fundamentally incompatible economic structures:
- **Pure-Play Used Car Retailers (e.g., Carvana, CarMax):** Subject to severe used-vehicle price volatility, wholesale auction swings, and inventory holding risk, with minimal service repair infrastructure and zero OEM warranty protection.
- **Aftermarket Auto Parts Retailers (e.g., AutoZone, O'Reilly):** High-margin specialized retail distribution without vehicle inventory floor plans or manufacturer franchise agreements.
- **Automotive OEMs (e.g., Ford, General Motors, Tesla):** Capital-intensive heavy manufacturing with vehicle warranty liabilities, cyclical factory utilization, and unionized labor obligations.

In contrast, **franchised dealership groups** (Asbury, AutoNation, Group 1) operate an integrated, four-pillar business model with distinct competitive and economic characteristics:
1. **Protected Franchise Moats:** State franchise laws grant exclusive geographic territories to franchised dealers and prohibit OEMs from selling directly to consumers or granting competing local franchises.
2. **The "Fixed Operations" Engine (Parts & Service):** 
   - Generates **40% to 50%+ of total dealership gross profit** with gross margins typically between $50\%$ and $60\%$.
   - **Counter-cyclical resilience:** Vehicle owners require safety inspections, maintenance, OEM warranty service, and collision repairs regardless of macroeconomic conditions. In economic downturns, consumers delay new vehicle purchases and keep older vehicles longer, expanding the aging vehicle fleet that requires maintenance and parts.
3. **Finance & Insurance (F&I):** High-margin transactional commissions earned from arranging third-party customer financing, extended warranties, and insurance policies with virtually zero inventory capital requirement.
4. **New & Used Vehicle Retail:** Generates large top-line revenue at modest gross margins ($5\%$ to $9\%$), but functions as the primary customer acquisition funnel that drives future warranty, service, parts, trade-in, and F&I profits.

**Analytical Conclusion:** To evaluate Asbury accurately, candidate peers **must** share this exact franchised dealership economic profile, where high-margin fixed operations provide an earnings cushion against vehicle sales cyclicality.

### 10. Peer Policy Decisions: AutoNation (AN) and Group 1 Automotive (GPI)

#### AutoNation (AN): **USE**
- **Business Reasoning:** AutoNation is the largest pure-play automotive retailer in the United States, operating franchised dealerships across major metropolitan markets. Like Asbury, AutoNation derives the foundation of its profitability from franchised parts/service operations, F&I, and diversified new/used vehicle sales across domestic, import, and luxury brands. It operates under identical U.S. consumer credit conditions, interest rate environments, and state franchise legal frameworks. AutoNation is a direct, high-quality operational comparable.

#### Group 1 Automotive (GPI): **QUALIFY (USE WITH QUALIFICATION)**
- **Business Reasoning:** Group 1 operates an identical franchised dealership model in the United States, with comparable brand portfolios and high-margin parts and service operations. However, Group 1 has substantial, growing international operations in the **United Kingdom** (greatly expanded by its acquisition of Inchcape's UK retail business in 2024). 
- **Analytical Qualifications:**
  1. **Geographic & Currency Exposure:** Group 1 generates a substantial fraction of its earnings in British Pounds (GBP), exposing it to foreign currency translation volatility against the U.S. Dollar.
  2. **Regulatory & Market Divergence:** The UK automotive retail market differs structurally from the U.S.: dealership margins are historically tighter, OEM agency sales models are more prevalent, and consumer economic dynamics diverge from the U.S. market.
  3. **M&A Integration Risk:** Recent UK acquisitions require ongoing debt servicing and operational integration.
- **Policy Determination:** GPI is retained as a candidate peer because its core U.S. operations reflect the same franchised dealership economics as Asbury, but its multiple must be qualified to reflect its international diversification and margin differences.

---

## 5. Peer Set Sensitivity & Evaluation

### 11. Impact of Removing Group 1 Automotive (GPI)
When GPI (the higher-multiple peer at $11.450149\times$) is excluded from the peer set:
- The remaining peer group consists solely of AutoNation ($10.037825\times$).
- The median peer multiple drops from $10.743987\times$ to $10.037825\times$.
- Asbury's implied target valuation drops from **\$231.00** to **\$215.81**, a direct reduction of **-\$15.18** per share (or $-6.57\%$).

**Analytical Takeaway:** In a two-peer set, the valuation benchmark is extraordinarily fragile. Excluding the qualified peer immediately eliminates the upper half of the valuation spectrum and anchors the target directly to the remaining peer's lower valuation.

### 12. Why a Single Remaining Peer Yields a Reference Estimate, Not a Range
A **valuation range** requires statistical dispersion—a defined lower bound (minimum) and upper bound (maximum) established by multiple independent market observations. 

When only AutoNation remains:
$$\text{Min P/E} = \text{Median P/E} = \text{Max P/E} = 10.037825\times$$
$$\text{Implied Price} = 10.037825\times \times \$21.50 = \$215.81$$

With $n = 1$, the variance and spread are zero. There is no interval or distribution reflecting market uncertainty. The resulting figure of $\$215.81$ is a **single-point reference estimate**—a calculation answering what Asbury would be worth if priced identically to AutoNation—not an implied range.

### 13. Why This Result Does NOT Prove Asbury Is Fairly Valued
Asbury's actual closing price on December 31, 2024 was **\$243.03**. While this price falls comfortably within the peer-implied range of **\$215.81 to \$246.18**, it sits $\$12.03$ ($+5.21\%$) above the two-peer median of $\$231.00$.

This alignment **does not prove** that Asbury is fairly valued, for five critical reasons:
1. **Comps Measure Pricing, Not Value:** Multiples analysis measures how public markets are currently pricing peers, not whether that price equals true intrinsic economic value. If the public market is systematically under-pricing or over-pricing the entire automotive retail sector, a comparable-company multiple simply replicates that market-wide mispricing.
2. **Sample Size Limitations:** A peer set of two companies (reduced to one if GPI is excluded) lacks statistical reliability. Idiosyncratic events, management decisions, or capital structures at AutoNation or Group 1 heavily skew the benchmark.
3. **Idiosyncratic Business Differences:** Asbury possesses distinct operating characteristics that may justify a premium or discount relative to peers:
   - Geographic concentration in fast-growing Sunbelt and Southeastern markets.
   - Distinct brand exposure (higher luxury brand concentration commands higher margins).
   - Proprietary digital retail initiatives (e.g., Asbury's *Clicklane* platform).
   - Superior operating margins or higher Return on Equity (ROE) that warrant trading at $11.30\times$ P/E versus AutoNation's $10.04\times$.
4. **Capital Structure Differences Ignored by P/E:** P/E is an equity multiple that does not explicitly account for enterprise-level leverage. If Asbury carries higher or lower debt than AutoNation, their risk profiles differ fundamentally. An enterprise-value multiple (EV/EBITDA) would be required to verify whether total firm value aligns across capital structures.
5. **Accrual Accounting vs. Cash Flow:** P/E relies on GAAP EPS, which can diverge significantly from true free cash flow due to dealership floor-plan interest, working capital inventory cycles, and facility capital expenditures.

---

## 6. Distinguishing Case Facts from Analytical Interpretations

To maintain rigorous research standards, the table below clearly delineates supplied factual data from student analytical interpretations:

| Category | Item / Metric | Classification | Description / Rationale |
| :--- | :--- | :---: | :--- |
| **Target Pricing & Earnings** | ABG Price (\$243.03), EPS (\$21.50) | **Supplied Fact** | Frozen case inputs as of Dec 31, 2024 / FY2024 annual reports. |
| **Peer Pricing & Earnings** | AN Price (\$169.84), EPS (\$16.92)<br>GPI Price (\$421.48), EPS (\$36.81) | **Supplied Fact** | Frozen case inputs as of Dec 31, 2024 / FY2024 annual reports. |
| **Calculated Multiples & Implied Values** | AN P/E ($10.037825\times$), GPI P/E ($11.450149\times$), Median ($10.743987\times$), Range (\$215.81–\$246.18), Median (\$231.00), Leave-one-out ($\pm\$15.18$) | **Mathematical Derivation** | Exact mathematical outputs calculated directly from supplied facts without external manipulation. |
| **Peer Policy: AutoNation** | Decision: **USE** | **Analytical Interpretation** | Grounded in AutoNation's pure-play US franchised dealership operating model matching Asbury. |
| **Peer Policy: Group 1** | Decision: **QUALIFY** | **Analytical Interpretation** | Grounded in GPI's UK international exposure introducing currency and margin differences. |
| **Valuation Assessment** | P/E alignment does not prove fair value | **Analytical Interpretation** | Grounded in financial theory regarding relative pricing vs. intrinsic value, sample size, and capital structure. |

---

## 7. Execution Guide & Next Steps

### Exact Run Command
To reproduce all quantitative calculations from the workspace root:

```powershell
.\Python-3.13.15\python.exe Lab-07\pe_calculator.py
```

### Pre-Checkout Checklist (Before GitHub Checkout)
- [x] Dedicated Lab 07 directory created: `Lab-07/`
- [x] Standard-library Python calculator created and tested: `Lab-07/pe_calculator.py`
- [x] All 10 case validation benchmarks verified and passing.
- [x] Comprehensive Lab 07 documentation created: `Lab-07/lab07.md`
- [x] Unrelated files preserved (no modifications to `Project-1/dcf.py` or IREN research files).
- [ ] Review files in VS Code.
- [ ] Stage and commit Lab 07 files to git when ready for class checkout.

---

## 8. Academic Context & AI Assistance Disclosure

This report and valuation model were prepared for FIN 43900 (AI Finance Applications, Purdue University) as a laboratory learning exercise. It is not investment research, and it does not constitute financial advice.

**AI Assistance Disclosure:**
Drafted with the assistance of AI (Google Antigravity / Codex), resumed from prior FIN 439 coursework sessions; case inputs, peer business evidence, and quantitative outputs were calculated, validated, and verified by the student; all peer policy decisions, analytical interpretations, and valuation judgments are my own. Any remaining errors are my own.

