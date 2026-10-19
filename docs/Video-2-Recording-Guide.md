# Video 2 Recording Guide: Code Architecture, Validation, and Changed-Input Testing

**Student:** Elliot (one "t")  
**Course:** FIN 43900 (Corporate Finance / Applied Financial Modeling, Purdue University)  
**Company:** IREN Limited (NASDAQ: IREN)  
**Maximum Allowed Duration:** **5:00 minutes**  
**Target Duration:** **3:45 – 4:15 minutes** (comfortably below the 5:00 minute ceiling)  
**Deliverable Artifacts Produced Later:** Video 2 recording file + `transcript-video-2.txt` / `.vtt`

---

## 1. What the Professor is Evaluating in Video 2

The professor is evaluating whether your financial valuation codebase possesses **genuine technical integrity, automated accounting safeguards, and reproducible validation**:
- **Codebase Organization & Cold-Run Reproducibility:** Showing how the files connect (`run_analysis.py`, `Lab-10/proforma_iren.py`, `visible_output.json`) and running the master execution command cleanly from terminal.
- **Transparent Historical Failure Analysis:** Preserving and explaining your actual Week 3 DCF failure ([`Project-1/dcf.py`](../Project-1/dcf.py)), where a generic cash-flow growth formula compounded negative starting cash flows into -$196.34/share. Explaining why financial institutions preserve broken models rather than deleting them.
- **Double-Entry Articulation Integrity:** Demonstrating that your five-year pro-forma forecast enforces $\text{Assets} - \text{Liabilities} - \text{Equity} = 0.0000$ across every single year.
- **Fail-Loud Refusal Gates:** Executing an intentional break test where injecting a $+ \$500\text{M}$ artificial cash discrepancy causes the model to loudly halt with `MODEL REFUSAL: Balance sheet check failed`.
- **Genuine Locked Changed-Input Record:** Walking through your precommitted human prediction logged at Git commit `3125ff9` *prior* to executing code, proving directional monotonicity and demonstrating that Capacity Energization is the dominant operating driver.

---

## 2. Pre-Recording Setup: Applications & Files to Open

Open the following before starting the Zoom recording:

1. **VS Code (or Editor of Choice):**  
   - Open the root folder `C:\Users\ellio\Documents\FIN439\IREN-research`.
   - Have the file explorer sidebar expanded so the folder hierarchy is clearly visible.
   - Pre-open these tabs in VS Code:
     1. [`Project-1/dcf.py`](../Project-1/dcf.py) (scrolled to lines 11–30)
     2. [`Lab-10/proforma_iren.py`](../Lab-10/proforma_iren.py) (scrolled to the valuation engine / refusal gate section)
     3. [`docs/Validation-and-AI-Use.md`](Validation-and-AI-Use.md) (scrolled to Section 4: *Locked Changed-Input Record*)
     4. [`visible_output.json`](../visible_output.json)
2. **Terminal Window (integrated in VS Code or standalone Windows PowerShell):**  
   - Working directory must be: `C:\Users\ellio\Documents\FIN439\IREN-research`
   - Test that commands work smoothly by typing `py --version` before hitting record.

---

## 3. Step-by-Step Screen-Sharing Click Path & Commands

Follow this chronological sequence:

| Timestamp | Application on Screen | What to Click / Type | What You Are Explaining |
|---|---|---|---|
| **0:00 – 0:40** | VS Code File Tree | Point cursor at file explorer: `run_analysis.py`, `Lab-10/`, `visible_output.json`. | Introduce yourself and your codebase architecture: anchored by `run_analysis.py` and locked to Git `main`. |
| **0:40 – 1:35** | `Project-1/dcf.py` + Terminal | Open `dcf.py`. Highlight lines 15–28. In terminal, run:<br>`py Project-1/dcf.py` | Explain the Week 3 failure: generic growth rate compounded negative starting cash flow into -$196.34/share. Explain why preserving historical failures proves modeling integrity. |
| **1:35 – 2:45** | `Lab-10/proforma_iren.py` + Terminal | Switch tab to `proforma_iren.py`. Highlight double-entry check loop (`Gap == 0.0000`). In terminal, run:<br>`py Lab-10/proforma_iren.py --test` | Show Test 1 (Valid Base Case), Test 2 (Refusal Gate: +$500M cash break triggers `MODEL REFUSAL`), and Test 3 (Valid restoration). Explain fail-loud accounting safeguards. |
| **2:45 – 3:35** | `docs/Validation-and-AI-Use.md` | Switch tab to Section 4 (*Locked Changed-Input Record*). Point cursor at precommit timestamp and prediction table. | Walk through genuine human precommit predictions logged before code run at commit `3125ff9`. Margin helps ($12.12 $\rightarrow$ $14.61), but revenue path shift dominates ($12.12 $\rightarrow$ $19.25), confirming Capacity Energization hierarchy. |
| **3:35 – 4:05** | Terminal + `visible_output.json` | In terminal, run:<br>`py run_analysis.py`<br>Then switch tab to `visible_output.json`. | Show the clean execution summary in terminal (<2 seconds) and show the generated contract in `visible_output.json`. Conclude cleanly. |

---

## 4. Spoken Script (Natural & Conversational)

> **[0:00 – 0:40 | Introduction and Codebase Architecture]**  
> *"Hello, my name is Elliot. In this second video, I’ll walk through the technical execution, accounting integrity safeguards, and validation suite of my IREN valuation codebase.  
> As you can see in my repository structure, the codebase is centered on `run_analysis.py`, which coordinates our five-year three-statement pro-forma engine in `Lab-10/` and exports our frozen data contract to `visible_output.json`. Everything is tracked under Git on branch `main`."*

> **[0:40 – 1:35 | The High-Risk Model Failure: Preserving the Week 3 DCF]**  
> *(Click on tab `Project-1/dcf.py` and bring terminal into view)*  
> *"To understand why an integrated three-statement pro-forma was necessary, let’s first examine my preserved Week 3 model in `Project-1/dcf.py`.  
> In Week 3, we used a traditional DCF formula where cash flow grows by explicit percentage multipliers. Watch what happened when I applied this to IREN in terminal:*  
> *(Run: `py Project-1/dcf.py`)*  
> *"Because IREN’s starting FY2026 cash flow was negative $2.19 billion due to massive capital expenditure, applying positive growth rates like 50% and 35% compounded the negative cash flow! By Year 5, cash flow plunged to negative $6.3 billion, yielding an impossible enterprise value of negative $60 billion and an implied share price of negative $196.  
> Rather than deleting this broken script, I preserved it in the repository. In corporate finance, preserving broken iterations is essential for institutional memory: it proved that capital-intensive infrastructure companies cannot be modeled with generic top-down growth formulas; they require statement-by-statement dynamic accounting."*

> **[1:35 – 2:45 | The Dynamic Pro-Forma Engine & Fail-Loud Refusal Gates]**  
> *(Click on tab `Lab-10/proforma_iren.py`)*  
> *"In Lab 10, I solved this by building `proforma_iren.py`.  
> Here, revenue scales with megawatt energization, cash cost of power is modeled at 70% gross margin, and capital expenditures taper from $2.5 billion down to $600 million as facilities are energized.  
> Most importantly, the model enforces strict double-entry balance sheet articulation: in every forecast year, Assets minus Liabilities minus Equity must equal exactly zero.  
> Let’s run our automated test suite in terminal using the `--test` flag:*  
> *(Run: `py Lab-10/proforma_iren.py --test`)*  
> *"Look at Test 2: the test intentionally breaks the balance sheet by injecting a $500 million cash discrepancy into FY2028.  
> As you can see, the engine halts immediately and throws a loud error: `MODEL REFUSAL: Balance sheet check failed in FY2028E! Discrepancy = $+500.0M. Model strictly refuses to value an invalid forecast.`  
> This refusal gate ensures that an out-of-balance forecast can never silently produce a corrupt valuation."*

> **[2:45 – 3:35 | The Genuine Locked Changed-Input Record]**  
> *(Click on tab `docs/Validation-and-AI-Use.md` and scroll to Section 4)*  
> *"Next, let’s examine my Locked Changed-Input Record in `Validation-and-AI-Use.md`.  
> Before running the sensitivity suite, I logged human precommit predictions with AI closed at Git commit `3125ff9`.  
> I predicted that expanding cash gross margin from 70% to 75% would increase operating income and intrinsic value monotonically, but would be secondary to capex. When executed, FCFF value rose from $12.12 to $14.61 per share.  
> I then tested shifting the five-year revenue growth path up by +5 percentage points per year. As predicted, revenue scaled dramatically, raising FCFF value from $12.12 to $19.25 per share, and swinging FCFE from negative $5.31 to positive $0.99.  
> Both tests confirmed directional monotonicity and established that Capacity Energization is the dominant operating driver, while confirming our overall recommendation remains WATCH-DEFER."*

> **[3:35 – 4:05 | Cold-Run Execution & Reproducibility]**  
> *(Switch to terminal)*  
> *"Finally, let’s run the master runner from a cold terminal:*  
> *(Run: `py run_analysis.py`)*  
> *"In 1.8 seconds, the script verifies all 12 checks, confirms balance sheet gap equals 0.0000, and writes the frozen output to `visible_output.json`.  
> Opening `visible_output.json`, you can see the complete contract is fully verified and 100% reproducible. Thank you."*

---

## 5. Exact Terminal Commands to Run During Video 2

Run these three commands in order in your terminal:

```powershell
# Command 1: Demonstrate the preserved Week 3 DCF failure (-$196.34/sh)
py Project-1/dcf.py

# Command 2: Execute Lab 10 Automated Test Suite & Refusal Gate (+ $500M cash break)
py Lab-10/proforma_iren.py --test

# Command 3: Execute Master Valuation Runner and regenerate visible_output.json
py run_analysis.py
```

---

## 6. Key Financial & Technical Numbers Verified for Video 2

- **Week 3 Failed Model Share Price:** -$196.34 / share (EV -$60.5B, Year 5 FCF -$6.3B)
- **Lab 10 Double-Entry Articulation Gap:** `0.0000` across all 5 forecast years (FY27E–FY31E)
- **Refusal Gate Discrepancy Injected:** $+ \$500.0\text{M}$ cash break in FY2028E
- **Precommit Git Commit Hash:** `3125ff9` (Timestamp: 2026-09-29 14:30 EDT)
- **Margin Sensitivity Result (+5 pp):** FCFF $12.12 $\rightarrow$ $14.61 / share (+$2.49); FCFE -$5.31 $\rightarrow$ -$2.93 / share
- **Revenue Path Sensitivity Result (+5 pp/yr):** FCFF $12.12 $\rightarrow$ $19.25 / share (+$7.13); FCFE -$5.31 $\rightarrow$ +$0.99 / share
- **Master Engine Execution Time:** $< 2.0$ seconds

---

## 7. Common Recording Mistakes to Avoid

- **Mistake 1: Trying to hide the Week 3 failure.** The grading rubric specifically awards points for transparently explaining high-risk failures and how they motivated subsequent architectural improvements.
- **Mistake 2: Typing commands too quickly or with typos.** Have the commands typed in a scratchpad or use the terminal history (press Up Arrow) so they run smoothly on camera.
- **Mistake 3: Inventing fake offline AI timestamps.** Point directly to the authentic precommit timestamp (2026-09-29 14:30 EDT) and commit `3125ff9` in `docs/Validation-and-AI-Use.md`.
- **Mistake 4: Exceeding 5:00 minutes.** This plan takes approximately 3:55 to 4:10. Stay on schedule and transition promptly between tabs.

