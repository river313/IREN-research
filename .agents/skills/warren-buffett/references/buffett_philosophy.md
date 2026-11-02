# Warren Buffett: Investment Philosophy & Quality Framework Reference

## 1. Core Tenet: Business Ownership Mentality
A share of stock represents a proportional ownership claim in an underlying business, not a speculative paper slip. An investor must evaluate a company the way a sole proprietor evaluates buying the whole corner store.
* **The Central Rule:** "It is far better to buy a wonderful company at a fair price than a fair company at a wonderful price."
* **Circle of Competence:** Stick strictly to businesses whose economics, competitive dynamics, and long-term customer relationships you can understand and project decades ahead.

---

## 2. The Economic Moat
An economic moat is a durable structural advantage that protects a business's high returns on invested capital from the erosion of market competition:
1. **Low-Cost Producer / Shared Economies of Scale:** Operating with structural cost advantages that competitors cannot match without enduring catastrophic operating losses (e.g., GEICO, Costco).
2. **High Customer Switching Costs:** Friction, expense, or operational risk that prevents customers from switching to competing alternatives.
3. **Network Effects:** A product or service whose utility increases proportionally with each additional user.
4. **Intangible Assets / Brand Loyalty:** Enduring consumer trust and habituation (e.g., Coca-Cola, See's Candies, Apple).

---

## 3. Financial Metrics & Quality Hurdle Rates

### A. Return on Equity (ROE) >= 15%
* **Significance:** Measures management's ability to generate earnings from the capital shareholders have entrusted to them.
* **Buffett Criterion:** Consistent ROE above 15% across economic cycles without relying on excessive financial leverage.
* **SEC XBRL Basis:** Net Income (`NetIncomeLoss`) divided by Year-End Stockholders' Equity (`StockholdersEquity`).
* **Condition:** If stockholders' equity is zero or negative (due to heavy accumulated deficits or extreme share repurchases), ROE cannot be reliably assessed and must be treated as "not known".

### B. Owner Earnings
* **Definition (1986 Berkshire Hathaway Annual Report):**
  $$\text{Owner Earnings} = \text{Operating Cash Flow} - \text{Capital Expenditures}$$
  Where Capital Expenditures represent the annual capitalized spending required to maintain the business's long-term competitive position and unit volume.
* **Significance:** Reported GAAP net income often distorts true economic earnings due to non-cash accruals, depreciation conventions, or mandatory heavy reinvestment cycles. A business that generates high GAAP profits but requires all its cash to buy replacement machinery generates zero cash for its owners.
* **SEC XBRL Basis:** Net Cash Provided by Operating Activities (`NetCashProvidedByUsedInOperatingActivities`) minus Capital Expenditures (`PaymentsToAcquirePropertyPlantAndEquipment` or `PaymentsToAcquireProductiveAssets`).
* **Checks:**
  1. **Owner Earnings Positive Every Year:** Must generate surplus cash in all evaluated fiscal years.
  2. **Owner Earnings Growth:** Owner earnings in the final fiscal year must exceed owner earnings in the initial fiscal year.

---

## 4. Evaluation Mandate: Quality vs. Valuation
In the FIN 439 Legend Investor framework:
* **Python computes every financial number from SEC EDGAR filings.**
* **AI interprets those numbers using Buffett's philosophy.**
* **Mandate:** Appraise business quality independently of market price. While Buffett insists on a "margin of safety" when buying, determining whether a business is inherently *worthy* of ownership is the prerequisite step.
* **Verdicts:**
  * **OWN THE BUSINESS:** Exceptional economic moat, consistently passes ROE and Owner Earnings checks, highly durable franchise.
  * **WATCH:** High-quality business that has cyclical or temporary headwinds, or requires further monitoring.
  * **PASS:** Fails fundamental quality checks, lack of owner earnings, structural disruption, or outside circle of competence.
