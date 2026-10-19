# Video 3 Recording Guide: Live Product Demonstration & Investment Committee Defense

**Student:** Elliot (one "t")  
**Course:** FIN 43900 (Corporate Finance / Applied Financial Modeling, Purdue University)  
**Company:** IREN Limited (NASDAQ: IREN)  
**Maximum Allowed Duration:** **5:00 minutes**  
**Target Duration:** **4:15 – 4:45 minutes** (comfortably below the 5:00 minute ceiling)  
**Deliverable Artifacts Produced Later:** Video 3 recording file + `transcript-video-3.txt` / `.vtt`

---

## 1. What the Professor is Evaluating in Video 3

The professor is evaluating two integrated criteria:
1. **CRITICAL REQUIREMENT — Live Interactive Product Demonstration (First 60–90 Seconds):**  
   You **must** start the video by interacting live with your deployed or locally hosted application ([`app.py`](../app.py)). You must demonstrate bounded driver controls, live reactive valuation recalculations, the reset button, and visual double-entry accounting integrity checks.
2. **Buy-Side Investment Committee Presentation & Defense (Remaining 3–4 Minutes):**  
   You must step into the role of a buy-side corporate finance analyst presenting to an institutional Investment Committee. Using [`Decision-Memo.pdf`](../Decision-Memo.pdf), you will defend:
   - Your recommendation: **WATCH / DEFER** (Zero equity allocation).
   - The fundamental valuation: **$12.12 / share** base case (fundamental range **$4.06 to $19.25 / share**) vs. current market price of **$45.73** (~280% premium).
   - Table 1 Enterprise-to-Equity DCF Bridge (connecting operating EV to net equity value via cash and debt).
   - Methodological reconciliation with direct FCFE (-$5.31 / share) explaining the pre-funding cash credit.
   - Operating driver hierarchy: Capacity Energization ($15.19 span) is the primary driver, 2.7x more impactful than power gross margin ($5.65 span).
   - Principal risks and three concrete, observable reversal triggers.

---

## 2. Pre-Recording Setup: Applications & Files to Open

Open and stage the following before hitting record on Zoom:

1. **Terminal 1 (Background Process for Streamlit):**  
   Open PowerShell in `C:\Users\ellio\Documents\FIN439\IREN-research` and launch the app:
   ```powershell
   py -m streamlit run app.py
   ```
2. **Web Browser (Primary Screen at Start):**  
   The command will automatically open your default browser to `http://localhost:8501`.  
   - Maximize or position the browser window cleanly.  
   - Verify that all sliders are at their default positions:
     - Cash Gross Margin: **70.0%**
     - Revenue Growth Path Shift: **0.0 pp**
     - Capex Scale Multiplier: **1.00x**
     - WACC Discount Rate: **10.0%**
     - Terminal Growth Rate ($g$): **2.5%**
   - Confirm that the green banner says: **DOUBLE-ENTRY ACCOUNTING INTEGRITY: PASS (Gap = 0.0000)**.
   - Confirm the displayed primary FCFF value is **$12.12 / share**.
3. **PDF Reader (Secondary Screen for Committee Presentation):**  
   Open [`Decision-Memo.pdf`](../Decision-Memo.pdf).  
   - Have it zoomed to Page 1, showing Section 1, Section 2, and Table 1 (*Enterprise-to-Equity DCF Bridge*).  
   - Be ready to scroll down to Page 2 (*Table 2 Sensitivity Spans & Reversal Triggers*).

---

## 3. Step-by-Step Screen-Sharing Click Path

Follow this exact chronological sequence:

| Timestamp | Application on Screen | What to Click / Demonstrate | What You Are Explaining |
|---|---|---|---|
| **0:00 – 1:15** | **Web Browser** (`app.py` Streamlit Workbench) | **MANDATORY OPENING PRODUCT DEMO:**<br>1. Point to the green check banner (`Gap = 0.0000`).<br>2. Point to the base valuation: **$12.12 / share**.<br>3. Move **Cash Gross Margin slider** from 70% $\rightarrow$ **75%** (show value rises to **$14.61**).<br>4. Move **Revenue Growth slider** to **+5.0 pp** (show value rises to **$19.25**).<br>5. Click **"Reset to Base Case"** button (show sliders snap back and value returns to **$12.12**). | Introduce the interactive pro-forma workbench. Show live reactivity, bounded controls, the reset function, and continuous double-entry accounting validation. |
| **1:15 – 2:30** | `Decision-Memo.pdf` (Page 1) | Switch window to `Decision-Memo.pdf` Page 1. Point cursor at Section 1 (*Recommendation: WATCH / DEFER*) and Table 1 (*Enterprise-to-Equity Bridge*). | Deliver the formal committee ask: WATCH / DEFER at $45.73 market price (~280% premium over $12.12 fundamental value). Walk through Table 1: Operating EV ($6,715M) + Cash ($5,896M) - Debt ($7,837M) = Equity ($4,774M / 394M shares = $12.12). Reconcile with -$5.31 FCFE. |
| **2:30 – 3:35** | `Decision-Memo.pdf` (Page 2) | Scroll down to Page 2. Point to Table 2 (*One-At-A-Time Sensitivity Spans*). | Explain driver hierarchy: Capacity Energization ($15.19 span) is the primary driver. Even under combined aggressive upside (+5 pp growth & 75% margin), value only reaches $19.25, proving the market price of $45.73 prices in multi-decade perfection. |
| **3:35 – 4:35** | `Decision-Memo.pdf` (Page 2) | Point cursor at Section 4 (*Risks & Monitoring Triggers*) and Section 5 (*Action Requested*). | Detail 3 observable reversal triggers: Horizons 2–4 customer acceptance, quarterly revenue >$375M with positive operating cash flow before prepayments, and <10% dilution. State committee ask: confirm zero equity position; next review at Q2 FY2027 earnings. |

---

## 4. Spoken Script (Natural & Conversational)

> **[0:00 – 1:15 | Mandatory Opening: Live Interactive Product Demonstration]**  
> *"Good afternoon, members of the Investment Committee. My name is Elliot.  
> Before presenting our formal recommendation on IREN Limited, I want to demonstrate our interactive valuation workbench. As required, this is a live, semi-adjustable application built for our investment team.  
> Looking at the top of the interface, our green check badge confirms that our core double-entry accounting engine is fully validated: in every single forecast year, balance sheet assets equal liabilities plus equity with a gap of zero.  
> On the left-hand panel, our key load-bearing drivers are exposed with bounded controls. Right now, our audited baseline yields a primary FCFF intrinsic equity value of **$12.12 per share**.  
> If our energy team believes IREN can achieve greater power efficiency, I can move the Cash Gross Margin slider from 70% to 75%. You can see the model live-rebalances: Year 5 EBIT expands to $891 million, and intrinsic value increases to **$14.61 per share**.  
> If we model accelerated hyperscaler cluster energization—shifting our revenue growth path up by +5 percentage points across all five years—intrinsic value rises to **$19.25 per share**.  
> And with a single click on our 'Reset to Base Case' button, all parameters immediately snap back to our baseline.  
> Having confirmed that our operational engine is interactive, bounded, and mathematically balanced, let’s turn to our investment committee decision memo."*

> **[1:15 – 2:30 | Committee Recommendation & The Enterprise-to-Equity Bridge]**  
> *(Switch screen to `Decision-Memo.pdf` Page 1)*  
> *"Looking at Page 1 of our decision memo, the AI Task Force recommends that the fund **DO NOT INITIATE** an equity position in IREN Limited and place the security on our **WATCH / DEFER** list.  
> The public market currently trades IREN at **$45.73 per share**, an $18 billion market capitalization. The market is pricing IREN as an unencumbered hyperscale AI winner following its $9.7 billion Microsoft contract and initial delivery of Horizon 1.  
> However, looking at Table 1—our Enterprise-to-Equity DCF Bridge—our audited five-year pro-forma model establishes a fundamental intrinsic equity value of **$12.12 per share**. The market price reflects an unsustainable **~280% premium** over operating reality.  
> As shown in Table 1, the present value of core operating cash flows and terminal value yields an enterprise value of $6.72 billion. When we credit IREN’s $5.90 billion in cash and deduct its $7.84 billion in contractual debt and notes, we arrive at an intrinsic equity value of $4.77 billion, or $12.12 per share across 394 million shares.  
> Crucially, while a direct equity FCFE calculation yields negative $5.31 per share due to heavy upfront capex burn, the FCFF bridge correctly credits the $5.9 billion cash balance that pre-funds this capital plan. Both methodologies arrive at the exact same conclusion: the current market price is massively detached from fundamentals."*

> **[2:30 – 3:35 | Sensitivity Analysis & The Capex Burden]**  
> *(Scroll down to Page 2, Table 2)*  
> *"Turning to Table 2 on Page 2, our sensitivity analysis establishes two fundamental conclusions:  
> First, the Capacity Energization Path is the dominant operating driver, producing a valuation span of **$15.19 per share** ($4.06 to $19.25), which is nearly three times more impactful than cash gross margin fluctuations. Megawatt delivery schedule dictates value.  
> Second, even under our most aggressive upside scenario—accelerating megawatt energization by +5 percentage points and optimizing power gross margins to 75%—intrinsic value only reaches **$19.25 per share**.  
> To justify $45.73 today, an investor must assume decades of uninterrupted hyper-growth with zero construction delays, zero margin compression, and perfect debt refinancing. There is zero execution margin of safety."*

> **[3:35 – 4:35 | Principal Risks, Reversal Triggers & Committee Ask]**  
> *(Point cursor at Section 4 and Section 5)*  
> *"We do not recommend shorting the stock due to extreme retail momentum, high borrowing costs, and potential acquisition speculation. Instead, we recommend zero allocation and propose three concrete, observable reversal triggers:  
> 1. **Verified Customer Acceptance:** SEC Form 8-K filings confirming commercial delivery and recognized billing for Childress Horizons 2, 3, and 4, scaling recognized GAAP quarterly revenue above $375 million ($1.5 billion ARR).  
> 2. **Operating Cash Flow Inflection:** Two consecutive quarters of positive cash flow from operations before customer prepayments.  
> 3. **Market Price Correction:** A market pullback into our fundamental valuation band of $12 to $18 per share.  
> **Committee Action Requested:** Confirm zero equity allocation. We will revisit the name at the Q2 FY2027 earnings release in February 2027. Thank you, and I welcome the committee's questions."*

---

## 5. Key Financial Figures Verified for Video 3

- **Committee Action:** Confirm zero equity position / WATCH / DEFER
- **Current Market Price:** $45.73 / share (~$18.0B market capitalization)
- **Primary Model Value:** $12.12 / share (FCFF Enterprise DCF; WACC 10.0%, $g = 2.5\%$)
- **Market Premium Over Fundamental Value:** +277.3% (~280%)
- **Fundamental Valuation Range:** $4.06 to $19.25 / share
- **Table 1 Bridge Numbers:**
  - PV Explicit FCFF (FY27E–FY31E): -$2,238.85M
  - PV Terminal Value: +$8,954.18M
  - Enterprise Value: $6,715.33M
  - (+) Cash & Equivalents: +$5,895.59M
  - (-) Term Debt & Convertible Notes: -$7,836.74M
  - Implied Equity Value: $4,774.18M
  - Basic Ordinary Shares: 394.059M
  - Implied VPS: $12.12 / share
- **Sensitivity Spans (Table 2):**
  - Capacity Energization: $4.06 to $19.25 ($\Delta = \$15.19 / \text{sh}$, dominant driver)
  - Power Gross Margin: $8.96 to $14.61 ($\Delta = \$5.65 / \text{sh}$)
- **Reversal Condition Thresholds:** Recognized GAAP quarterly revenue $> \$375\text{M}$ ($1.5B ARR), positive operating cash flow before customer prepayments, expansion funded without share dilution $> 10\%$.

---

## 6. Common Recording Mistakes to Avoid

- **Mistake 1: Starting with PowerPoint or PDF.** The rubric explicitly requires the **live interactive product demonstration in the first 60–90 seconds**. Always start on `http://localhost:8501`.
- **Mistake 2: Forgetting to click "Reset to Base Case".** Demonstrating that the product can gracefully snap back to the audited baseline proves state management usability.
- **Mistake 3: Recommending a Short position.** Institutional committees evaluate risk management. Explicitly advise *against* shorting due to high borrow costs and momentum; recommend zero equity allocation.
- **Mistake 4: Exceeding 5:00 minutes.** This rehearsal script takes approximately 4:20 to 4:35. Deliver the committee ask promptly after detailing the reversal triggers.

