# FIN 439 Lab 14 — Portfolio Baselines

**Course:** FIN 43900 (Applied Financial Modeling & Corporate Valuation, Purdue University)  
**Student:** Elliot  
**Client / Case Study:** Meridian Foundation Reserve  
**Files:** [`portfolio.py`](portfolio.py) | [`mandate.py`](mandate.py)  

---

## 1. Objective

Lab 14 implements a Python risk engine using the standard library to calculate the expected return, volatility (incorporating full covariance), and reserve-eligible allocation of three baseline portfolio allocations (Benchmark, Equal Weight, and Inverse Volatility) for the Meridian Foundation training case. It evaluates whether any baseline satisfies the foundation's 6.50% expected return objective and tests the Benchmark portfolio against the institutional mandate rules established in Lab 13.

---

## 2. Inputs

The following parameters are course-provided training assumptions for the Meridian Foundation educational case, not real market estimates or current trading forecasts.

### Asset Sleeve Assumptions

| Asset Sleeve | Expected Return | Volatility ($\sigma$) | Reserve-Eligible |
|---|---:|---:|:---:|
| Treasury bills | 3.5% | 0.5% | Yes |
| Treasury 10-year note | 4.3% | 7.0% | Yes |
| Investment-grade bond fund | 5.0% | 6.0% | No |
| Global equity index fund | 8.0% | 16.0% | No |

### Correlation Matrix ($\rho$)

| Asset Sleeve | Treasury bills | Treasury 10-year | IG bond fund | Global equity |
|---|---:|---:|---:|---:|
| Treasury bills | 1.00 | 0.10 | 0.05 | 0.00 |
| Treasury 10-year note | 0.10 | 1.00 | 0.80 | −0.10 |
| Investment-grade bond fund | 0.05 | 0.80 | 1.00 | 0.25 |
| Global equity index fund | 0.00 | −0.10 | 0.25 | 1.00 |

### Return Objective and Policy Parameters
- **CPI Baseline Estimate:** 2.5%
- **Real Return Target:** 4.0%
- **Nominal Return Objective:** 6.5% ($\text{CPI} + 4.0\%$)
- **Reserve-Eligible Sleeves:** Treasury bills and Treasury 10-year note (daily-liquid sovereign obligations)
- **Mandate Reserve Floor:** 3.0% ($100.0M reserve $\times$ 4 quarters $\times$ $0.75M/quarter)

---

## 3. Portfolio Results

All results are calculated dynamically by `portfolio.py` from the inputs above.

### Summary Table

| Portfolio | Weights: Bills / 10-Yr / IG / Equity | Expected Return | Volatility | Reserve Allocation | Meets 6.5% Objective? |
|---|---|---:|---:|---:|:---:|
| **Benchmark** | 0.0% / 0.0% / 40.0% / 60.0% | 6.80% | 10.46% | 0.0% | Yes |
| **Equal Weight** | 25.0% / 25.0% / 25.0% / 25.0% | 5.20% | 5.21% | 50.0% | No |
| **Inverse Volatility** | 84.3% / 6.0% / 7.0% / 2.6% | 3.77% | 1.05% | 90.3% | No |

### Calculation Notes and Exact Values
- **Benchmark:** Expected Return = 6.8000%, Volatility = 10.4614%, Reserve Allocation = 0.0%. Meets the 6.50% objective ($6.80\% \ge 6.50\%$).
- **Equal Weight:** Expected Return = 5.2000%, Volatility = 5.2145%, Reserve Allocation = 50.0%. Fails the 6.50% objective ($5.20\% < 6.50\%$).
- **Inverse Volatility:** Raw reciprocal weights: Bills ($1 / 0.005 = 200.0$), 10-Year ($1 / 0.070 \approx 14.2857$), IG Bonds ($1 / 0.060 \approx 16.6667$), Equity ($1 / 0.160 = 6.25$). Sum of reciprocals = $237.2024$. Normalized weights: Bills = 84.316%, 10-Year = 6.023%, IG Bonds = 7.026%, Equity = 2.635%. Expected Return = 3.7721%, Volatility = 1.0497%, Reserve Allocation = 90.339%. Fails the 6.50% objective ($3.77\% < 6.50\%$).

All three calculated portfolios match the professor's published answers exactly subject to normal rounding.

---

## 4. Validation

The following validation checks were executed in Python to confirm engine integrity:

### Test 1 — Correlation Sensitivity Check
- **Procedure:** Temporarily changed the Investment-Grade Bond / Global Equity correlation from 0.25 to 0.50 in symmetric matrix positions `[2][3]` and `[3][2]`.
- **Expected Benchmark Volatility:** Approximately 11.00%.
- **Actual Calculated Volatility:** **11.00%** (exact: 10.9982%).
- **Status:** **PASS**. Demonstrates that portfolio risk correctly incorporates the covariance cross-product ($2 w_i w_j \text{Cov}(i,j)$) rather than omitting correlation. Original 0.25 correlation was restored afterward.

### Test 2 — Invalid Correlation Refusal
- **Procedure:** Temporarily set the Investment-Grade Bond / Global Equity correlation to 1.30 (exceeding the mathematical upper limit of +1.0).
- **Expected Engine Behavior:** Refuse execution with a clear error message.
- **Actual Engine Behavior:** Validation check raised `ValueError`:
  ```text
  Invalid correlation value: cell (2, 3) has value 1.3000, which violates the required range [-1.0, +1.0].
  ```
- **Status:** **PASS**. Confirms that the engine strictly refuses invalid correlation matrices prior to performing portfolio computations. Original inputs were restored afterward.

---

## 5. Mandate Check

The Benchmark portfolio (40.0% Investment-Grade Bond Fund, 60.0% Global Equity Index Fund) was added to `mandate.py` as **Candidate E** and evaluated against the Meridian Foundation mandate rules.

### Mechanical Evaluation Results (Candidate E)
- **Weights sum to 100%:** 100.0% (PASS)
- **Long-only constraint (lowest weight $\ge$ 0.0%):** 0.0% (PASS)
- **Reserve requirement ($\ge$ 3.0%):** **0.0% (FAIL)**
- **Five-business-day liquidity ($\ge$ 90.0%):** 100.0% (PASS — equities redeem in 2 days, IG bonds in 3 days)
- **Single-company issuer concentration ($\le$ 8.0%):** 0.0% (PASS — diversified index funds are exempt)
- **Calendar-year loss rule:** Requires CIO clarification
- **Overall Verdict:** **fails 1 rule(s)**

### Key Mandate Finding
**The client's own benchmark breaks the client's mandate.** Although Candidate E represents the strategic policy benchmark specified in Statement S4 and satisfies the 6.50% expected return objective (6.80%), it cannot be adopted as the reserve portfolio because its reserve-eligible allocation is 0.0% against the mandatory 3.0% floor. To make the benchmark compliant with institutional governance, at least 3.0% must be carved out of equities and bonds into Treasury bills or 10-year notes.

---

## 6. Brief Interpretation

### Diversification Mechanics
Portfolio variance is calculated as:
$$\sigma_p^2 = \sum_{i=1}^n w_i^2 \sigma_i^2 + 2 \sum_{i < j} w_i w_j \text{Cov}(i, j) = \sum_{i=1}^n w_i^2 \sigma_i^2 + 2 \sum_{i < j} w_i w_j \rho_{i,j} \sigma_i \sigma_j$$

Because asset correlations are strictly below +1.0, portfolio volatility is less than the weighted average of the asset volatilities. For the Benchmark portfolio:
$$\text{Weighted Average Volatility} = 0.40(6.0\%) + 0.60(16.0\%) = 2.40\% + 9.60\% = 12.00\%$$
Because the correlation between bonds and equities is $\rho = 0.25$, actual portfolio volatility drops to **10.46%**, eliminating $1.54\%$ of annualized risk through diversification alone. If the correlation rises to 0.50 (as tested in Test 1), diversification benefits weaken and volatility increases to **11.00%**.

### Why Inverse Volatility Concentrates in Treasury Bills
Inverse-volatility weighting sets each asset's allocation proportional to $1 / \sigma_i$, intentionally penalizing volatile sleeves. In this asset universe:
- Treasury bills have an extremely low volatility ($\sigma = 0.5\% = 0.005$), yielding a reciprocal of $1 / 0.005 = 200.0$.
- In contrast, the 10-year note ($\sigma = 7.0\%$) yields $14.29$, IG bonds ($\sigma = 6.0\%$) yield $16.67$, and Global Equity ($\sigma = 16.0\%$) yields $6.25$.
- Because bills have a volatility 12 to 32 times smaller than the other sleeves, Treasury bills capture **84.3%** of the entire portfolio allocation ($200.0 / 237.20$).

While this concentration compresses portfolio volatility to an ultra-low **1.05%** and produces a massive reserve allocation of **90.3%**, it starves the portfolio of growth assets, depressing expected return to **3.77%**.

### Return, Risk, and Mandate Compliance Across the Baselines
The three baseline portfolios illustrate the trade-offs in institutional portfolio construction:

1. **Benchmark (60/40 Equity/Bond):** Achieves the return objective ($6.80\% \ge 6.50\%$) with moderate volatility ($10.46\%$), but **fails the reserve requirement** ($0.0\% < 3.0\%$).
2. **Equal Weight (25% each):** Satisfies the reserve mandate ($50.0\% \ge 3.0\%$) and cuts volatility to $5.21\%$, but **fails the return objective** ($5.20\% < 6.50\%$), generating a 1.30% annual purchasing power deficit.
3. **Inverse Volatility (84.3% Bills):** Provides extreme capital preservation ($\sigma = 1.05\%$) and abundant liquidity ($90.3\%$), but **fails the return objective by 2.73%** ($3.77\% \text{ vs. } 6.50\%$).

None of the three naive baselines simultaneously meets both the foundation's 6.50% expected return requirement and its 3.0% reserve mandate constraint.
