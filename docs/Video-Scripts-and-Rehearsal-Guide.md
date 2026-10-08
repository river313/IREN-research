# Project 1 — Video Presentation Scripts & Screen-Sharing Rehearsal Guide

**Student Name:** Elliot  
**Course:** FIN 43900 (Corporate Finance / Applied Financial Modeling, Purdue University)  
**Target Company:** IREN Limited (NASDAQ: IREN)  
**Valuation Date:** October 8, 2026  

> [!IMPORTANT]
> **Academic Integrity Notice:**  
> These scripts and screen plans are rehearsal frameworks prepared for Elliot to personally practice, record, and defend. These videos have **not yet been recorded**, and transcripts must only be generated from your actual spoken recordings.

---

## 📹 Video 1: Research Evolution & Evidence Trajectory

**Maximum Duration:** **≤ 3:00 minutes** (Recommended target: **2:30 – 2:45**)  
**Core Question to Answer:** *What changed or remained stable after project-specific research; what drove it; and what evidence justified it?*  
**Deliverable File to Submit Later:** `Video 1` link + `transcript-video-1.txt`  

### Screen-Sharing Plan
- **0:00 – 0:30:** Display [`IREN_2026-09-03_report.md`](../IREN_2026-09-03_report.md) (Edition A baseline, commit `2710819`) highlighting Section 6.
- **0:30 – 1:30:** Display [`Research-Evolution.pdf`](../Research-Evolution.pdf) (or `docs/Research-Evolution.md`), specifically scrolling through the **A-to-B Evidence Table**.
- **1:30 – 2:30:** Display the Form 10-K Cash Flow Statement (PDF p. 137 / p. F-9) pointing to the $1.34B computer hardware capex, then return to the table.
- **2:30 – 2:50:** Face camera / final slide summarizing the unchanged WATCH-DEFER stance.

### Word-for-Word Spoken Script

> **[0:00 – 0:35 | The Edition A Baseline]**  
> *"Hi everyone, my name is Elliot. Today I’m presenting the research evolution of my FIN 43900 valuation of IREN Limited.  
> On September 3rd, I submitted my Edition A baseline in Lab 04. My initial recommendation was **WATCH / DEFER**. At the time, IREN had just reported strong top-line revenue of $707 million and announced that its first 50-megawatt AI data center, Horizon 1, had been accepted by Microsoft. But my qualitative judgment hesitated: the company had suffered a massive GAAP net loss of over $702 million, reported nearly $14 billion in capital commitments, and relied on $11 billion in debt and equity financing. I didn’t want to initiate a buy until I had proof of sustainable cash generation."*

> **[0:35 – 1:30 | The Analytical Shift: From Intuition to Accounting Proof]**  
> *"Over the past four weeks, my thesis and recommendation remained stable at **WATCH / DEFER**, but the evidence behind it underwent a complete transformation.  
> In Edition A, my deferral was an intuitive reaction to headline net losses. In Edition B, I built a fully integrated five-year three-statement pro-forma financial model. The model proved mathematically that even if IREN scales recognized GAAP revenue at 100% in FY27 and 50% in FY28—reaching $3.5 billion by 2031—the required cash capex of $2.5 billion in Year 1 and $1.5 billion in Year 2 consumes all cash flow. Operating cash flow cannot cover debt service and capex until Year 4."*

> **[1:30 – 2:20 | Auditing the Data: Uncovering the Hidden Capex]**  
> *"This evolution was driven by my own independent auditing of the filings. When I inspected financial aggregators like Yahoo Finance and CapIQ, they reported IREN's FY2026 capex as $3.0 billion. But when I audited the primary Form 10-K cash flow statement, I discovered an additional $1.34 billion line item titled 'Payments for computer hardware'—purchases of NVIDIA GPU clusters. The aggregators were understating IREN's actual capital drain by over 30%!  
> Furthermore, in Lab 10, when an AI tool suggested using a standard inventory turnover formula, I rejected it because IREN is a pure digital infrastructure and cloud compute business that carries **zero inventory**. Instead, I modeled **Customer Prepayments** from Microsoft—$1.84 billion in cash advances—as the company’s primary non-dilutive working capital engine."*

> **[2:20 – 2:45 | Conclusion & Attribution]**  
> *"To summarize: my recommendation did not change, but my understanding evolved from headline skepticism to an audited, company-specific operating model. The change was driven primarily by course instruction on three-statement articulation, peer feedback in Labs 11 and 12, and my own primary source auditing. Thank you."*

---

## 📹 Video 2: Codebase Architecture & Validation Suite

**Maximum Duration:** **≤ 5:00 minutes** (Recommended target: **4:00 – 4:30**)  
**Core Question to Answer:** *How does the submitted code produce the result, and what high-risk test passed or failed?*  
**Deliverable File to Submit Later:** `Video 2` link + `transcript-video-2.txt`  

### Screen-Sharing Plan
- **0:00 – 0:45:** Open VS Code showing the repository directory tree: `run_analysis.py`, `Lab-10/proforma_iren.py`, `visible_output.json`, and `docs/`.
- **0:45 – 1:45:** Open [`Project-1/dcf.py`](../Project-1/dcf.py) lines 11–28, showing the historical Week 3 script. Run it in terminal to show the negative compounding failure (-$196.34/sh).
- **1:45 – 3:00:** Open [`Lab-10/proforma_iren.py`](../Lab-10/proforma_iren.py). Walk through the 3-statement logic, the double-entry check loop (`Gap == 0.0000`), and run Test 2 (the +$500M cash break refusal gate).
- **3:00 – 4:00:** Open [`docs/Validation-and-AI-Use.md`](../docs/Validation-and-AI-Use.md), showing the **Locked Changed-Input Record** and the precommit prediction table.
- **4:00 – 4:30:** Open terminal and run `py run_analysis.py`. Show the clean output and how it populates `visible_output.json`.

### Word-for-Word Spoken Script

> **[0:00 – 0:45 | Introduction & Repository Architecture]**  
> *"Hello, I’m Elliot. In this second video, I’ll walk through the technical execution, accounting integrity gates, and validation suite of my IREN valuation codebase.  
> As you can see in my repository structure, the codebase is anchored by `run_analysis.py`, which integrates the five-year three-statement pro-forma engine from Lab 10 and exports our frozen visible output contract to `visible_output.json`. Everything is tracked under Git on branch main."*

> **[0:45 – 1:45 | The High-Risk Failure: Preserving the Week 3 DCF Bug]**  
> *"To understand why the pro-forma is essential, let’s first look at my preserved Week 3 model in `Project-1/dcf.py`.  
> In Week 3, we used a standard DCF formula where cash flow grows by explicit percentage rates. When I plugged in IREN’s actual FY2026 cash flow of negative $2,191 million, applying positive growth rates like 50% and 35% compounded the negative number! By Year 5, cash flow plunged to negative $6.3 billion, yielding an impossible enterprise value of negative $60 billion and a share price of -$196. The reverse DCF broke completely.  
> Rather than deleting this failure, I preserved it in the repository as required by the course rubric. It taught me that capital-intensive infrastructure companies cannot use generic cash-flow growth multipliers; they require dynamic statement modeling."*

> **[1:45 – 3:00 | The Pro-Forma Engine & Refusal Gates]**  
> *"In Lab 10, I solved this by building `proforma_iren.py`.  
> The model projects Revenue based on megawatt energization, Cost of Power at 70% cash gross margin, and separate capex that tapers from $2.5 billion down to $600 million as facilities are completed. Cash flow to equity remains negative in Years 1 through 3, but turns positive in Year 4 at $131 million and Year 5 at $380 million.  
> Crucially, the model enforces strict double-entry accounting integrity. In every single year, Assets must equal Liabilities plus Equity.  
> Watch what happens when I run our automated refusal test: Test 2 artificially injects a $500 million cash discrepancy into Year 2. The script halts immediately with a loud error: `MODEL REFUSAL: Balance sheet check failed! Gap = $+500.0M`. The model strictly refuses to value an out-of-balance forecast."*

> **[3:00 – 4:00 | The Locked Changed-Input Test]**  
> *"Next, let’s look at my validation record in `Validation-and-AI-Use.md`.  
> Before running the sensitivity suite, I precommitted a human prediction with AI closed at commit `3125ff9`. I predicted that shifting the 5-year revenue growth path up by +5 percentage points would significantly scale Year 5 revenue and free cash flow, but would not flip the overall decision from WATCH-DEFER because intermediate capex burn remains massive.  
> When executed, Year 5 revenue scaled to $4.2 billion, and implied value rose from -$5.31 to +$0.99 per share. The prediction matched directionally, proving that capacity energization is the dominant operating driver, while confirming that the recommendation remains WATCH-DEFER."*

> **[4:00 – 4:30 | Final Execution & Reproducibility]**  
> *"Finally, when I run `py run_analysis.py` in terminal, it runs in under two seconds, confirms all five years balance with Gap = 0.0000, and writes the frozen contract to `visible_output.json`. The codebase is 100% reproducible and locked. Thank you."*

---

## 📹 Video 3: Product Demonstration & Investment Committee Defense

**Maximum Duration:** **≤ 5:00 minutes** (Recommended target: **4:15 – 4:45**)  
**Core Structure:**  
- **First 60 seconds (MANDATORY):** Live interactive product demonstration (`app.py`).  
- **Remaining 3–4 minutes:** Buy-side Investment Committee presentation and recommendation defense.  
**Deliverable File to Submit Later:** `Video 3` link + `transcript-video-3.txt`  

### Screen-Sharing Plan
- **0:00 – 1:05 (Live Product Demo):** Open browser displaying local Streamlit app (`py -m streamlit run app.py`).
  - Move the **Cash Gross Margin slider** from 70% to 75% and point to the updated FCFF value ($15.45/sh).
  - Move the **Revenue Growth shift slider** to +5 pp and point to the value ($19.25/sh).
  - Click the **"Reset to Base Case"** button to restore $12.12/sh.
  - Show the green **"DOUBLE-ENTRY ACCOUNTING INTEGRITY: PASS"** badge.
- **1:05 – 2:30:** Switch to [`Decision-Memo.pdf`](../Decision-Memo.pdf) Page 1, pointing to Table 1 (Enterprise-to-Equity Bridge).
- **2:30 – 3:30:** Scroll to Page 2, pointing to Table 2 (Sensitivity Spans) and the Reversal Triggers.
- **3:30 – 4:30:** Face camera / final slide delivering the formal committee ask and next review milestone.

### Word-for-Word Spoken Script

> **[0:00 – 1:05 | Live Product Demonstration (Mandatory Opening)]**  
> *"Good afternoon, members of the Investment Committee. My name is Elliot.  
> Before presenting our recommendation on IREN Limited, I want to demonstrate our interactive valuation workbench. As required, this is a live, semi-adjustable product built for our analyst team.  
> On the left driver panel, our accounting engine is locked, while our key load-bearing drivers are exposed with bounded controls.  
> Right now, our base case produces a primary FCFF intrinsic value of **$12.12 per share**.  
> If our energy team believes IREN can negotiate better power rates, I can adjust the Cash Gross Margin slider from 70% to 75%. You can see the model live-rebalances: Year 5 EBIT expands to $891 million, and intrinsic value rises to **$15.45 per share**.  
> If I test an aggressive cluster delivery scenario—shifting revenue growth up by +5 percentage points across all five years—value rises to **$19.25 per share**.  
> And with one click on our 'Reset to Base Case' button, all sliders return to our audited baseline.  
> Most importantly, at the top of the screen, our green accounting check badge confirms that every single statement articulates with zero balance sheet gap."*

> **[1:05 – 2:30 | Committee Recommendation & The Enterprise Bridge]**  
> *"Now turning to our formal investment recommendation: the AI Task Force recommends that the fund **DO NOT INITIATE** an equity position in IREN Limited and place the name on our **WATCH / DEFER** list.  
> The market currently prices IREN at **$45.73 per share**, an $18 billion equity valuation. The market is treating IREN as an unencumbered hyperscale AI winner because of its $9.7 billion Microsoft contract and customer acceptance of Horizon 1.  
> But looking at Table 1 of our decision memo, our audited pro-forma DCF model produces an enterprise value of $6.7 billion. Adding IREN's $5.9 billion in cash and deducting its $7.8 billion in debt yields an intrinsic equity value of $4.8 billion, or **$12.12 per share**.  
> The stock is trading at an astounding **280% market premium** over fundamental operating DCF value!  
> Why? Because scaling to 1.2 gigawatts requires massive capital expenditure. In FY2026, IREN burned $4.33 billion in cash capex and reported an operating loss of over $1.0 billion. Free cash flow to equity will remain deeply negative through 2029."*

> **[2:30 – 3:30 | Sensitivities & The Capex Burden]**  
> *"Our sensitivity analysis in Table 2 reveals two critical insights:  
> First, the Capacity Energization Path is the dominant operating driver, creating a $15.19 per share span, more than double the impact of power margin fluctuations.  
> Second, even if we combine our most aggressive upside assumptions—accelerating megawatt energization and optimizing power margins—intrinsic value only reaches **$19.25 per share**.  
> There is no fundamental operating scenario where IREN is worth $45.73 today. The market price is pricing in decades of uninterrupted hyper-growth with zero operational execution buffer."*

> **[3:30 – 4:30 | Observable Reversal Triggers & Next Review Point]**  
> *"We do not recommend shorting the stock due to extreme retail momentum and high borrowing fees. Instead, we propose three observable monitoring triggers to revisit our recommendation:  
> 1. **Customer Acceptance:** Verified delivery and billing of Childress Horizons 2, 3, and 4, scaling recognized GAAP quarterly revenue above $375 million.  
> 2. **Operating Cash Flow Inflection:** Two consecutive quarters of positive cash flow from operations before customer advances.  
> 3. **Market Price Correction:** A market pullback toward our fundamental valuation band of $12 to $18 per share.  
> Our committee ask: maintain zero allocation. We will review the name upon the Q2 FY2027 earnings release in February. Thank you, and I look forward to your questions."*
