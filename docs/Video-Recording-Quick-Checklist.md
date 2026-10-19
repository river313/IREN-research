# Project 1 Video Recording Quick Checklist & Screen Staging Guide

**Student:** Elliot (one "t")  
**Course:** FIN 43900 (Corporate Finance / Applied Financial Modeling, Purdue University)  
**Company:** IREN Limited (NASDAQ: IREN)  
**Environment:** Windows PowerShell + Zoom Screen Sharing

Keep this one-page checklist on your phone or second monitor when recording your three Project 1 videos in your dorm room.

---

## 🛠️ Phase 1: Dorm Room & Computer Pre-Flight (Do Once Before Recording)

- [ ] **Quiet Environment:** Close your dorm door, turn off fans/AC or high-noise appliances.
- [ ] **Windows "Do Not Disturb":** Turn on Focus Assist / Do Not Disturb in Windows 11 to silence notifications, emails, and Discord dings.
- [ ] **Zoom Audio Check:**
  - In Zoom settings $\rightarrow$ Audio $\rightarrow$ Test Mic & Speaker.
  - Set Zoom to **"Suppress background noise: Auto"** or Low.
  - Set Zoom video recording to save locally on your laptop (`Record on this Computer`).
- [ ] **Zoom Screen Share Setup:**
  - Share your **entire primary monitor** (or desktop screen) rather than a single window, so that switching between VS Code, PDF Reader, and Browser happens smoothly without black screens.
- [ ] **Terminal Working Directory:**  
  Open PowerShell in:  
  `C:\Users\ellio\Documents\FIN439\IREN-research`

---

## 📹 Video 1 Quick Card: Research Evolution & Evidence Trajectory

- **Duration Constraint:** **Maximum 3:00 minutes** (Target: **2:25 – 2:35**)
- **Windows to Pre-Stage:**
  1. `IREN_2026-09-03_report.md` (VS Code or text viewer, top of file ready to scroll to Section 6)
  2. `Research-Evolution.pdf` (PDF Reader, open to page 1 showing the A-to-B Evidence Table)
- **Key Spoken Points & Cues:**
  1. **[0:00 – 0:35]** Introduce Elliot. Point to `IREN_2026-09-03_report.md` (Commit `2710819`). Original recommendation: WATCH / DEFER based on headline net loss ($(702.6)M) and capex hesitation.
  2. **[0:35 – 1:30]** Switch to `Research-Evolution.pdf`. Walk through A-to-B table. Recommendation stayed WATCH / DEFER, but foundation shifted from intuitive hesitation to audited 5-year pro-forma DCF ($12.12/sh vs. $45.73 market price).
  3. **[1:30 – 2:15]** Explain primary source audit: Aggregators reported $3.0B capex; Form 10-K Cash Flow Stmt (p. F-9) revealed $1.34B in computer hardware payments, establishing true cash capex of $4.33B. Rejected inventory ($0) and modeled Microsoft's $1.84B prepayments.
  4. **[2:15 – 2:35]** Conclude: changes driven by course instruction, peer feedback, and filing audits.
- **Stop Recording at or before 2:45.**

---

## 📹 Video 2 Quick Card: Code Architecture, Validation & Changed-Input Testing

- **Duration Constraint:** **Maximum 5:00 minutes** (Target: **3:50 – 4:10**)
- **Windows to Pre-Stage:**
  1. VS Code showing file tree (`IREN-research`) with tabs open:
     - `Project-1/dcf.py` (lines 15–28)
     - `Lab-10/proforma_iren.py`
     - `docs/Validation-and-AI-Use.md` (Section 4: Locked Changed-Input Record)
     - `visible_output.json`
  2. Terminal at the bottom of VS Code or alongside it.
- **Commands to Run Chronologically:**
  ```powershell
  # 1. Run at ~0:55 to show Week 3 negative compounding failure (-$196.34/sh)
  py Project-1/dcf.py

  # 2. Run at ~2:00 to show refusal gate failure on +$500M cash break
  py Lab-10/proforma_iren.py --test

  # 3. Run at ~3:40 to show cold-run master execution in <2 seconds
  py run_analysis.py
  ```
- **Key Spoken Points & Cues:**
  1. **[0:00 – 0:40]** Introduce codebase architecture: `run_analysis.py` orchestrates `proforma_iren.py` and exports `visible_output.json`.
  2. **[0:40 – 1:35]** Run `Project-1/dcf.py`. Show -$196.34/share failure. Explain why preserving historical failures demonstrates scientific and modeling integrity.
  3. **[1:35 – 2:45]** Run `py Lab-10/proforma_iren.py --test`. Highlight Test 2 loud refusal error: `MODEL REFUSAL: Balance sheet check failed... Gap = $+500.0M`.
  4. **[2:45 – 3:35]** Show `Validation-and-AI-Use.md` Section 4. Explain human precommit prediction at commit `3125ff9`: Margin expansion ($12.12 $\rightarrow$ $14.61) is secondary to revenue path shift ($12.12 $\rightarrow$ $19.25), proving Capacity Energization is dominant driver.
  5. **[3:35 – 4:05]** Run `py run_analysis.py` and open `visible_output.json`.
- **Stop Recording at or before 4:20.**

---

## 📹 Video 3 Quick Card: Live Product Demo & Investment Committee Defense

- **Duration Constraint:** **Maximum 5:00 minutes** (Target: **4:15 – 4:35**)
- **CRITICAL OPENING RULE:** **Start on the web browser displaying the live Streamlit app!**
- **Windows to Pre-Stage:**
  1. Terminal running: `py -m streamlit run app.py` (start *before* opening Zoom)
  2. Browser open to `http://localhost:8501` (full screen, showing green accounting check badge and $12.12/sh base)
  3. `Decision-Memo.pdf` (PDF Reader, ready on Page 1)
- **Live Product Demonstration Sequence (First 60–90 Seconds):**
  1. **[0:00 – 0:25]** Greet committee. Point out green badge: **PASS (Gap = 0.0000)** and base value **$12.12 / share**.
  2. **[0:25 – 0:45]** Drag **Cash Gross Margin slider** from 70% $\rightarrow$ **75%** (show value rises to **$14.61**).
  3. **[0:45 – 1:05]** Drag **Revenue Growth slider** to **+5.0 pp** (show value rises to **$19.25**).
  4. **[1:05 – 1:15]** Click **"Reset to Base Case"** button (show sliders snap back and value returns to **$12.12**).
- **Committee Presentation Sequence (Remaining 3–4 Minutes):**
  1. **[1:15 – 2:30]** Switch to `Decision-Memo.pdf` Page 1. Committee ask: **WATCH / DEFER** at $45.73 market price (~280% premium over $12.12 value). Walk through Table 1 Enterprise Bridge: EV $6,715M + Cash $5,896M - Debt $7,837M = Equity $4,774M / 394M shares = $12.12. Reconcile with -$5.31 FCFE.
  2. **[2:30 – 3:35]** Scroll to Page 2, Table 2. Explain driver hierarchy: Capacity Energization ($15.19 span) dominates. Combined upside only yields $19.25; $45.73 market price prices in perfection.
  3. **[3:35 – 4:35]** Detail 3 observable reversal triggers (Horizons 2–4 customer acceptance, quarterly GAAP revenue >$375M with positive CFO, and <10% dilution). Conclude with committee action: zero allocation, revisit at Q2 FY2027 earnings.
- **Stop Recording at or before 4:45.**

---

## 📁 Phase 3: Post-Recording Steps (When Finished)

After Zoom finishes converting the recordings:

1. **Check Video Durations:**
   - Video 1: Must be $\le 3:00$ (e.g., 2:28)
   - Video 2: Must be $\le 5:00$ (e.g., 4:02)
   - Video 3: Must be $\le 5:00$ (e.g., 4:26)
2. **Rename Video Files:**
   - Rename Zoom `.mp4` files to:  
     `Video-1-Research-Evolution.mp4`  
     `Video-2-Code-Architecture.mp4`  
     `Video-3-Product-Demo-Committee-Defense.mp4`
3. **Generate Transcripts:**  
   Generate exact transcripts from your recorded audio (using Zoom auto-transcript, Microsoft Word transcribe, or OpenAI Whisper) and save as:
   - `transcript-video-1.txt` (or `.vtt`)
   - `transcript-video-2.txt` (or `.vtt`)
   - `transcript-video-3.txt` (or `.vtt`)
4. **Update Submission Manifest:**  
   In [`project-submission-manifest-template.csv`](../project-submission-manifest-template.csv), fill in the exact video links, titles, durations, and commit hash.

